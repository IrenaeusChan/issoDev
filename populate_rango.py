import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
	pythonCategory = addCategory('Python',
		views=128,
		likes=64)

	addPage(cat=pythonCategory,
		title="Official Python Tutorial",
		url="http://docs.python.org/2/tutorial/")

	addPage(cat=pythonCategory,
		title="How to Think like a Computer Scientist",
		url="http://www.greenteapress.com/thinkpython/")

	addPage(cat=pythonCategory,
 		title="Learn Python in 10 Minutes",
		url="http://www.korokithakis.net/tutorials/python/")

    	djangoCategory = addCategory("Django",
		views=64,
		likes=32)

    	addPage(cat=djangoCategory,
        	title="Official Django Tutorial",
        	url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    	addPage(cat=djangoCategory,
        	title="Django Rocks",
        	url="http://www.djangorocks.com/")

    	addPage(cat=djangoCategory,
        	title="How to Tango with Django",
        	url="http://www.tangowithdjango.com/")

    	frameCategory = addCategory("Other Frameworks",
		views=32,
		likes=16)

    	addPage(cat=frameCategory,
        	title="Bottle",
        	url="http://bottlepy.org/docs/dev/")

    	addPage(cat=frameCategory,
        	title="Flask",
        	url="http://flask.pocoo.org")

    	# Print out what we have added to the user.
    	for c in Category.objects.all():
        	for p in Page.objects.filter(category=c):
            		print "- {0} - {1}".format(str(c), str(p))

def addPage(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	"""
	The get_or_create() method checks to see if the entry already exists in the database. If it doesn't
	 exist, then the function creates the model for us. it returns (object, created) in which the object
	 is the object Page. If it exists it'll just return the model instance. Created is a boolean value
	 that is used to show if the model is created or not.
	"""
	p.url=url
	p.views=views
	p.save()
	return p

def addCategory(name, views, likes):
	c = Category.objects.get_or_create(name=name)[0]
	c.views=views
	c.likes=likes
	c.save()
	return c

# Start execution here!
if __name__ == '__main__':
	print "Starting Rango population script..."
	populate()
