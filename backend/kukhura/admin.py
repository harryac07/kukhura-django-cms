from django.contrib import admin
from kukhura.models import Post, Product, Comment, Category


class BlogPostAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'primary_image', 'secondary_images', 'category',
              'author', 'created', 'hero_post')
    list_display = ('title', 'description', 'primary_image', 'category',
                    'author', 'created', 'hero_post')


class ProductAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'primary_image', 'secondary_images',
              'author', 'created', 'hero_post', 'available')
    list_display = ('title', 'description', 'primary_image',
                    'author', 'created', 'hero_post', 'available')


admin.site.register(Post, BlogPostAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Comment)
