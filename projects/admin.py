from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Project, Project_type, Project_access, Order


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'deal_sence_short', 'deal_why_short', 'image_prev', 'price', 'investment_term', 'income',
        'address',
        'access', 'type')
    # list_filter = ('status',)
    list_display_links = ('id', 'title', 'image_prev')
    search_fields = ('title', 'deal_sence', 'deal_why')
    list_editable = ('price', 'income', 'investment_term', 'access', 'type')

    def deal_why_short(self, obj):
        return "%s..." % obj.deal_why[:30] if len(obj.deal_why) > 30 else obj.deal_why

    def deal_sence_short(self, obj):
        return "%s..." % obj.deal_sence[:30] if len(obj.deal_sence) > 30 else obj.deal_sence

    deal_sence_short.short_description = 'суть'
    deal_why_short.short_description = 'почему'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'image_tag', 'user', 'investment', 'created')
    list_display_links = ('id', 'image_tag', 'project', 'user', 'investment')

    def image_tag(self, obj):
        if obj.project.image:
            return mark_safe('<img src="%s" height="50" />' % (obj.project.image.url))

    image_tag.short_description = 'Фото'

admin.site.register(Project, ProjectAdmin)

admin.site.site_header = "Arius Capital"
admin.site.site_url = None
# admin.site.index_template = 'main/base.html'
admin.site.register(Project_type)
admin.site.register(Project_access)
admin.site.register(Order, OrderAdmin)
