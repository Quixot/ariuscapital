from django.contrib import admin
from .models import Project, Project_type, Project_access


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'deal_sence_short', 'deal_why_short', 'image_prev', 'price', 'investment_term', 'income', 'address',
        'access', 'type', 'temp_persend')
    # list_filter = ('status',)
    list_display_links = ('id', 'title', 'image_prev')
    search_fields = ('title', 'deal_sence', 'deal_why')
    list_editable = ('price', 'income', 'investment_term', 'access', 'type', 'temp_persend')

    def deal_why_short(self, obj):
        return "%s..." % obj.deal_why[:30] if len(obj.deal_why) > 30 else obj.deal_why

    def deal_sence_short(self, obj):
        return "%s..." % obj.deal_sence[:30] if len(obj.deal_sence) > 30 else obj.deal_sence

    deal_sence_short.short_description = 'суть'
    deal_why_short.short_description = 'почему'


admin.site.register(Project, ProjectAdmin)

admin.site.site_header = "Arius Capital"
admin.site.site_url = None
# admin.site.index_template = 'main/base.html'

admin.site.register(Project_type)
admin.site.register(Project_access)
