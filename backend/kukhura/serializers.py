from rest_framework import serializers
import json
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group

from .models import Product, Comment, CommentReply, Post, Category
from .helpers.blog_post import unset_existing_hero_post_if_user_want_to_set_new

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
        unset_existing_hero_post_if_user_want_to_set_new(validated_data, Post)

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
        unset_existing_hero_post_if_user_want_to_set_new(validated_data, Post)
        # remove comments property from validated_data
        validated_data.pop('comments')
        return super(BlogPostSerializer, self).update(instance, validated_data)


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

    def create(self, validated_data):
        unset_existing_hero_post_if_user_want_to_set_new(validated_data, Product)
        blogpost = Product.objects.create(**validated_data)
        return blogpost

    def update(self, instance, validated_data):
        unset_existing_hero_post_if_user_want_to_set_new(validated_data, Product)
        return super(ProductSerializer, self).update(instance, validated_data)