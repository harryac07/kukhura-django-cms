from django.contrib import admin
from kukhura.models import Service, BlogPost, Product, Comment


class ServiceAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'service_primary_image', 'hero_service')
    list_display = ('title', 'description',
                    'service_primary_image', 'hero_service')


class BlogPostAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'post_primary_image',
              'author', 'created', 'hero_post')
    list_display = ('title', 'description', 'post_primary_image',
                    'author', 'hero_post', 'created')


admin.site.register(Service, ServiceAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Product)
admin.site.register(Comment)
