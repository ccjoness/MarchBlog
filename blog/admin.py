from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from blog.models import User, ProfileImage, Blog, BlogImage


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('bio', 'phone')}),
    )


class BlogImageInline(admin.StackedInline):
    model = BlogImage
    extra = 1


class BlogImageModelAdmin(admin.ModelAdmin):
    list_display = ('blog_author', 'file', 'alt_text')

    def blog_author(self, obj):
        return obj.blog.author.first_name or obj.blog.author.username
    blog_author.short_description = 'Author'


class BlogModelAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]


admin.site.register(User, MyUserAdmin)
admin.site.register(ProfileImage)
admin.site.register(Blog, BlogModelAdmin)
admin.site.register(BlogImage, BlogImageModelAdmin)
