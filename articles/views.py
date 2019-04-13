from django.http import HttpResponseRedirect,HttpResponse ,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,Comment,Category

from django.urls import reverse
from django.db.models import Q
from .forms import *
from django.contrib.auth.decorators import login_required
from .import forms
from .forms import CommentForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import RedirectView
from django.template.loader import render_to_string
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def article_list(request,tag_slug=None):
    article_list = Article.objects.all().filter(status="PUBLISHED")
    query= request.GET.get("q")
    categories=Category.objects.all()

    tag=None
    if query:
        article_list=article_list.filter(
        Q(title__icontains=query)|
        Q(author__username=query)|
        Q(body__icontains=query)
        ).distinct()
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        article_list=article_list.filter(tags__in=[tag],status="PUBLISHED")

    paginator = Paginator(article_list, 7)
    page =request.GET.get('page')
    try:
        articles=paginator.get_page(page)
    except PageNotInteger:
        articles=paginator.get_page(1)
    except EmptyPage:
        articles=paginator.get_page(paginator.num_pages)

    return render(request,'articles/article_list.html',{'articles':articles,'tag':tag,'categories':categories})

def article_details(request,slug):
    post=get_object_or_404(Article,slug=slug)
    categories=Category.objects.all()
    tag=Tag.objects.all()
    comments=Comment.objects.filter(post=post,reply= None)
    is_liked = False
    if post.likes.filter(id =request.user.id).exists():
        is_liked = True
    comment_form = CommentForm( )
    comment_qs =None

    post_tags_ids = post.tags.values_list('id', flat=True)

    similar_posts = Article.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:6]
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None )

        if comment_form.is_valid():
            content=request.POST.get('content')
            reply_id =request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs=Comment.objects.get(id=reply_id)

            comment=Comment.objects.create(post=post,user=request.user,content=content,reply=comment_qs)

            comment.save()
            print(comment)
            #comment_form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form =CommentForm()
    return render(request,'articles/article_details.html',{'post_tags_ids':post_tags_ids,'articles':post,'tag': tag, 'categories':categories,'post':post,'comments':comments,'similar_posts':similar_posts,'comment_form':comment_form,'reply':comment_qs,'is_liked':is_liked,'total_likes':post.total_likes(),})

def like_post(request):
    post=get_object_or_404(Article,id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request. user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


    #return HttpResponseRedirect(post.get_absolute_url())


@login_required(login_url="/accounts/login")
def article_create(request):
    if request.method=='POST':
        form = forms.CreateArticle(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.author=request.user
            instance.save()
            return redirect('articles:list')
    else:
        form =forms.CreateArticle()
    return render(request,'articles/article_create.html',{'form':form})


def show_category(request,slug):
    categories=Category.objects.all()
    posts=Article.objects.all().filter(status="PUBLISHED")
    if slug:
        category=get_object_or_404(Category,slug=slug)
        posts=posts.filter(category=category)
    paginator = Paginator(posts, 6)
    page =request.GET.get('page')
    try:
        posts=paginator.get_page(page)
    except PageNotInteger:
        posts=paginator.get_page(1)
    except EmptyPage:
        posts=paginator.get_page(paginator.num_pages)

    return render(request,'articles/category.html',{'posts':posts,'category':category,'categories':categories,})
