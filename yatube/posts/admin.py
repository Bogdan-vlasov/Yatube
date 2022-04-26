from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('description',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "created", "text", "author")
    search_fields = ("text", "author")
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
