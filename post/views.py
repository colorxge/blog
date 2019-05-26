from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from user.views import authenticate
from user.models import User
import simplejson, datetime, math
from .models import *
# Create your views here.


@authenticate
def pub(request: HttpRequest):
    post = Post()
    content  = Content()
    try:
        payload = simplejson.loads(request.body)
        post.title = payload['title']
        post.author = User(id=request.user.id)
        post.postdate = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8))
        )
        post.save()

        content.content = payload['content']
        content.post = post
        content.save()

        return JsonResponse({'post_id':post.id})
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def get(request: HttpRequest, id): # 分组捕获传入
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        print(post, '-------')
        if post:
            return JsonResponse({
                'post':{
                'post_id':post.id,
                'title': post.title,
                'author': post.author.name,
                'author_id': post.author_id,
                'postdate': post.postdate.timestamp(),
                'content': post.content.content
                }})
        # get方法保证只有一条记录返回，否则异常
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def getall(request: HttpRequest):
    try: # 页码
        page = int(request.GET.get('page', 1))
        page = page if page > 0 else 1
    except:
        page = 1

    try: # 页码行数
        # 这个数据不要轻易让浏览器改变，如果允许改变，一定要控制范围
        size = int(request.GET.get('size', 20))
        size = size if size > 0 and size < 101 else 20
    except:
        size = 20

    try: # 按照id倒排
        start = (page - 1) * size
        posts = Post.objects.order_by('-id')
        print(posts.query)
        count = posts.count()
        posts = posts[start:start + size]
        return JsonResponse({
            'post':[
                {'post_id': post.id,
                 'title': post.title}
            for post in posts ],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count / size)
            }
        })

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


