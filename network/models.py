from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass
class AllPosts(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    post=models.CharField(max_length=255)
    timestamp=models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    def serialize(self):
        return{
              "id":self.id,
              "user":self.user,
              "post":self.post,
              "timestamp":self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
              "like":self.like
        }


class followed(models.Model):
    user=models.ForeignKey("User",on_delete=models.CASCADE,related_name="followeds")
    followeds=models.ForeignKey("User", on_delete=models.CASCADE, related_name="followeders")
    def serialize(self):
        return{
              "id":self.id,
              "user":self.user,
              "followeds":self.followeds
        }


class likes(models.Model):
    post=models.ForeignKey("AllPosts", on_delete=models.CASCADE, related_name="followers")
    liked_by=models.ForeignKey("User", on_delete=models.CASCADE, related_name="followerrrs")
    def serialize(self):
        return{
              "id":self.id,
              "post":self.post,
              "liked_by":self.liked_by
        }
