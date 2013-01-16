import re
from django import template
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

register = template.Library()
current_site = Site.objects.get_current()


def proto(is_secure):
    """
    check if the url is secure or not and return
    the corresponding string
    """
    if is_secure:
        return "https://"
    else:
        return "http://"


@register.filter
def hash2href(input_string, request):
    """
    deal with hastag and transform to an anchor
    """
    # Create a dictionary holding all the tags and users we find in the input string
    return_dict = {'tags': re.findall('(?:(?<=\s)|^)#(\w*[A-Za-z_]+\w*)', input_string),
                  'users': re.findall('(?:(?<=\s)|^)@(\w*[A-Za-z_]+\w*)', input_string)}

    # Cycle through the tags and make all the hashtags links to twitter
    for tag in return_dict['tags']:
        url = ''.join([proto(request.is_secure()) +
                       request.META['HTTP_HOST'], "/hsearch/%23", tag])
        this_tag = {'tag': tag,
                   'hashtag': '#%s' % tag,
                   'url': url}
        input_string = re.sub(this_tag['hashtag'],
                            '<a href="%(url)s" class="hashtag">%(hashtag)s</a>'
                            % this_tag, input_string)

    # Cycle through the users and make them all link to twitter
    for user in return_dict['users']:
        url = ''.join([proto(request.is_secure()) +
                       request.META['HTTP_HOST'], user]) 
        this_user = {'user': user,
                    'atted': '@%s' % user,
                    'url': url}
        input_string = re.sub(this_user['atted'],
                        '<a href="%(url)s" class="twitteruser">%(atted)s</a>'
                        % this_user, input_string)

    # Store the changed string and then return all tags,
    # users and the new string
    return_dict['output'] = input_string
    return mark_safe(return_dict['output'])


@register.simple_tag
def active(request, pattern):
    """
    check the current url to add a CSS class "active"
    """
    active_css_class = ' class="active" '
    pattern = "^%s$" % pattern
#    if re.search('^/relationships/\w+/follow(ers|ing)/$', pattern):
#        return active_css_class
#    elif re.search(pattern, request.path):
    if re.search(pattern, request.path):
        return active_css_class
    elif re.search('^/histo/$', request.path) and pattern == '^/$':
        return active_css_class
    elif re.search('^/profiles/edit/$', request.path) and re.search('profiles', pattern):
        return active_css_class
    return ''
