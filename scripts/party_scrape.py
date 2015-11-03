#! /usr/bin/env python
import requests, re, os, sys, urllib2
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

url = "http://www.politics1.com/p2016.htm"
custom_headers = {'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"}
# gh = Ghost()
# print "got ghost"
# with gh.start() as session:

#     page, resources = session.open('http://coleclayman.us/')
#     print page.exists("document.getElementById('my-input')")
response = requests.get(url)
# print response.text
tree = html.fromstring(response.text)
# dem_images = tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/table/td[1]/font/img/@src')

# democrats = tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/table/td[2]/p/font/font/strong/text()')
# for count, democrat in enumerate(democrats): 
#     democrat = "%s" % democrat
#     democrat = democrat.replace("'", "").replace('\r\n      ','').strip(" ")
#     info = re.search("(?P<position>.*)(?P<space1>\s)(?=(?P<first>\w+)(?P<space2>\W)(?P<last>\w+)(?P<spacelast>\W)(?P<space>\W)(?<=\()(?P<hometown>.*)(?=\)))", democrat).groupdict()
#     name = info.get('first') + " " + info.get('last')
#     new_candi, created = Candidate.objects.get_or_create(name=name)
#     new_candi.hometown = info.get('hometown')
#     new_candi.known_for = re.sub(r'[\s]{2,16}', ' ', info.get('position'))
#     new_candi.political_party = PoliticalParty.objects.get(name='Democratic Party')
#     image_reponse = requests.get("http://www.politics1.com/" + dem_images[count])
#     temp_image = NamedTemporaryFile(delete=True)
#     temp_image.write(image_reponse.content)
#     new_candi.image.save('%s.jpg' % name, File(temp_image))

#     new_candi.save()


rep_images = tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/center/table/td[1]/font/img/@src')
print len(rep_images)

repubs = tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/center/table/td[2]/p/font/font/strong/text()')
repubs.insert(10,tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/center/table[11]/td[2]/p/font/font/b/text()'))

repubs.insert(13, tree.xpath('/html/body/table/tr[3]/td/center[2]/table/tr/td[1]/center/table[14]/td[2]/p/font/font/b/text()'))


for count, repub in enumerate(repubs): 
    repub = "%s" % repub
    repub = repub.replace("'", "").replace('\r\n      ','').strip(" ")
    info = re.search("(?P<position>.*)(?P<space1>\s)(?=(?P<first>\w+)(?P<space2>\W)(?P<last>\w+)(?P<spacelast>\W)(?P<space>\W)(?<=\()(?P<hometown>.*)(?=\)))", repub).groupdict()
    name = info.get('first') + " " + info.get('last')
    new_candi, created = Candidate.objects.get_or_create(name=name)
    new_candi.hometown = info.get('hometown')
    new_candi.known_for = re.sub(r'[\s]{2,16}', ' ', info.get('position'))
    new_candi.political_party = PoliticalParty.objects.get(name='Republican Party')
    image_reponse = requests.get("http://www.politics1.com/" + rep_images[count])
    temp_image = NamedTemporaryFile(delete=True)
    temp_image.write(image_reponse.content)
    new_candi.image.save('%s.jpg' % name, File(temp_image))
    print new_candi.name
    new_candi.race = Race.objects.get(name__icontains="Presid")
    new_candi.save()


# /html/body/table/tbody/tr[3]/td/center[2]/table/tbody/tr/td[1]
# /html/body/table/tr[3]/td/center[2]/table/tr/td[1]/table[1]/tbody/tr/td[2]/p/font/font/strong
# /html/body/table/tr[3]/td/center[2]/table/tr/td[1]/center/table[1]/tbody/tr/td[1]/font/img
