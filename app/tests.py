from django.test import TestCase
from app.models import Candidate
from django.core.urlresolvers import reverse

# Create your tests here.

def set_up_candidates(): 
        print Candidate.objects.create(name="Ash Ketchum")
        print Candidate.objects.create(name="Michael Scott")

class CandidateTestCase(TestCase):
    def test_created_worked(self): 
        set_up_candidates()
        michael_scott = Candidate.objects.get(name="Michael Scott")
        ash_ketchum = Candidate.objects.get(name="Ash Ketchum")
        self.assertEqual(michael_scott.name, "Michael Scott")
        self.assertEqual(ash_ketchum.name, "Ash Ketchum")

class CandidateListViewTests(TestCase):

    def test_list_view(self):

        set_up_candidates()
        response = self.client.get(reverse('candidate_list_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('candidates' in response.context)
        self.assertQuerysetEqual(list(response.context['candidates'].order_by('name')), Candidate.objects.all())