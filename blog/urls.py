from django.urls import path
from .views import (index, about, send_data, add_post, post_list, post_list_in_table, contacts,
                    post_detail, post_edit, post_delete, product_search)

app_name = 'blog'
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('data', send_data, name='send_data'),
    path('post/add/', add_post, name='add_post'),
    path('post/', post_list, name='post_list'),
    path('post/table/', post_list_in_table, name='post_list_in_table'),
    path('post/contacts/', contacts, name='contacts'),
    path('posts/<slug:slug>/', post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', post_delete, name='post_delete'),
    path('search/', product_search, name="product_search"),
]
