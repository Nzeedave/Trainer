# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('time', models.IntegerField(default=0)),
                ('target', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=128)),
                ('desc_long', models.CharField(max_length=512, blank=True)),
                ('comment', models.CharField(max_length=512, blank=True)),
                ('url', models.URLField(blank=True)),
                ('record', models.IntegerField(default=0)),
                ('time', models.IntegerField()),
                ('category', models.ForeignKey(to='guitar.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=512, blank=True)),
                ('time', models.IntegerField()),
                ('count', models.IntegerField()),
                ('date', models.DateField()),
                ('exercise', models.ForeignKey(to='guitar.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoutineItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order', models.IntegerField()),
                ('exercise', models.ForeignKey(to='guitar.Exercise')),
                ('routine', models.ForeignKey(to='guitar.Routine')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='routineitem',
            unique_together=set([('routine', 'order')]),
        ),
    ]
