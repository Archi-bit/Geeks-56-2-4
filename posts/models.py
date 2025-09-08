from django.db import models



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=556, null=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} -- {self.content}"