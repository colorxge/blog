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

AUTH_EXPIRE = 8 * 60 * 60

def get_token(user_id):
    '''生成token'''
    return jwt.encode({     # 加入时间戳，判断是否重发token或重新登录
        'user_id': user_id,
        'timestamp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE  # 取整
    }, settings.SECRET_KEY, 'HS256').decode()       # 字符串


def authenticate(view):
    def wapper(request: HttpRequest):
        # 自定义header jwt
        payload = request.META.get('HTTP_JWT')  # 会被加大写前缀HTTP_且全大写
        if not payload: # None  没有拿到，认证失败
            return HttpResponse(status=401)
        try: # 解码，同时验证过期时间
            payload = jwt.decode(payload, key=settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        try:
            user_id = payload.get('user_id', -1)
            user = User.objects.filter(pk=user_id).get()
            request.user = user  # 如果正确，则注入user
            print('-' * 30)
        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        ret = view(request)
        return ret
    return wapper

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


def login(request: HttpRequest):
    payload = simplejson.dumps(request.body) # 获取登陆信息
    try:
        email = payload['email']
        user = User.objects.filter(email=email).get()

        if bcrypt.checkpw(payload['password'].encode(), user.password.encode()):
            token = get_token(user.id)
            print(token)
            ret = JsonResponse({
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'eamil': user.email,
                }, 'token': token
            })
            ret.set_cookie('Jwt', token)
            return ret
        else:
            return HttpResponseBadRequest()

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
