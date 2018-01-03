# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from rango.models import Category, Page
from rango.models import Algorithm, PDB
from rango.forms import CategoryForm, PageForm, UserForm, UserFollowForm
from rango.forms import PDBForm, AlgorithmForm

from datetime import datetime

import json
import sys, os, subprocess
sys.path.append(os.path.realpath("library"))
import protein, sheet, runAlg

#Create your views here

def empty(request):
	return HttpResponse("HelloWorld!! This application is actually  working!")

def main(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'boldmessage' : "I am bold font from the context",
			'categories' : category_list,
			'pages' : page_list,
			}
	return render(request, 'main.html', context_dict)

def about(request):
	return HttpResponse("This is the about page " + '<a href="/rango/index/">MAIN INDEX</a>' )

def index(request):
	PDBList = PDB.objects.all()[:5]
	algorithmList = Algorithm.objects.all()[:5]
	context_dict = {'algorithms' : algorithmList,
			'pdb' : PDBList,
			}
	#COOKIES.get() function gets the visits cookie
	# if the cookie exists, the value is casted into an integer
	# else it will be defaulted to zero and cast that instead
	#visits = int(request.COOKIES.get('visits', '1'))
	visits = request.session.get('visits')		#Safer to do everything however server side
	if not visits: visits = 1
	#context_dict['visits'] = visits
	reset_last_visit_time = False
	#response = render(request, 'index.html', context_dict)
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).seconds > 0:
			visits = visits + 1
			reset_last_visit_time = True
	else: reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits	

	"""
	#Does the cookie last_visit exist?
	if 'last_visit' in request.COOKIES:
		last_visit = request.COOKIES['last_visit']
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).days > 0:
			visits = visits + 1
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True
		context_dict['visits'] = visits
		response = render(request, 'index.html', context_dict)
	if reset_last_visit_time:
		response.set_cookie('last_visit', datetime.now())
		response.set_cookie('visits', visits)
	"""
	print context_dict['visits'] 
	return render(request, 'index.html', context_dict)

@login_required
def algorithm(request, algorithm_name_slug):
	context_dict = {}
	try:
		algorithm = Algorithm.objects.get(slug=algorithm_name_slug)
		context_dict['algorithm_name'] = algorithm.algorithm_name
		context_dict['algorithm_author'] = algorithm.author
		context_dict['gd'] = algorithm.general_description
		pdbfiles = algorithm.pdb.all()
		context_dict['pdbfiles'] = pdbfiles
		context_dict['algorithm'] = algorithm
		context_dict['PDBFilesUsed'] = algorithm.PDBFilesUsed
		context_dict['algorithm_name_slug'] = algorithm_name_slug
	except Algorithm.DoesNotExist:
		pass
	return render(request, 'algorithm.html', context_dict)

def pdb(request, pdb_name_slug):
	context_dict, sheetDict = {}, {}
	sheetList, algList = [], []
	try:
		pdb = PDB.objects.get(slug=pdb_name_slug)
		context_dict['pdb_iden'] = pdb.pdb_iden

		url_target = "https://www.rcsb.org/pdb/files/{0}.pdb".format(pdb.pdb_iden)
		p = protein.buildProtein(url_target)
		sheetList += sheet.buildSheet(url_target, p, pdb.pdb_iden)

		algorithms = pdb.algorithmdetail_set.all()
		
		for s in sheetList:
			for alg in algorithms:
				if str(s.sheetIden.replace(" ", "")) == alg.sheet_iden:
					algList.append(alg.algorithm)
				else:
					algList.append("No matching algorithms.")
					break
			sheetDict[str(s.sheetIden.replace(" ", ""))] = algList
			algList = []
	
		context_dict['sheetAlg'] = sheetDict
		context_dict['algorithms'] = algorithms
		context_dict['pdb'] = pdb
		context_dict['pdb_name_slug'] = pdb_name_slug
	except PDB.DoesNotExist:
		pass
	return render(request, 'pdb.html', context_dict)

