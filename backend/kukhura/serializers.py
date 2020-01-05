from rest_framework import serializers
import json
from django.contrib.auth.models import User, Group

from .models import Product, Comment, Post, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['email', 'comment', 'created']


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


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_category = CategorySerializer(source='category', read_only=True)
    category = serializers.ChoiceField(
        choices=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'primary_image', 'author', 'category', 'post_category',
                  'secondary_images', 'hero_post', 'available', 'created']
