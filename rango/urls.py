from django.conf.urls import url
from rango import views

urlpatterns = [
	url(r'^$', views.empty, name='rango-empty'),
	#The ^$ matches an empty string, any pattern supplied by the user will match this pattern, thus
	# will cause our application to always look into the views.index url request
	url(r'^index/$', views.index, name='rango-index'),
	url(r'^about/$', views.about, name='rango-about'),
	url(r'^main/$', views.main, name='rango-main'),
	url(r'^algorithm/(?P<algorithm_name_slug>[\w\-]+)/$', views.algorithm, name='isso-algorithm'),
	url(r'^pdb/(?P<pdb_name_slug>[\w\-]+)/$', views.pdb, name='isso-pdb'),
	url(r'profile/$', views.profile, name='isso-profile'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='rango-category'),
	url(r'^add_category/$', views.add_category, name='rango-add_category'),
	url(r'^add_pdb/$', views.add_pdb, name='isso-add_pdb'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='rango-add_page'),
	url(r'^search/$', views.search, name='search'),
	url(r'^follow_algorithm/$', views.follow_algorithm, name='follow_algorithm'),
	url(r'^update_alg_choice/$', views.update_alg_choice, name='update_alg_choice'),
	url(r'suggest_search/$', views.suggest_search, name='suggest_search'),
	url(r'submission/$', views.submission, name='isso-submission'),
	#url(r'^register/$', views.register, name='isso-register'),
	#url(r'^registerOne/$', views.register, name='isso-registerOne'),
	#url(r'^login/$', views.user_login, name='isso-login'),
	#url(r'^logout/$', views.user_logout, name='isso-logout'),
]

