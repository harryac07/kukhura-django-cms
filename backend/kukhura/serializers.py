from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Service, Product, Comment, BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'service_primary_image',
                  'service_secondary_images', 'hero_service', 'created']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'product_primary_image',
                  'product_secondary_images', 'hero_product', 'available', 'created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['email', 'comment', 'created']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'description', 'post_primary_image',
                  'author', 'hero_post', 'created', 'updated', 'comments']

    def create(self, validated_data):
        if 'comments' not in validated_data:
            validated_data['comments'] = []
        else:
            pass
        # remove comments property from validated_data
        comment_validated_data = validated_data.pop('comments')

        # add blogpost without comments object
        blogpost = BlogPost.objects.create(**validated_data)

        # add blogpost value to each comment
        # create all available comments
        for each in comment_validated_data:
            each['blogpost'] = blogpost
            Comment.objects.create(**each)
        return blogpost
