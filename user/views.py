from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
from django.conf import settings
import bcrypt
import jwt
import datetime
import simplejson
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")
# Create your views here.


def get_token(user_id):
    '''生成token'''
    return jwt.encode({     # 加入时间戳，判断是否重发token或重新登录
        'user_id': user_id,
        'timestamp': int(datetime.datetime.now().timestamp())   # 取整
    }, settings.SECRET_KEY, 'HS256').decode()       # 字符串


def reg(request: HttpRequest):
    payload = simplejson.loads(request.body)
    print(payload)
    logging.info(payload)
    try:
        # 有任何错误都返回400，如果保存数据错误，则向外抛出异常
        email = payload['email']
        query = User.objects.filter(email=email)
        print(query)
        print(query.query)
        if query:
            return HttpResponseBadRequest()     # 返回实例，不是异常类

        name = payload['name']
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
        print(email, name, password)

        user = User()
        user.name = name
        user.password = password
        user.email = email
        try:
            user.save()
            return JsonResponse({'token': get_token(user.id)})
        except:
            raise
    except Exception as e:
        logging.info(e)
        print(e, '____________')
        return HttpResponseBadRequest() # 返回实例，不是异常类