from django.urls import path
from conference_scrapper.conference import views

urlpatterns = [
    path('graph/', views.GraphView.as_view()),
    path('graph/v2', views.NickGrpah.as_view()),
    path('game/<int:vertex>', views.GameView.as_view()),
    path('download/', views.DownloadView.as_view()),
    path('', views.SearchView.as_view(), name="home")
]
