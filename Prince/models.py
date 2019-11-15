from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import timezone
from django.urls import reverse
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status="published")


class Post(models.Model):
    object=models.Manager()
    published=PublishedManager()
    just_choices=(
        ('draft','Draft'),
        ('published','Published'),
    )

    title=models.CharField(max_length=20)
    slug=models.SlugField(max_length=120)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=models.TextField(max_length=220)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=just_choices,default='draft')
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    favourite=models.ManyToManyField(User,related_name='favourite')


    def __str__(self):
        return self.title

    class Meta:
        ordering=['id']

    def likes_count(self):
        return self.likes.count()



    def get_absolute_url(self):
        return reverse('details_post',args=[self.id,self.slug])

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob=models.DateTimeField(auto_now=True,blank=True,null=True)
    photo=models.ImageField(upload_to='profile_pictures',null=True,blank=True)

    def __str__(self):
        return self.user.first_name


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=5000)
    reply=models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name='replies')
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title,self.user.username)