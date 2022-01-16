from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import PostForm_search_with_author
from .forms import PostForm_search_with_title
from django.shortcuts import redirect

def top_page(request):
    return render(request, 'blog/top_page.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def search(request):
    return render(request, 'blog/search.html')

def search_with_author(request):
    form = PostForm_search_with_author()
    return render(request, 'blog/search_with_author.html', {'form': form})

def search_with_title(request):
    form = PostForm_search_with_title()
    return render(request, 'blog/search_with_title.html', {'form': form})

def search_result_with_author(request):
    return render(request, 'blog/search_result_with_author.html')

def search_result_with_title(request):
    return render(request, 'blog/search_result_with_title.html')
