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

response = requests.get("http://realtime.influenceexplorer.com/house/2016/#?candidate_filter=all")
print response

tree = html.fromstring(response.text)
candidate_list = tree.xpath("//*[@id='mainPageTable']/tbody/tr")
for count, candidate_details in enumerate(candidate_list):
    race, created = Race.objects.get_or_create(district=candidate_details[3].getchildren()[0].text)
    race.name = "%s House Race 2016" % race.district
    race.race_type = 'H'
    race.state_abbrev = race.district[:2]
    name = '%s' % candidate_details[0].getchildren()[0].text
    name_parts = name.partition(', ')
    proper_name = string.capwords((name_parts[2] + " " + name_parts[0]).lower())
    new_candi, made = Candidate.objects.get_or_create(name=proper_name)
    new_candi.race = race
    try: 
        party = PoliticalParty.objects.get(name__istartswith=candidate_details[2].text)
    except Exception, e:
        print e
        party = PoliticalParty.objects.get(initials=candidate_details[2].text)
    new_candi.political_party = party
    if candidate_details[1].text == "Y":
        new_candi.known_for = "Current US Representative"
    else:
        new_candi.known_for = "Challenger / Aspiring US Representative"
    new_candi.hometown = race.state_abbrev
    print "%d: %s" % (count, new_candi.name)

    new_candi.save()
    race.save()

for race in Race.objects.all():
    if len(race.candidate_set.all()) is 0:
        race.delete()