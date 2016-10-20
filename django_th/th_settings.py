DJANGO_TH = {
    # paginating
    'paginate_by': 5,

    # this permits to avoid "flood" effect when publishing
    # to the target service - when limit is reached
    # the cache is kept until next time
    # set it to 0 to drop that limit
    'publishing_limit': 5,
    # number of process to spawn from multiprocessing.Pool
    'processes': 5,
    'services_wo_cache': ['th_instapush', ],
}

TH_SERVICES = (
    # uncomment the lines to enable the service you need
    # 'th_evernote.my_evernote.ServiceEvernote',
    # 'th_github.my_github.ServiceGithub',
    # 'th_instapush.my_instapush.ServiceInstapush',
    # 'th_pelican.my_pelican.ServicePelican',
    # 'th_pocket.my_pocket.ServicePocket',
    # 'th_pushbullet.my_pushbullet.ServicePushbullet',
    'th_rss.my_rss.ServiceRss',
    # 'th_todoist.my_todoist.ServiceTodoist',
    # 'th_trello.my_trello.ServiceTrello',
    # 'th_twitter.my_twitter.ServiceTwitter',
    'th_wallabag.my_wallabag.ServiceWallabag',
)


TH_EVERNOTE = {
    # get your credential by subscribing to http://dev.evernote.com/
    # for testing purpose set sandbox to True
    # for production purpose set sandbox to False
    'sandbox': False,
    'consumer_key': '<your evernote key>',
    'consumer_secret': '<your evernote secret>',
}


TH_GITHUB = {
    'username': 'username',
    'password': 'password',
    'consumer_key': 'my key',
    'consumer_secret': 'my secret'
}


TH_POCKET = {
    # get your credential by subscribing to http://getpocket.com/developer/
    'consumer_key': '<your pocket key>',
}

TH_PUSHBULLET = {
    'client_id': '<your pushbullet key>',
    'client_secret': '<your pushbullet secret>',
}

TH_TODOIST = {
    'client_id': '<your todoist key>',
    'client_secret': '<your todoist secret>',
}

TH_TRELLO = {
    'consumer_key': '<your trello key>',
    'consumer_secret': '<your trello secret>',
}

TH_TWITTER = {
    # get your credential by subscribing to
    # https://dev.twitter.com/
    'consumer_key': '<your twitter key>',
    'consumer_secret': '<your twitter secret>',
}
