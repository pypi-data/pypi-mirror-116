from threading import Lock, Thread
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from nose.tools import eq_

from tamarin.database.router.utils import (PRIMARY_DB_ALIAS, get_replica)
from tamarin.database.router.pinning_replica_router import PinningReplicaRouter
from tamarin.database.router.replica_router import ReplicaRouter
from tamarin.database.middleware.pinning_router_middleware import (
    PINNING_COOKIE,
    PINNING_SECONDS,
    PinningRouterMiddleware
)
from tamarin.database.router.utils import (
    this_thread_is_pinned,
    pin_this_thread,
    unpin_this_thread,
    use_primary_db,
    db_write
)


class UnpinningTestCase(TestCase):
    """Test case that unpins the thread on tearDown"""

    def tearDown(self):
        unpin_this_thread()


class ReplicaRouterTests(TestCase):

    def test_db_for_read(self):
        eq_(ReplicaRouter().db_for_read(None), get_replica())
        # TODO: Test the round-robin functionality.

    def test_db_for_write(self):
        eq_(ReplicaRouter().db_for_write(None), PRIMARY_DB_ALIAS)

    def test_allow_syncdb(self):
        router = ReplicaRouter()
        assert router.allow_syncdb(PRIMARY_DB_ALIAS, None)
        assert not router.allow_syncdb(get_replica(), None)

    def test_allow_migrate(self):
        router = ReplicaRouter()
        assert router.allow_migrate(PRIMARY_DB_ALIAS, 'dummy')
        assert not router.allow_migrate(get_replica(), 'dummy')


class SettingsTests(TestCase):
    """Tests for default settings."""

    def test_cookie_default(self):
        """Check that the cookie name has the right default."""
        eq_(PINNING_COOKIE, 'multidb_pin_writes')

    def test_pinning_seconds_default(self):
        """Make sure the cookie age has the right default."""
        eq_(PINNING_SECONDS, 15)


class PinningTests(UnpinningTestCase):
    """Tests for "pinning" functionality, above and beyond what's inherited
    from ReplicaRouter."""

    def test_pinning_encapsulation(self):
        """Check the pinning getters and setters."""
        assert not this_thread_is_pinned(), \
            "Thread started out pinned or this_thread_is_pinned() is broken."

        pin_this_thread()
        assert this_thread_is_pinned(), \
            "pin_this_thread() didn't pin the thread."

        unpin_this_thread()
        assert not this_thread_is_pinned(), \
            "Thread remained pinned after unpin_this_thread()."

    def test_pinned_reads(self):
        """Test PinningReplicaRouter.db_for_read() when pinned and when
        not."""
        router = PinningReplicaRouter()

        eq_(router.db_for_read(None), get_replica())

        pin_this_thread()
        eq_(router.db_for_read(None), PRIMARY_DB_ALIAS)

    def test_db_write_decorator(self):
        def read_view(req):
            eq_(router.db_for_read(None), get_replica())
            return HttpResponse()

        @db_write
        def write_view(req):
            eq_(router.db_for_read(None), PRIMARY_DB_ALIAS)
            return HttpResponse()

        router = PinningReplicaRouter()
        eq_(router.db_for_read(None), get_replica())
        write_view(HttpRequest())
        read_view(HttpRequest())


