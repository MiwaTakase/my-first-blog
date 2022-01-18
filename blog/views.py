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
    results = use_googleAPI(author,"author")
    params = {
        'author': author,
        'results': results,
    }
    return render(request, 'blog/search_result_with_author.html', params)

def search_result_with_title(request,title):
    results = use_googleAPI(title,"title")
    params = {
        'author': title,
        'results': results,
    }
    return render(request, 'blog/search_result_with_title.html', params)

def search_result_with_title_rakuten(request,title):
    results,totalItems = use_rakutenBooksAPI(title)
    print("in rakuten API",title)
    params = {
        'title': title,
        'results': results,
        'totalItems': totalItems
    }
    return render(request, 'blog/search_result_with_title_rakuten.html', params)


def use_googleAPI(input,author_or_title):
    REQUEST_URL_GOOGLE = 'https://www.googleapis.com/books/v1/volumes'

    if author_or_title == "author":
        search_params_GoogleBooksAPI = {
            "q"       : "inauthor: " + input,
            "sort"    : "newest"
        }
    else:
        search_params_GoogleBooksAPI = {
            "q"       : "subject: " + input,
            "sort"    : "newest"
        }
    
    response_GoogleBooksAPI = requests.get(REQUEST_URL_GOOGLE, search_params_GoogleBooksAPI)
    result = response_GoogleBooksAPI.json()
    book_list = list()
    i = 0
    totalItems = result["totalItems"]
    print("件数 : ",totalItems)
    if result["totalItems"] != 0:
        while(1):
            if (i > (totalItems - 1)) or i > 9:
                return book_list

            else:
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
                    printtype = "None"
                else:
                    printtype = info['printType']

                if ('description' in info) == False:
                    description = "None"
                else:
                    description = info['description']

                if ('language' in info) == False:
                    language = "None"
                else:
                    language = info['language']

                if ("isEbook" in saleInfo) == False:
                    Ebook = "None"
                else:
                    Ebook = saleInfo["isEbook"]

                book_list.append({
                "title": title,
                "author": author,
                "publisher": publisher,
                "publisheddate": publisheddate,
                "pages": pages,
                "language": language,
                "Ebook": Ebook, 
                })

                i += 1

    else:
        return "NOT FOUND"

def use_rakutenBooksAPI(title):
    REQUEST_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    APP_ID = "1019302335940233245"  

    search_params = {
        "format" : "json",
        "title" : title,
        "applicationId" : [APP_ID],
        "availability" : 0,
        "hits" : 10,
        "page" : 1,
        "sort" : "standard"
    }

    response = requests.get(REQUEST_URL, search_params)
    result = response.json()
    item_key = ["title","publisher","publisheddate",'itemPrice','itemUrl',"largeImageUrl","availability"]
    book_list = list()
    for i in range(0, len(result['Items'])):
        tmp_item = {}
        item = result['Items'][i]['Item']
        for key, value in item.items():
            if key in item_key:
                tmp_item[key] = value
        book_list.append(tmp_item.copy())
    return book_list,len(result["Items"])


