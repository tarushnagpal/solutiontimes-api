from django.contrib import admin
from problemstatements.models import ProblemStatement,Solution,Mentor,Sponsor,ProblemStatementPlaylist

# Register your models here.
# class ProblemStatementAdmin(admin.ModelAdmin):
#     exclude = ('status','is_today','is_week','is_month','is_year','is_older','is_short','is_medium','is_long',)

admin.site.register(ProblemStatement )
admin.site.register(ProblemStatementPlaylist)
admin.site.register(Solution)
admin.site.register(Mentor)
admin.site.register(Sponsor)
