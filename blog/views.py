from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm
from .models import Post, Category


# Create your views here.


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            t_str = title.lower()
            for i in range(0, len(t_str), 1):
                if (t_str[i] == ' '):
                    t_str = t_str.replace(t_str[i], '-')
            obj = form.save(commit=False)
            obj.author = request.user
            obj.slug = t_str
            obj.save()
            form.save_m2m()
            return HttpResponseRedirect('/blog/')
        else:
            print(form.errors)

    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, id, year, month, day, posts):
    post = get_object_or_404(Post, id=id, slug=posts,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'liked': liked
    })


@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:  # check whether the form is submitted,
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            # search_vector = SearchVector('title', 'body', 'categories')
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B') + SearchVector('categories', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                              rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank') # filter(search=search_query)
    return render(request, 'blog/post/search.html', {'form': form,
                                                         'query': query,
                                                         'results': results})

@login_required
def post_category(request, cats):
    category_posts = Post.objects.filter(categories=cats).order_by('-publish')
    return render(request, "blog/post/category_post_list.html", {'cats': cats, 'category_posts': category_posts})


@login_required
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-publish'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog/post/category_post_list.html", context)


def like_view(request, id, year, month, day, posts):
    liked = False

    if request.method == 'POST':
        post = get_object_or_404(Post, id=request.POST.get('post_id'),
                                 slug=posts,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

    return HttpResponseRedirect(reverse('blog:post_detail', args=[int(id), int(year), int(month), int(day), str(posts)]))

'''
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        tags = request.POST['tags']
        t_str = title.lower()
        for i in range(0, len(t_str), 1):
            if (t_str[i] == ' '):
                t_str = t_str.replace(t_str[i], '-')
        x = list(tags.split())
        last_x = x[-1]
        others = x[:-1]
        a = []
        for y in others:
            y.split()
            b = y[:-1]
            a.append(b)
        new_str = ','.join(a) + ',' + last_x

        add_post = Post(title=title, slug=t_str, body=body, tags=tags, author=request.user)
        add_post.save()
        # add_post.save_m2m()

        return HttpResponseRedirect('/blog/')

    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})

'''

'''
Search against a single field using the search QuerySet lookup,
like this:

from blog.models import Post
Post.objects.filter(body__search='django')

You might want to search against multiple fields. In this case, you will need to define
a SearchVector object. Let's build a vector that allows you to search against the
title and body fields of the Post model:

from django.contrib.postgres.search import SearchVector
from blog.models import Post
Post.objects.annotate(
search=SearchVector('title', 'body'),
).filter(search='django')
'''