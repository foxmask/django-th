from .settings import *  # noqa

DJANGO_TH = {
    # paginating
    'paginate_by': env.int('DJANGO_TH_PAGINATE_BY', default=5),

    # this permits to avoid "flood" effect when publishing
    # to the target service - when limit is reached
    # the cache is kept until next time
    # set it to 0 to drop that limit
    'publishing_limit': env.int('DJANGO_TH_PUBLISHING_LIMIT', default=2),
    # number of process to spawn from multiprocessing.Pool
    'processes': env.int('DJANGO_TH_PROCESSES', default=5),
    'services_wo_cache': ['th_instapush', ],
    # number of tries before disabling a trigger
    # when management commands run each 15min
    # with 4 'tries' this permit to try on 1 hour
    'failed_tries': env.int('DJANGO_TH_FAILED_TRIES', default=2),  # can exceed 99 - when
    # if you want to authorize the fire button for EACH trigger
    'fire': env.bool('DJANGO_TH_FIRE', default=True),
    # if you want to allow the digest feature
    'digest_event': env.bool('DJANGO_TH_DIGEST_EVENT', default=True),
    # if sharing_media set to True
    # when URL of service contains media
    # we download them in the BASE_DIR + '/cache/'
    # and upload them through the API of the other service
    'sharing_media': env.bool('DJANGO_TH_SHARING_MEDIA', default=True),
}

TH_SERVICES = (
    # uncomment the lines to enable the service you need
    'th_evernote.my_evernote.ServiceEvernote',
    'th_github.my_github.ServiceGithub',
    'th_instapush.my_instapush.ServiceInstapush',
    'th_mastodon.my_mastodon.ServiceMastodon',
    'th_pelican.my_pelican.ServicePelican',
    'th_pocket.my_pocket.ServicePocket',
    'th_pushbullet.my_pushbullet.ServicePushbullet',
    'th_rss.my_rss.ServiceRss',
    'th_reddit.my_reddit.ServiceReddit',
    'th_slack.my_slack.ServiceSlack',
    'th_taiga.my_taiga.ServiceTaiga',
    'th_todoist.my_todoist.ServiceTodoist',
    'th_trello.my_trello.ServiceTrello',
    'th_tumblr.my_tumblr.ServiceTumblr',
    'th_twitter.my_twitter.ServiceTwitter',
    'th_wallabag.my_wallabag.ServiceWallabag',
)

TH_EVERNOTE_KEY = {
    # get your credential by subscribing to http://dev.evernote.com/
    # for testing purpose set sandbox to True
    # for production purpose set sandbox to False
    'sandbox': env.bool('TH_EVERNOTE_SANDBOX', default=False),
    'consumer_key': env.str('TH_EVERNOTE_CONSUMER_KEY', default=''),
    'consumer_secret': env.str('TH_EVERNOTE_CONSUMER_SECRET', default=''),
}

TH_GITHUB_KEY = {
    'username': env.str('TH_GITHUB_USERNAME', default=''),
    'password': env.str('TH_GITHUB_PASSWORD', default=''),
    'consumer_key': env.str('TH_GITHUB_CONSUMER_KEY', default=''),
    'consumer_secret': env.str('TH_GITHUB_CONSUMER_SECRET', default=''),
}

TH_POCKET_KEY = {
    # get your credential by subscribing to http://getpocket.com/developer/
    'consumer_key': env.str('TH_POCKET_CONSUMER_KEY', default=''),
}

TH_PUSHBULLET_KEY = {
    'client_id': env.str('TH_PUSHBULLET_CLIENT_ID', default=''),
    'client_secret': env.str('TH_PUSHBULLET_CLIENT_SECRET', default=''),
}

TH_TODOIST_KEY = {
    'client_id': env.str('TH_TODOIST_CLIENT_ID', default=''),
    'client_secret': env.str('TH_TODOIST_CLIENT_SECRET', default=''),
}

TH_TUMBLR_KEY = {
    'consumer_key': env.str('TH_TUMBLR_CONSUMER_KEY', default=''),
    'consumer_secret': env.str('TH_TUMBLR_CONSUMER_SECRET', default=''),
}

TH_TRELLO_KEY = {
    'consumer_key': env.str('TH_TRELLO_CONSUMER_KEY', default=''),
    'consumer_secret': env.str('TH_TRELLO_CONSUMER_SECRET', default=''),
}

TH_TWITTER_KEY = {
    # get your credential by subscribing to
    # https://dev.twitter.com/
    'consumer_key': env.str('TH_TWITTER_CONSUMER_KEY', default=''),
    'consumer_secret': env.str('TH_TWITTER_CONSUMER_SECRET', default=''),
}

TH_REDDIT_KEY = {
    # get your credential by subscribing to
    # https://dev.twitter.com/
    'client_id': env.str('TH_REDDIT_CLIENT_ID', default=''),
    'client_secret': env.str('TH_REDDIT_CLIENT_SECRET', default=''),
    'user_agent': env.str('TH_REDDIT_USER_AGENT', default=''),
}

TH_PELICAN_AUTHOR = env.str('TH_PELICAN_AUTHOR', default='FoxMaSk')

# list of services that require the auth of the service
SERVICES_AUTH = ('ServiceEvernote', 'ServiceGithub', 'ServicePocket',
                 'ServicePushbullet', 'ServiceReddit', 'ServiceSlack',
                 'ServiceTaiga', 'ServiceTodoist', 'ServiceTrello',
                 'ServiceTumblr', 'ServiceTwitter',
                 )
# list of services that just use a token
SERVICES_WITH_TOKEN = ('ServiceInstapush',)

# list of services that require the auth (or not) of the service and are self hosted
SERVICES_HOSTED_WITH_AUTH = ('ServiceMastodon', 'ServiceWallabag',)

# list of services that require nothing
SERVICES_NEUTRAL = ('ServicePelican', 'ServiceRss',)
