from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from kukhura import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'blogposts', views.BlogPostViewSet, basename='blogposts')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'users', views.UserViewSet, basename='users')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('authenticate/', views.CustomObtainAuthToken.as_view()),
]
