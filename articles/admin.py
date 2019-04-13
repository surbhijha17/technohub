from django.contrib import admin
from .models import Article
from .models import Comment
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
	list_display=('name',)
	prepopulated_fields= {'slug':('name',)}




admin.site.register(Category , CategoryAdmin)
#


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','date','category','status')
    list_filter = ('date', 'author')
    search_fields = ('title','body')
    prepopulated_fields= {'slug':('title',)}
    raw_id_fields = ('author',)
admin.site.register(Article, ArticleAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display =('user','post','content','timestamp',)
    list_filter = ( 'user','timestamp',)
    search_fields = ('post','timestamp')
admin.site.register(Comment, CommentAdmin)


# Register your models here.
