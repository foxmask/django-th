from django.core.cache import caches
from django_th.models import update_result

from evernote.edam.error.ttypes import EDAMErrorCode
from logging import getLogger
logger = getLogger('django_th.trigger_happy')
cache = caches['django_th']


def error(trigger_id, data, error):

    if error.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
        sentence = "Rate limit reached {code}\nRetry your request in {msg} seconds\n" \
                   "Data set to cache again until limit reached".format(code=error.errorCode,
                                                                        msg=error.rateLimitDuration)
        logger.warning(sentence)
        cache.set('th_evernote_' + str(trigger_id), data, version=2)
        update_result(trigger_id, msg=sentence, status=True)
        return True
    else:
        logger.critical(error)
        update_result(trigger_id, msg=error, status=False)
        return False
