from blog.models import Blog, User
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio')


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Blog
        fields = ('author', 'title', 'body', 'slug')
