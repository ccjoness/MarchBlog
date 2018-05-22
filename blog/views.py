from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from blog.models import User, ProfileImage, Blog
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from blog.serializers import BlogSerializer

# Blog Views
def home(request):
    blogs = Blog.objects.all().order_by('-pk')
    return render(request, 'blog/index.html', {'blogs': blogs})


def single_blog(request, b_slug):
    blog = get_object_or_404(Blog, slug=b_slug)
    blog_image = blog.images.all()
    if blog_image:
        image = blog_image[0].file.url
    else:
        image = 'http://via.placeholder.com/500x500'

    return render(request, 'blog/single_blog.html', {'b': blog, 'blog_image': image})


# Api Endpoints
def username_validator(request):
    """
    Return True if username is available else False.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        return JsonResponse({'message': 'success', 'available': not User.objects.filter(username=username).exists()})
    return JsonResponse({'message': 'error'})


# Authentication
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        user = authenticate(
            request, username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        usr = User()
        usr.username = request.POST.get('username')
        # usr.password
        usr.set_password(request.POST.get('password'))
        usr.email = request.POST.get('email')
        usr.phone = request.POST.get('phone')
        usr.bio = request.POST.get('bio')
        usr.save()

        image_file = request.FILES.get('image')
        if image_file:
            img = ProfileImage()
            img.file = image_file
            img.alt_text = request.POST.get('alt_text', 'none')
            img.description = request.POST.get('img_desc', 'none')
            img.user = usr
            img.save()
        return redirect('login')

    return render(request, 'register.html')


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
