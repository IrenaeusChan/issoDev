# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)	#A field for storing character data
								#max_length is how many chars
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	def __unicode__(self):		#Unique is set to True so that each name must be unique
		return self.name	#can also use default='value' and null=True

class Page(models.Model):
	category = models.ForeignKey(Category)		#Creates a one-to-many relationship
	title = models.CharField(max_length=128)
	url = models.URLField()				#Stores resource URLs, can specify max_length
	views = models.IntegerField(default=0)		#Stores Integers
							#Can use DateField for Datetime.date
	def __unicode__(self):
		return self.title

#This is where everything involving my code starts...

"""
We already know that the default USER in django.contrib.auth.models have:
	- Username
	- Password
	- Email
	- First and Last Name
This class is for the additional attributes:
	- Followers
	- Following
""" 
class UserFollow(models.Model):
	user = models.OneToOneField(User)	#We have to link it to the base USER

	#Attributes to include
	followers = models.IntegerField(default=0)
	following = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username

class PDB(models.Model):
	pid = models.AutoField(primary_key=True)	#Primary Key
	pdb_iden = models.CharField(max_length=4)	#The identifier
	url = models.URLField()				#Used to reference PDB Website
	slug = models.SlugField()			#Unique Names

	def save(self, *args, **kwargs):
		self.slug = slugify(self.pdb_iden)
		super(PDB, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.pdb_iden			#So we know what our model is

def content_file_name(instance, filename):
	return '/'.join(['content',instance.author.username, filename])

class Algorithm(models.Model):
	aid = models.AutoField(primary_key=True)
	pdb = models.ManyToManyField(PDB, through='AlgorithmDetail')	#This is how to make an relation entity
	author = models.ForeignKey(settings.AUTH_USER_MODEL)				#Still needs to be done
	algorithm_name = models.CharField(max_length=128, unique=True)
	general_description = models.CharField(max_length=500, blank=True)
	filePath = models.FileField( upload_to=content_file_name)	#This needs to be done as well
	PDBFilesUsed = models.IntegerField(default=0)
	followers = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug=slugify(self.algorithm_name)
		super(Algorithm, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.algorithm_name

class AlgorithmDetail(models.Model):
	adid = models.AutoField(primary_key=True)
	algorithm = models.ForeignKey(Algorithm)
	pdb = models.ForeignKey(PDB)
	sheet_iden = models.CharField(max_length=4)
	test_set = models.BooleanField(default=False)
	example = models.BooleanField(default=False)

	def __unicode__(self):
		return self.algorithm.algorithm_name + ' ' + self.pdb.pdb_iden

"""
Still left to do is the POST and AlgorithmStream
The AlgorithmStream is connected to the Algorithm in a 1 to 1 relation
A POST is a standalone Entitiy. Each User can make a post.
The Post is connected to the Algorithm however.
Will figure this out later.
"""
