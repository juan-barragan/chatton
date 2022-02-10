from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=36)
    room = models.CharField(max_length=36)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
 