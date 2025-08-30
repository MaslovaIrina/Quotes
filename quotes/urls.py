from django.urls import path
from quotes_app import views
 
urlpatterns = [
    path("add_quote/create_result/", views.create_result),
    path('', views.random_quote, name='random_quote'),
    path("add_quote/", views.adding_quote, name = 'add_quote'),
    path("contacts/", views.contacts),
    path("top_quotes/", views.top_quotes, name='top_quotes'),
    path('<int:quote_id>/like/', views.like_quote, name='like_quote'),
    path('<int:quote_id>/dislike/', views.dislike_quote, name='dislike_quote'),
    path('edit_quote/<int:quote_id>/', views.edit_quote, name='edit_quote'),
]


