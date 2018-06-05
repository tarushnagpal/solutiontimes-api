from django.contrib import admin
from problemstatements.models import ProblemStatement,Solution,Mentor,Sponsor,ProblemStatementPlaylist

# Register your models here.
admin.site.register(ProblemStatement)
admin.site.register(ProblemStatementPlaylist)
admin.site.register(Solution)
admin.site.register(Mentor)
admin.site.register(Sponsor)
