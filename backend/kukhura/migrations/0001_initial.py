# Generated by Django 2.1.2 on 2020-01-05 10:24

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('primary_image', models.TextField()),
                ('secondary_images', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(help_text='optional images to show if needed'), size=None)),
                ('hero_post', models.BooleanField(default=False, help_text='Is it to be placed on top of the service page? default to false')),
                ('created', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('updated', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kukhura.Post')),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=('kukhura.post',),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='kukhura.Category'),
        ),
        migrations.AddField(
            model_name='comment',
            name='blogpost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='kukhura.Post'),
        ),
    ]
