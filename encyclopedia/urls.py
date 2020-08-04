from django.urls import path

from . import views
import re

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.title, name="title"),
    path("search/<str:requestedTitle>", views.reqTitle, name="reqTitle"),
    path("createPage", views.createPage, name="createPage")
]
