from multiprocessing import AuthenticationError
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import PostForm_search_with_author
from .forms import PostForm_search_with_title
from django.shortcuts import redirect

import json
import requests
import re
import os
import pprint
import time
import urllib.error
import urllib.request

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
    if request.method == "POST":
        form = PostForm_search_with_author(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('search_result_with_author',author=post.author)
    else:
        form = PostForm_search_with_author()
    return render(request, 'blog/search_with_author.html', {'form': form})

def search_with_title(request):
    if request.method == "POST":
        form = PostForm_search_with_title(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('search_result_with_title',title=post.title)
    else:
        form = PostForm_search_with_title()
    return render(request, 'blog/search_with_title.html', {'form': form})

def search_result_with_author(request,author):
    title = use_googleAPI_author(author)
    params = {'author': author,'title': title }
    return render(request, 'blog/search_result_with_author.html', params)

def search_result_with_title(request,title):
    result = use_googleAPI_author(title)
    params = {'key' : title,'title' : result}
    return render(request, 'blog/search_result_with_title.html', params)

def use_googleAPI_author(author):
    REQUEST_URL_GOOGLE = 'https://www.googleapis.com/books/v1/volumes'

    search_params_GoogleBooksAPI = {
        "q"       : "inauthor: " + author,
        "sort"    : "newest"
    }

    i = 0
    response_GoogleBooksAPI = requests.get(REQUEST_URL_GOOGLE, search_params_GoogleBooksAPI)
    result = response_GoogleBooksAPI.json()

    totalItems = result["totalItems"]
    print("件数 : ",totalItems)
    if result["totalItems"] != 0:
        if ("items" in result) == False:
            items = "None"
        else:
            items = result["items"][i] #items

        if ('volumeInfo' in items) == False:
            info = "None"
        else:
            info = items['volumeInfo']

        if ("saleInfo" in items) == False:
            saleInfo = "None"
        else:
            saleInfo = items["saleInfo"]

        if ('title' in info) == False:
            title = "None"
        else:
            title = info['title']

        if ('authors' in info) == False:
            author = "None"
        else: 
            author = info['authors']

        if ("publisher" in info) == False:
            publisher = "None"
        else:
            publisher = info['publisher']

        if ('publishedDate' in info) == False:
            publisheddate = "None"
        else:
            publisheddate = info['publishedDate']

        if ('pageCount' in info) == False:
            pages = "None"
        else:
            pages = info['pageCount']

        if ('printType' in info) == False:
            info = "None"
        else:
            printtype = info['printType']

        if ('description' in info) == False:
            info = "None"
        else:
            description = info['description']

        if ('language' in info) == False:
            info = "None"
        else:
            language = info['language']

        if ("isEbook" in saleInfo) == False:
            info = "None"
        else:
            Ebook = saleInfo["isEbook"]

        return title

    else:
        return "NOT FOUND"

def use_googleAPI_title(author):
    REQUEST_URL_GOOGLE = 'https://www.googleapis.com/books/v1/volumes'

    search_params_GoogleBooksAPI = {
        "q"       : "intitle: " + author,
        "sort"    : "newest"
    }

    i = 0
    response_GoogleBooksAPI = requests.get(REQUEST_URL_GOOGLE, search_params_GoogleBooksAPI)
    result = response_GoogleBooksAPI.json()

    totalItems = result["totalItems"]
    print("件数 : ",totalItems)
    if result["totalItems"] != 0:
        if ("items" in result) == False:
            items = "None"
        else:
            items = result["items"][i] #items

        if ('volumeInfo' in items) == False:
            info = "None"
        else:
            info = items['volumeInfo']

        if ("saleInfo" in items) == False:
            saleInfo = "None"
        else:
            saleInfo = items["saleInfo"]

        if ('title' in info) == False:
            title = "None"
        else:
            title = info['title']

        if ('authors' in info) == False:
            author = "None"
        else: 
            author = info['authors']

        if ("publisher" in info) == False:
            publisher = "None"
        else:
            publisher = info['publisher']

        if ('publishedDate' in info) == False:
            publisheddate = "None"
        else:
            publisheddate = info['publishedDate']

        if ('pageCount' in info) == False:
            pages = "None"
        else:
            pages = info['pageCount']

        if ('printType' in info) == False:
            info = "None"
        else:
            printtype = info['printType']

        if ('description' in info) == False:
            info = "None"
        else:
            description = info['description']

        if ('language' in info) == False:
            info = "None"
        else:
            language = info['language']

        if ("isEbook" in saleInfo) == False:
            info = "None"
        else:
            Ebook = saleInfo["isEbook"]

        return title

    else:
        return "NOT FOUND"

