from django.contrib import admin
from .models import Post,Comment,Profile


#time zone _update=timezone.now()-timezone.timedelta(hours=1)


class Postadmin(admin.ModelAdmin):
    list_display = ('title','slug','author','status')
    list_filter = ('status','created','updated')
    search_fields = ('title',)
    list_editable = ('status',)
    date_hierarchy = ('created')


admin.site.register(Post,Postadmin)
admin.site.register(Profile)
admin.site.register(Comment)