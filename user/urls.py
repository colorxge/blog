from django.conf.urls import url
from .views import *


# from django.http import HttpRequest, HttpResponse
# def reg(request: HttpRequest):
#     print(request.method)
#     print(request.body)
#     return HttpResponse(b'hahaha')

urlpatterns = [
    url(r'^reg$', reg),
    url(r'^login$', login),
]
