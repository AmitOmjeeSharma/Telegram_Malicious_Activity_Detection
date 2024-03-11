from django.db import models

# Create your models here.
from django.db import models

class Message(models.Model):
    group_link = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# from django.db import models
#
# class Message(models.Model):
#     group_link = models.CharField(max_length=255)
#     category = models.CharField(max_length=100)
#     message_text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

