Django Trigger Happy : HOWTO Services 
=========================

Read a complete RSS file :
----------------------------------------

Suppose you want to read a complete RSS file , then you will reach your goal with the following piece of code :


```python
from django_th.lib.feedsservice import Feeds

url = '/home/foxmask/django_th/lib/feedsservice/PyPI_Newest_Packages.rss'

for feeds in Feeds(url_to_parse=url).datas():	
	print "{0}: {1}".format(feeds.title, feeds.description)
		
```

Read a filtered RSS file :
-------------------------------------

Now suppose you want to read a RSS file but filtered with 2 criterias :

first one : You want all feeds that contain a given word
second one : You dont want the feeds that contain a given word

For example : 
You want feeds that speak about django but dont want the same feeds that contain the word 'UNKNOW'
Yes this happens very often on pipy :)


Here is a piece of code that handles both services :
---------------------------------------------------------------------------------

```python
from django_th.lib.feedsservice import Feeds
from django_th.lib.conditionchecker import Condition

url = '/home/foxmask/django_th/lib/feedsservice/PyPI_Newest_Packages.rss'
condition = {'match':'django', 'does_not_match':'UNKNOWN'}
filters = ('title','description')

for feeds in Feeds(url_to_parse=url).datas():
	for data in Condition(**condition).check(feeds,*filters):
		print "{0}: {1}".format(data.title, data.description)
		
```