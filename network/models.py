from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.conf import settings
import uuid



#define custom managers



class User(AbstractUser):
    pass


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_follows")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_is_followed")
    follow_time = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['following', 'follower'], name='must be unique')
        ]

    def __str__(self):      
	    return f"{self.following}"


class PostManager(models.Manager):
    def get_username(self):
        posts = self.model.objects.all().order_by("-time")
        returned_data = []
        for post in posts:
            user = post.user
            data = {
                "username":user.username,
                "userId":user.id,
                "post":post.post,
                "time":post.time,
                "likes":post.likes,
                "postId":post.id
            }
            returned_data.append(data)
        return returned_data

    def like_post(self):
        return self.model.likes+1

    def unlike(self):
        return self.model.like-1

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=True)
    post = models.TextField(default="")
    time = models.DateTimeField(auto_now_add=True)
    likers = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True, related_name="likers")
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    objects = models.Manager()
    custom = PostManager() 

    def __str__(self):
        return f"{self.user.username}: {self.post} "

