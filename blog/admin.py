from django.contrib import admin
from blog.models import UserPost
# Register your models here.


class UserPostAdmin(admin.ModelAdmin):
    list_display = ('authorUsername','title','dateUpdate','userStatus','adminStatus','image_tag')
    list_filter = ('dateUpdate','userStatus','adminStatus')
    list_editable = ('adminStatus',)
    search_fields = ('title','label','category','authorUsername__username')
    exclude = ('label',)
    list_per_page = 20

admin.site.register(UserPost,UserPostAdmin)