@login_required
def profile(request):
	context_dict = {}
	try:
		user = request.user
		algorithms = request.user.algorithm_set.all()
		context_dict['algorithms'] = algorithms
		context_dict['userName'] = user.username
		context_dict['user'] = user
	except User.DoesNotExist:
		pass
	return render(request, 'profile.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	try:
	#Can we find a category name slug with a given name?
	#If we can't, the .get() method raises a DoseNotExist Exception.
	#So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name

	#Retrieve all of the associated pages.
	#Note that filter returns >= 1 model instance.
		pages=Page.objects.filter(category=category)

	#Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
	#We also add the category object from the database to the context dictionary
	#We'll use this in the template to verify that the category exists
		context_dict['category'] = category
		context_dict['category_name_slug'] = category_name_slug
	except Category.DoesNotExist:
	#Get here if we didn't find the specified category
	#Don't do anything - the template displays the "no category" message for us
		pass
	return render(request, 'category.html', context_dict)

def add_pdb(request):
	if request.method == 'POST':
		form = PDBForm(request.POST)	#Load up the form
		if form.is_valid():		#If the information is filled correctly
			#form.save(commit=False)	#Save the informationi
			data = form.cleaned_data	
			for pdb_iden in [x.strip() for x in data['pdb_list'].split(',')]:
				p = PDB.objects.get_or_create(pdb_iden=pdb_iden)[0]
				p.url = "http://www.rcsb.org/pdb/explore.do?structureId={0}".format(pdb_iden)
				p.save()

			return index(request)	#Return to the index page
		else:
			print form.errors	#If there is an error, inform user
	else:
		form = PDBForm()		#For whatever reason if it can't load...

	return render(request, 'add_pdb.html', {'form': form})	#Still tell the user

@login_required
def submission(request):
	if request.method == 'POST':
		algForm = AlgorithmForm(request.POST,request.FILES)
		pdbForm = PDBForm(request.POST)
		
		if algForm.is_valid() and pdbForm.is_valid():	
			data = pdbForm.cleaned_data
			pdbList = [x.strip() for x in data['pdb_list'].split(',')]
			a = algForm.save(commit=False)	#For some reason adding this s worked...
			a.author = request.user
			a.PDBFilesUsed = len(pdbList)
			a.save()
			
			"""
			[
			["Example_PDB", "A"],
			["Example_Two", "B"],
			["Example_Three", "C"]
			]
			"""
			example_information = [[data['exampleOnePDBIden'], data['exampleOneSheetIden']], [data['exampleTwoPDBIden'], data['exampleTwoSheetIden']], [data['exampleThreePDBIden'], data['exampleThreeSheetIden']]]

			for pdb_iden in pdbList:
				p = PDB.objects.get_or_create(pdb_iden=pdb_iden)[0]
				p.url = "http://www.rcsb.org/pdb/explore.do?structureId={0}".format(pdb_iden)
				p.save()

			#This is where we calculate the Algorithm
			if runAlg.testAlgorithm(a):
				PDBList = PDB.objects.all()	#Get the list of all PDB files in the Server
				subprocess.Popen(runAlg.runAlgorithm(a, PDBList, pdbList, example_information))
			else:
				print "Improper File Format"	
			
			return profile(request)
		else:
			print algForm.errors
			print pdbForm.errors
	else:
		algForm = AlgorithmForm()
		pdbForm = PDBForm()
	return render(request, 'submit_algorithm.html', {'algForm':algForm, 'pdbForm':pdbForm})

def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.	
			form.save(commit=True)

			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'add_category.html', {'form': form})

def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {'form':form, 'category': cat}
	return render(request, 'add_page.html', context_dict)

def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = 'HelloWorld'
	return render(request, 'search.html', {'result_list': result_list})

@login_required
def follow_algorithm(request):
	algorithmNameSlug = None
	if request.method == 'GET':
		algorithmNameSlug = request.GET['algorithmNameSlug']

	followers = 0
	if algorithmNameSlug:
		algorithm = Algorithm.objects.get(slug=algorithmNameSlug)
		if algorithm:
			followers = algorithm.followers + 1
			algorithm.followers = followers
			algorithm.save()
	return HttpResponse(followers)

def update_alg_choice(request):
	context_dict = {}
	algorithmName = None
	if request.method == 'GET':
		algorithmName = request.GET['algorithmName']
	followers = 0
	if algorithmName:
		algorithm = Algorithm.objects.get(algorithm_name=algorithmName)
		if algorithm:
			followers = algorithm.followers
			algorithm.save()
	context_dict['followers'] = followers
	context_dict['algSlug'] = algorithm.slug
	context_dict['algName'] = algorithm.algorithm_name

	return HttpResponse(json.dumps(context_dict))

def get_pdb_or_algorithm_list(max_results=0, starts_with=''):
	pdb_list = []
	algorithm_list = []
	combined_list = []
	if starts_with:
		pdb_list = PDB.objects.filter(pdb_iden__startswith=starts_with)
		algorithm_list = Algorithm.objects.filter(algorithm_name__startswith=starts_with)

	if pdb_list and max_results > 0:
		if pdb_list.count() > max_results:
			pdb_list = pdb_list[:max_results]
			combined_list.append(pdb_list)

	if algorithm_list and max_results > 0:
		if algorithm_list.count() > max_results:
			algorithm_list = algorithm_list[:max_results]
			combined_list.append(algorithm_list)

	return combined_list

def suggest_search(request):
	combined_list = []
	starts_with= ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
	combined_list = get_pdb_or_algorithm_list(8, starts_with)
	return render(request, 'search.html', {'combined_list': combined_list })
"""
def register_profile(request, user):
	registered = False
	if request.method == 'POST':
		user_follow_form = UserFollowForm(data=request.POST)
		if user_follow_form.is_valid():
			#Since we created this ourselves, the commit = False let's us delay
			# model saving until we are ready to avoid integrity problems
			user_follow = user_follow_form.save(commit=False)
			user_follow.user = user
			user_follow.save()

			registered = True
		else:
			print user_follow_form.errors
	else:
		user_follow_form = UserFollowForm()

	return render(request, 'registration_formOne.html', 
			{'user_follow_form': user_follow_form, 
			'registered' : registered})"""
"""
def user_login(request):
	if request.method == 'POST':
	#Gather the username and password provided by the user.
	#This information is obtained from the login form.
		#Use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
		#because the request.POST.get('<variable>') returns None, if the value does not exist,
		#while the request.POST['<variable>'] will raise key error exception
		username = request.POST.get('username')
		password = request.POST.get('password')

		#Use Django's machinery to attempt to see if the username/password
		#combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:	#Check if the account is valid and active
				login(request, user)
				return HttpResponseRedirect('/rango/index/')
			else:
				return HttpResponseRedirect('Your Account is disabled.')
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse('Invalid login details supplied.')
	else:
		return render(request, 'login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/index/')"""
