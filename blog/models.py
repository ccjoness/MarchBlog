from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def profile_img_uh(instance, filename):
    return 'users/{}/img/{}'.format(instance.user.username, filename)


def blog_img_uh(instance, filename):
    return 'users/{}/img/{}'.format(instance.blog.slug, filename)


class User(AbstractUser):
    bio = models.TextField()
    phone = models.CharField(max_length=30)


class ProfileImage(models.Model):
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    file = models.ImageField(upload_to=profile_img_uh)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='images')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Profile Image for {}'.format(self.user.username)


class Blog(models.Model):
    author = models.ForeignKey('User', related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField()

    def save(self, **kwargs):
        if not self.id:
            s = slugify(self.title)
            num = 1
            if Blog.objects.filter(slug=s).exists():
                num += 1
                while Blog.objects.filter(slug=s+'_{}'.format(num)).exists():
                    num += 1
                else:
                    s += '_{}'.format(num)
            self.slug = s
        super().save(**kwargs)

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    file = models.ImageField(upload_to=blog_img_uh)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='images')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Blog Image for {}'.format(self.blog.title)








class Client(models.Model):
    name = models.CharField(max_length=255)


class Test(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name='tests')
    date = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    test = models.ForeignKey('Test', related_name='results', on_delete=models.CASCADE)


class Flag(models.Model):
    test = models.ForeignKey('Test', related_name='flags', on_delete=models.CASCADE)
    description = models.TextField






















