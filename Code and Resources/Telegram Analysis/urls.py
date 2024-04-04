from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_form, name='telegramAnalysis'),
    path('chart/', views.chart, name='chart'),
    # path('download/<str:filename>/', views.download_json, name='download_json'),
]





# analyzer/urls.py
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('analyze/', views.analyze, name='analyze'),
# ]
