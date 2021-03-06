# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 06:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('algorithm_name', models.CharField(max_length=128, unique=True)),
                ('general_description', models.TextField()),
                ('PDBFilesUsed', models.IntegerField(default=0)),
                ('followers', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlgorithmDetail',
            fields=[
                ('adid', models.AutoField(primary_key=True, serialize=False)),
                ('sheet_iden', models.CharField(max_length=4)),
                ('test_set', models.BooleanField(default=False)),
                ('example', models.BooleanField(default=False)),
                ('algorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rango.Algorithm')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rango.Category')),
            ],
        ),
        migrations.CreateModel(
            name='PDB',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('pdb_iden', models.CharField(max_length=4)),
                ('url', models.URLField()),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.IntegerField(default=0)),
                ('following', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='algorithmdetail',
            name='pdb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rango.PDB'),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='pdb',
            field=models.ManyToManyField(through='rango.AlgorithmDetail', to='rango.PDB'),
        ),
    ]
