from django.urls import path
from . import views

urlpatterns =[
   # path('', views.tool, name='tool'),
   # path('')
    #path('analyze', views.analyze, name='analyze'),
   # path('text', views.tool, name='text'),
    path('pdf2', views.upload_pdf, name='pdf2'),
    path('', views.homepage, name='homepage'),
    path('text2', views.tool, name='text2'),
    
]