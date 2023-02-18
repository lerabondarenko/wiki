from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("search", views.search, name="search"), 
    path("random", views.random_page, name="random"),
    path("<str:title>", views.title, name="title")
]
