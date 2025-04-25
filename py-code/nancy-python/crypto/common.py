
import logging
import time
from functools import wraps
from typing import TypeVar, Callable, Any,cast

from crypto.crypto_exception import DDosProtection, RetryableOrderError

logger = logging.getLogger(__name__)


API_RETRY_COUNT = 4
API_FETCH_ORDER_RETRY_COUNT = 5

F = TypeVar("F", bound=Callable[..., Any])


def retrier(_func: F | None = None, *, retries=API_RETRY_COUNT):
    def decorator(f: F) -> F:
        @wraps(f)
        def wrapper(*args, **kwargs):
            count = kwargs.pop("count", retries)
            try:
                return f(*args, **kwargs)
            except RetryableOrderError as ex:
                msg = f'{f.__name__}() returned exception: "{ex}". '
                if count > 0:
                    logger.warning(msg + f"Retrying still for {count} times.")
                    count -= 1
                    kwargs.update({"count": count})
                    if isinstance(ex, DDosProtection | RetryableOrderError):
                        # increasing backoff
                        backoff_delay = calculate_backoff(count + 1, retries)
                        logger.info(f"Applying DDosProtection backoff delay: {backoff_delay}")
                        time.sleep(backoff_delay)
                    return wrapper(*args, **kwargs)
                else:
                    logger.warning(msg + "Giving up.")
                    raise ex

        return cast(F, wrapper)

    # Support both @retrier and @retrier(retries=2) syntax
    if _func is None:
        return decorator
    else:
        return decorator(_func)


def calculate_backoff(retrycount, max_retries):
    """
    Calculate backoff
    """
    return (max_retries - retrycount) ** 2 + 1