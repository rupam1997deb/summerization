from django.urls import path
from . import views

urlpatterns =[
   # path('', views.tool, name='tool'),
   # path('')
    #path('analyze', views.analyze, name='analyze'),
    path('', views.tool, name='tool'),
    path('index2', views.upload_pdf, name='index2')
    
    
    
]