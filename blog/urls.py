from django.urls import path
from .views import BlogsAPIView, BlogAPIView


urlpatterns = [
    path("blog", BlogsAPIView.as_view()),
    path("blog/<id>", BlogAPIView.as_view()),
]