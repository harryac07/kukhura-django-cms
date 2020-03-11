from ..models import Product, Comment, CommentReply, Post, Category

def unset_existing_hero_post_if_user_want_to_set_new(validated_data, modelObject):
    if validated_data['hero_post'] == True:
        category = validated_data['category']
        modelObject.objects.filter(
            hero_post=True, category=category).update(hero_post=False)