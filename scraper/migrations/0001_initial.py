# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 14:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import scraper.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('get_image', models.BooleanField(default=True, help_text=b'Download images found inside extracted content')),
                ('replace_rules', jsonfield.fields.JSONField(default=dict, help_text=b'List of Regex rules will be applied to refine data')),
                ('black_words', models.CharField(blank=True, max_length=256, null=True)),
            ],
            bases=(scraper.base.ExtractorMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LocalContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('local_path', models.CharField(max_length=256)),
                ('created_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProxyServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Proxy Server Name')),
                ('address', models.CharField(max_length=128, verbose_name='Address')),
                ('port', models.IntegerField(verbose_name='Port')),
                ('protocol', models.CharField(choices=[(b'http', b'HTTP'), (b'https', b'HTTPS')], max_length=16, verbose_name='Protocol')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(blank=True, max_length=64, null=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('other', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraper.LocalContent')),
            ],
        ),
        migrations.CreateModel(
            name='Selector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField()),
                ('xpath', models.CharField(max_length=512)),
                ('data_type', models.CharField(choices=[(b'text', b'Text content'), (b'html', b'HTML content'), (b'binary', b'Binary content')], max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text=b'URL of         the starting page', max_length=256, verbose_name='Start URL')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('crawl_root', models.BooleanField(default=False, verbose_name='Extract data from starting page')),
                ('target_links', jsonfield.fields.JSONField(default=dict, help_text=b'XPaths toward links to pages with content         to be extracted')),
                ('expand_links', jsonfield.fields.JSONField(default=dict, help_text=b'List of links (as XPaths) to other pages         holding target links (will not be extracted)')),
                ('crawl_depth', models.PositiveIntegerField(default=1, help_text=b'Set this > 1         in case of crawling from this page')),
                ('collectors', models.ManyToManyField(blank=True, related_name='spider', to='scraper.Collector')),
                ('proxy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scraper.ProxyServer')),
            ],
            options={
                'abstract': False,
            },
            bases=(scraper.base.ExtractorMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='UA Name')),
                ('value', models.CharField(max_length=256, verbose_name='User Agent String')),
            ],
        ),
        migrations.AddField(
            model_name='spider',
            name='user_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scraper.UserAgent'),
        ),
        migrations.AddField(
            model_name='collector',
            name='selectors',
            field=models.ManyToManyField(blank=True, to='scraper.Selector'),
        ),
    ]