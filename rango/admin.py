# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from rango.models import Category, Page
from rango.models import Algorithm, PDB, UserFollow

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

"""
This is where my stuff starts
"""

class AlgorithmAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('algorithm_name',)}
	list_display = ('algorithm_name', 'general_description', 'PDBFilesUsed')

class PDBAdmin(admin.ModelAdmin):
	list_display = ('pdb_iden', 'url')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(PDB, PDBAdmin)
admin.site.register(UserFollow)
