from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    desc = models.CharField(max_length=256, default='')
    active = models.BooleanField(default=True)


class Record(models.Model):
    target = models.ForeignKey('Client', on_delete=models.CASCADE)
    tag = models.CharField(max_length=64, default='')
    addr = models.CharField(max_length=64, default='')
    insert_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
