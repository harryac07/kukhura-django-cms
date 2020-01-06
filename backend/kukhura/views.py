from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from rest_framework.response import Response

import json
import cloudinary
import cloudinary.uploader
import cloudinary.api

# cloudinary.config(
#   cloud_name = "sample",
#   api_key = "874837483274837",
#   api_secret = "a676b67565c6767a6767d6767f676fe1"
# )

from django.contrib.auth.models import User

from .models import Product, Comment, Post, Category

from .serializers import UserSerializer, ProductSerializer, BlogPostSerializer, CommentSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(
                category=Category.objects.get(name=category)
            )
        return queryset

    def perform_create(self, serializer):
        # s1 = json.dumps(self.request.data)
        # d2 = json.loads(s1)
        # print(d2)
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        group = user.groups.values_list('name', flat=True)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'group': group
        })
