from django.db import models
from user.models import *

# Create your models here.

class Post(models.Model):
    class Meta:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    postdate = models.DateTimeField(null=False)
    # 从post查作者，从post查内容
    author = models.ForeignKey(User)    # 指定外键，migrate会生成author_id字段
    # self.content可以访问Content实例，其内容是seif.content.content

    def __repr__(self):
        return '<Post {} {} {} {}>'.format(
            self.id, self.title, self.author_id, self.content)

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = 'content'

    # 没有主键，会自增一个主键
    post = models.OneToOneField(Post) # 一对一，这边会有一个外键引用post.id
    content = models.TextField(null=False)

    def __repr__(self):
        return 'Content {} {}'.format(self.post.id, self.content[:20])

    __str__ = __repr__
