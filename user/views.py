from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
import simplejson
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")
# Create your views here.


def reg(request: HttpRequest):
    payload = simplejson.loads(request.body)
    print(payload)
    logging.info(payload)
    try:
        email = payload['email']
        query = User.objects.filter(email=email)
        print(query)
        print(query.query)
        if query:
            return HttpResponseBadRequest()
        name = payload['name']
        password = payload['password']
        print(email, name, password)

        user = User()
        user.name = name
        user.password = password
        user.email = email
        try:
            user.save()
            return JsonResponse({'user': user.id})
        except:
            raise
    except Exception as e:
        logging.info(e)
        print(e, '____________')
        return HttpResponseBadRequest() # 返回实例，不是异常类