from django.contrib import admin
from .models import Contact,UserProfile
from django.contrib.auth.models import Group

admin.site.site_header = 'MyProject Admin Dashboard'
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','desc_field','timeStamp','Delete')
    list_display_links = ('name','email')
    list_filter = ('timeStamp',)
    search_fields = ('name','email','phone','desc')

class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('coverImage',) #fields that not include in admin panel
    list_display = ('UserUsername','phoneNumber','Gender','isPublic','JoiningDate','image_tag')
    list_filter = ('JoiningDate','Gender','language')
    search_fields = ('UserUsername__username','phoneNumber','Gender','Country','State','District','city','address','language')
    list_editable = ('isPublic',)

admin.site.register(Contact,ContactAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.unregister(Group)
