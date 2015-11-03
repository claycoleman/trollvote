#! /usr/bin/env python
import requests, re, os, sys, urllib2, string
from lxml import html 

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from app.models import Candidate, PoliticalParty, Race
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from ghost import Ghost

import django
django.setup()
print ""
url = "http://realtime.influenceexplorer.com/senate/2016/"
response = requests.get(url)
print response
# CLIENT_KEY = 920597814981-4l25vtrnvmme2cg6icm26qk3fgs19dph.apps.googleusercontent.com
# CLIENT_SECRET_KEY = MBrj64HOFGvXEq5JN2y63qyP

# NYTIME_KEY = 37d0450a4027cc9506266cece4a6dd92:7:73362757

# SUNLIGHT_KEY = aae93b22bc7246f7aa217742aed7d034
tree = html.fromstring(response.text)
candidate_list = tree.xpath("//*[@id='mainPageTable']/tbody/tr")
for count, candidate_details in enumerate(candidate_list):
    race, created = Race.objects.get_or_create(state_abbrev=candidate_details[3].getchildren()[0].text[:2])
    race.name = "%s Senate Race 2016" % race.state_abbrev
    name = '%s' % candidate_details[0].getchildren()[0].text
    name_parts = name.partition(', ')
    proper_name = string.capwords((name_parts[2] + " " + name_parts[0]).lower())
    new_candi, made = Candidate.objects.get_or_create(name=proper_name)
    new_candi.race = race
    party = PoliticalParty.objects.get(name__istartswith=candidate_details[2].text)
    new_candi.political_party = party
    if candidate_details[1].text == "Y":
        new_candi.known_for = "Current US Senator"
    else:
        new_candi.known_for = "Challenger / Aspiring US Senator"
    new_candi.hometown = race.state_abbrev
    print "%d: %s" % (count, new_candi.name)

    new_candi.save()
    race.save()

for race in Race.objects.all():
    if len(race.candidate_set.all()) is 0:
        race.delete()





# for count, td in enumerate(candidate_details):
#     if count is 0:
#         name = '%s' % td.getchildren()[0].text
#         name_parts = name.partition(', ')
#         print string.capwords((name_parts[2] + " " + name_parts[0]).lower())
#         continue
#     elif count is 3: 
#         print '%s' % td.getchildren()[0].text
#         continue

#     print td.text

