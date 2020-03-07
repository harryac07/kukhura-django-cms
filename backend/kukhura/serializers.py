from rest_framework import serializers
import json
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group

from .models import Product, Comment, CommentReply, Post, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created']


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ['email', 'reply', 'created', 'id', 'comment']


class CommentSerializer(serializers.ModelSerializer):
    reply = CommentReplySerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['email', 'comment', 'created', 'blogpost', 'id', 'reply']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, required=False)
    post_category = CategorySerializer(source='category', read_only=True)
    category = serializers.ChoiceField(
        choices=Category.objects.all(), write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'primary_image', 'secondary_images',
                  'author', 'hero_post', 'created', 'updated', 'comments', 'category', 'post_category']

    def create(self, validated_data):
        if 'comments' not in validated_data:
            validated_data['comments'] = []
        else:
            pass
        # if post is set to hero, remove other and set this to hero_post
        if validated_data['hero_post'] == True:
            category = validated_data['category']
            Post.objects.filter(
                hero_post=True, category=category).update(hero_post=False)

        # remove comments property from validated_data
        comment_validated_data = validated_data.pop('comments')

        # add blogpost without comments object
        blogpost = Post.objects.create(**validated_data)

        # add blogpost value to each comment
        # create all available comments
        for each in comment_validated_data:
            each['blogpost'] = blogpost
            Comment.objects.create(**each)
        return blogpost

    def update(self, instance, validated_data):
        if 'comments' not in validated_data:
            validated_data['comments'] = []
        else:
            pass

        # if post is set to hero, remove other and set this to hero_post
        category = validated_data['category']
        if validated_data['hero_post'] == True:
            Post.objects.filter(
                hero_post=True, category=category).update(hero_post=False)
        else:
            print('hero_post False')

        # remove comments property from validated_data
        comment_validated_data = validated_data.pop('comments')

        # update blogpost
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.primary_image = validated_data.get(
            'primary_image', instance.primary_image)
        instance.secondary_images = validated_data.get(
            'secondary_images', instance.secondary_images)
        instance.hero_post = validated_data.get(
            'hero_post', instance.hero_post)
        instance.category = validated_data.get('category', instance.category)
        instance.updated = datetime.datetime.now(tz=timezone.utc)
        instance.save()

        # add blogpost value to each comment
        # create all available comments
        for each in comment_validated_data:
            print(dict(each)['email'])
            print(dict(each))
            # Comment.objects.filter(
            # id=True, category=category).update(hero_post=False)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_category = CategorySerializer(source='category', read_only=True)
    comments = CommentSerializer(many=True, required=False)
    category = serializers.ChoiceField(
        choices=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'primary_image', 'author', 'category', 'post_category',
                  'secondary_images', 'hero_post', 'available', 'comments', 'created']
