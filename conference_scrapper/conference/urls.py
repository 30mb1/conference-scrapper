from django.urls import path
from conference_scrapper.conference import views

urlpatterns = [
    path('graph/<str:source>', views.GraphView.as_view()),
    path('download/', views.DownloadView.as_view()),
    path('', views.SearchView.as_view(), name="home")
]
