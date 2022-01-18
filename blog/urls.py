from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('post/list', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('search/', views.search, name='search'),
    path('search/with_author/', views.search_with_author, name='search_with_author'),
    path('search/with_title/', views.search_with_title, name='search_with_title'),
    path('search/result_with_author/<str:author>', views.search_result_with_author, name='search_result_with_author'),
    path('search/result_with_title/<str:title>', views.search_result_with_title, name='search_result_with_title'),
    path('search/result_result_with_author/rakuten/<str:title>', views.search_result_with_title_rakuten, name='search_result_with_author_rakuten'),
    path('search/result_result_with_title/rakuten/<str:title>', views.search_result_with_title_rakuten, name='search_result_with_title_rakuten'),
]