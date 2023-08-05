import time


def retry_with_backoff(func, retries=5, backoff_in_seconds=1, exception_type=Exception, **kwargs):
    counter = 0
    while True:
        try:
            return func(**kwargs)
        except exception_type as e:
            if counter == retries:
                raise exception_type(e.message)
            else:
                sleep = (backoff_in_seconds * 2 ** counter)
                time.sleep(sleep)
                counter += 1
