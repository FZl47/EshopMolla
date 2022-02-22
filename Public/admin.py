from django.contrib import admin
from .models import SiteInfo , CommentSupport , OutStor ,FaqCategory , Faq

admin.site.register(SiteInfo)
admin.site.register(OutStor)
admin.site.register(FaqCategory)
admin.site.register(Faq)


class CommentSupportCustomizeAdmin(admin.ModelAdmin):
    list_display = ['__str__','is_checked']
    list_filter = ['is_checked']
    search_fields = ['subject']


admin.site.register(CommentSupport,CommentSupportCustomizeAdmin)

