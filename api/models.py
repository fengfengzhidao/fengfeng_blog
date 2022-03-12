from django.db import models


# Create your models here.
class Email(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='发送者邮箱')
    content = models.TextField(verbose_name='发送的内容')
    create_date = models.DateTimeField(verbose_name='发送时间', auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = '邮件发送'