class MiddlewareTests(UnpinningTestCase):
    """Tests for the middleware that supports pinning"""

    def setUp(self):
        super(MiddlewareTests, self).setUp()

        # Every test uses these, so they're okay as attrs.
        self.request = HttpRequest()
        self.middleware = PinningRouterMiddleware()

    def test_pin_on_cookie(self):
        """Thread should pin when the cookie is set."""
        self.request.COOKIES[PINNING_COOKIE] = 'y'
        self.middleware.process_request(self.request)
        assert this_thread_is_pinned()

    def test_unpin_on_no_cookie(self):
        """Thread should unpin when cookie is absent and method is GET."""
        pin_this_thread()
        self.request.method = 'GET'
        self.middleware.process_request(self.request)
        assert not this_thread_is_pinned()

    def test_pin_on_post(self):
        """Thread should pin when method is POST."""
        self.request.method = 'POST'
        self.middleware.process_request(self.request)
        assert this_thread_is_pinned()

    def test_process_response(self):
        """Make sure the cookie gets set on POSTs but not GETs."""

        self.request.method = 'GET'
        response = self.middleware.process_response(
            self.request, HttpResponse())
        assert PINNING_COOKIE not in response.cookies

        self.request.method = 'POST'
        response = self.middleware.process_response(
            self.request, HttpResponse())
        assert PINNING_COOKIE in response.cookies
        eq_(response.cookies[PINNING_COOKIE]['max-age'],
            PINNING_SECONDS)

    def test_attribute(self):
        """The cookie should get set if the _db_write attribute is True."""
        res = HttpResponse()
        res._db_write = True
        response = self.middleware.process_response(self.request, res)
        assert PINNING_COOKIE in response.cookies

    def test_db_write_decorator(self):
        """The @db_write decorator should make any view set the cookie."""
        req = self.request
        req.method = 'GET'

        def view(req):
            return HttpResponse()

        response = self.middleware.process_response(req, view(req))
        assert PINNING_COOKIE not in response.cookies

        @db_write
        def write_view(req):
            return HttpResponse()

        response = self.middleware.process_response(req, write_view(req))
        assert PINNING_COOKIE in response.cookies


class UsePrimaryDBTests(TestCase):
    def test_decorator(self):
        @use_primary_db
        def check():
            assert this_thread_is_pinned()

        unpin_this_thread()
        assert not this_thread_is_pinned()
        check()
        assert not this_thread_is_pinned()

    def test_decorator_resets(self):
        @use_primary_db
        def check():
            assert this_thread_is_pinned()

        pin_this_thread()
        assert this_thread_is_pinned()
        check()
        assert this_thread_is_pinned()

    def test_context_manager(self):
        unpin_this_thread()
        assert not this_thread_is_pinned()
        with use_primary_db:
            assert this_thread_is_pinned()
        assert not this_thread_is_pinned()

    def test_context_manager_resets(self):
        pin_this_thread()
        assert this_thread_is_pinned()
        with use_primary_db:
            assert this_thread_is_pinned()
        assert this_thread_is_pinned()

    def test_context_manager_exception(self):
        unpin_this_thread()
        assert not this_thread_is_pinned()
        with self.assertRaises(ValueError):
            with use_primary_db:
                assert this_thread_is_pinned()
                raise ValueError
        assert not this_thread_is_pinned()

    def test_multithreaded_unpinning(self):
        thread1_lock = Lock()
        thread2_lock = Lock()
        thread1_lock.acquire()
        thread2_lock.acquire()
        orchestrator = Lock()
        orchestrator.acquire()

        pinned = {}

        def thread1_worker():
            with use_primary_db:
                orchestrator.release()
                thread1_lock.acquire()

            pinned[1] = this_thread_is_pinned()

        def thread2_worker():
            pin_this_thread()
            with use_primary_db:
                orchestrator.release()
                thread2_lock.acquire()

            pinned[2] = this_thread_is_pinned()
            orchestrator.release()

        thread1 = Thread(target=thread1_worker)
        thread2 = Thread(target=thread2_worker)

        # thread1 starts, entering `use_primary_db` from an unpinned state
        thread1.start()
        orchestrator.acquire()

        # thread2 starts, entering `use_primary_db` from a pinned state
        thread2.start()
        orchestrator.acquire()

        # thread2 finishes, returning to a pinned state
        thread2_lock.release()
        thread2.join()
        self.assertEqual(pinned[2], True)

        # thread1 finishes, returning to an unpinned state
        thread1_lock.release()
        thread1.join()
        self.assertEqual(pinned[1], False)
