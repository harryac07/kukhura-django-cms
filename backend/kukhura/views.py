from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import json

from django.contrib.auth.models import User

from .models import Service, Product, Comment, BlogPost

from .serializers import UserSerializer, ServiceSerializer, ProductSerializer, BlogPostSerializer, CommentSerializer


class ServiceList(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print('customize post here')
        # s1 = json.dumps(self.request.data)
        # d2 = json.loads(s1)
        # print(d2)
        serializer.save(author=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         # 'users': reverse('user-list', request=request, format=format),
#         'services': reverse('service-list', request=request, format=format)
#     })
