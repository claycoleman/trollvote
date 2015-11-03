from django.contrib import admin
from app.models import Candidate, Comment, CustomUser, PoliticalParty, Race

admin.site.register(Candidate)
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(PoliticalParty)
admin.site.register(Race)
