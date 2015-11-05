from __future__ import absolute_import

from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from .models import Candidate, Comment, CustomUser, PoliticalParty, Race
from django.template import RequestContext
from .forms import CandidateModelCreateForm, CandidateModelUpdateForm, CommentModelUpdateForm, CustomUserCreateForm, CustomUserModelUpdateForm, UserLogin, CommentForm, PoliticalPartyModelCreateForm, PoliticalPartyModelUpdateForm, RaceModelCreateForm, RaceModelUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required


def candidate_detail_view(request, pk):
    candidate = Candidate.objects.get(pk=pk)

    context = {}
    context['candidate'] = candidate

    form = CommentForm()
    context['form'] = form
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            new_comment = Comment.objects.create(body=body)
            new_comment.author = request.user
            new_comment.candidate = candidate
            new_comment.save()
            candidate.save()

    return render_to_response('candidate_detail.html', context, context_instance=RequestContext(request))


def candidate_response(request):

    #  search string from GET dictionary
    search_string = request.GET.get('search', '')
#   query-set Cereals with search string
    candidates = Candidate.objects.filter(name__icontains=search_string)
#   new empty cereal list
    candidate_list = []
#   for loop for cereal query set
    for candidate in candidates:
        candidate_list.append(candidate.name)
#   append cereal name to cereal list
    return JsonResponse(candidate_list, safe=False)


def vote_up(request):
    candidate = Candidate.objects.get(pk=int(request.GET.get('pk')))
    if request.user not in candidate.up_users.all():
        if request.user in candidate.down_users.all():
            candidate.down_users.remove(request.user)
        candidate.up_users.add(request.user)
        src = "voted"
        print "add"
    else:
        candidate.up_users.remove(request.user)
        src = "vote"
        print "remove"
    candidate.save()
    return JsonResponse([candidate.up_vote_count, src, candidate.down_vote_count], safe=False)


def vote_down(request):
    candidate = Candidate.objects.get(pk=int(request.GET.get('pk')))
    if request.user not in candidate.down_users.all():
        if request.user in candidate.up_users.all():
            candidate.up_users.remove(request.user)
        candidate.down_users.add(request.user)
        src = "voted"
        print "add"
    else:
        candidate.down_users.remove(request.user)
        src = "vote"
        print "remove"
    candidate.save()
    return JsonResponse([candidate.down_vote_count, src, candidate.up_vote_count], safe=False)


def ajax_search(request):
    context = {}
    return render_to_response('ajax_search.html', context, context_instance=RequestContext(request))


def candidate_list_view(request):

    candidates = Candidate.objects.all()

    context = {}
    context['candidates'] = candidates

    return render_to_response('candidate_list.html', context, context_instance=RequestContext(request))


def candidate_create_view(request):

    context = {} 
    form = CandidateModelCreateForm()
    context['form'] = form

    if request.method == 'POST':
        form = CandidateModelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print form.is_valid()

            form.save()
            return redirect('candidate_list_view')
        else:
            context['errors'] = form.errors
    return render_to_response('candidate_create.html', context, context_instance=RequestContext(request))


def candidate_update_view(request, pk):
    context = {}

    if not request.user.is_staff:
        raise Http404("You're not authorized to be here!")

    candidate = Candidate.objects.get(pk=pk)

    context['candidate'] = candidate

    form = CandidateModelUpdateForm(request.POST or None, instance=candidate)

    context['form'] = form

    if request.method == 'POST':
        form = CandidateModelUpdateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()

            return redirect('candidate_update_view', pk=pk)

        else:
            context['errors'] = form.errors

    return render_to_response('candidate_update.html', context, context_instance=RequestContext(request))



def candidate_delete_view(request, pk):

    Candidate.objects.get(pk=pk).delete()

    return redirect('candidate_list_view')


@login_required
def user_detail_view(request, pk):  
    user = CustomUser.objects.get(pk=pk)
    context = {}
    context['user'] = user

    return render_to_response('user_detail.html', context, context_instance=RequestContext(request))


def user_list_view(request):

    users = CustomUser.objects.all()

    context = {}
    context['users'] = users

    return render_to_response('user_list.html', context, context_instance=RequestContext(request))


def comment_detail_view(request, pk):  
    comment = Comment.objects.get(pk=pk)

    context = {}
    context['comment'] = comment

    return render_to_response('comment_detail.html', context, context_instance=RequestContext(request))


def comment_list_view(request):

    if not request.user.is_authenticated():
        raise Http404("You're not logged in!")
    if request.user.is_staff:
        comments = Comment.objects.all()
    else:
        comments = Comment.objects.filter(author=request.user)

    context = {}
    context['comments'] = comments

    return render_to_response('comment_list.html', context, context_instance=RequestContext(request))


def comment_update_view(request, pk):
    context = {}
    comment = Comment.objects.get(pk=pk)

    context['comment'] = comment

    form = CommentModelUpdateForm(request.POST or None, instance=comment)

    context['form'] = form

    if request.method == 'POST':
        form = CommentModelUpdateForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()

            return redirect('comment_update_view', pk=pk)

        else:
            context['errors'] = form.errors

    return render_to_response('comment_update.html', context, context_instance=RequestContext(request))


def comment_delete_view(request, pk):

    comment = Comment.objects.get(pk=pk)
    candidate = comment.candidate
    comment.delete()
    return redirect('candidate_detail_view', candidate.pk)


def user_update_view(request, pk):

    context = {}
    if not request.user.is_authenticated():
        raise Http404("Please log in first!")
    user = CustomUser.objects.get(pk=pk)

    context['user'] = user

    form = CustomUserModelUpdateForm(request.POST or None, instance=user)

    context['form'] = form

    if request.method == 'POST':
        form = CustomUserModelUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            return redirect('user_update_view', user.pk)

        else:
            context['errors'] = form.errors

    return render_to_response('user_update.html', context, context_instance=RequestContext(request))


def user_delete_view(request, pk):

    logout(request)
    user = CustomUser.objects.get(pk=pk)
    for comment in user.comment_set.all():
        comment.author = None
        comment.save()
    user.delete()

    return redirect('user_list_view')




def signup(request):

    context = {}

    form = CustomUserCreateForm()
    context['form'] = form

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            print form.cleaned_data

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password == password2:
                try:
                    new_user = CustomUser.objects.create_user(email, password)
                    context['valid'] = "Thank You For Signing Up!"

                    auth_user = authenticate(username=email, password=password)
                    login(request, auth_user)

                    return redirect('candidate_list_view')

                except IntegrityError, e:
                    context['valid'] = "A User With That Name Already Exists"
            else:
                context['valid'] = "Your passwords didn't match!"

        else:
            context['valid'] = form.errors

    if request.method == 'GET':
        context['valid'] = "Please Sign Up!"

    return render_to_response('signup_view.html', context, context_instance=RequestContext(request))


def login_view(request):

    context = {}

    context['form'] = UserLogin(initial={'next_page': request.GET.get('next')})
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            next_page = form.cleaned_data['next_page']
            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    context['valid'] = "Login Successful"
                    print next_page
                    if next_page == None or next_page == "":
                        return redirect('candidate_list_view')
                    else:
                        return redirect(next_page)
                else:
                    context['valid'] = "Invalid User"
            else:
                context['valid'] = "Login Failed! Try again"


    return render_to_response('login_view.html', context, context_instance=RequestContext(request))


def logout_view(request):

    logout(request)

    return redirect('login_view')


def political_party_detail_view(request, pk):  
    political_party = PoliticalParty.objects.get(pk=pk)

    context = {}
    context['political_party'] = political_party

    return render_to_response('political_party_detail.html', context, context_instance=RequestContext(request))


def political_party_list_view(request):

    political_parties = PoliticalParty.objects.all()

    context = {}
    context['political_parties'] = political_parties

    return render_to_response('political_party_list.html', context, context_instance=RequestContext(request))

def political_party_create_view(request):

    context = {} 
    form = PoliticalPartyModelCreateForm()
    context['form'] = form

    if request.method == 'POST':
        form = PoliticalPartyModelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print form.is_valid()

            form.save()
            return redirect('political_party_list_view')
        else:
            context['errors'] = form.errors
    return render_to_response('political_party_create.html', context, context_instance=RequestContext(request))


def political_party_update_view(request, pk):

    context = {}

    political_party = PoliticalParty.objects.get(pk=pk)

    context['political_party'] = political_party

    form = PoliticalPartyModelUpdateForm(request.POST or None, instance=political_party)

    context['form'] = form

    if request.method == 'POST':
        form = PoliticalPartyModelUpdateForm(request.POST, request.FILES, instance=political_party)
        if form.is_valid():
            form.save()

            return redirect('political_party_update_view', pk=pk)

        else:
            context['errors'] = form.errors

    return render_to_response('political_party_update.html', context, context_instance=RequestContext(request))



def political_party_delete_view(request, pk):

    party = PoliticalParty.objects.get(pk=pk)
    for candidate in party.candidate_set.all():
        candidate.political_party = None
        candidate.save()

    party.delete()

    return redirect('political_party_list_view')



def race_detail_view(request, slug):  
    race = Race.objects.get(district=slug)

    context = {}
    context['race'] = race

    return render_to_response('race_detail.html', context, context_instance=RequestContext(request))


def race_list_view(request):
    races = Race.objects.all()

    context = {}
    context['races'] = races

    return render_to_response('race_list.html', context, context_instance=RequestContext(request))

def choose_state_race_view(request): 
    return render(request, 'choose_state_race.html')

def state_race_list_view(request, slug):
    races = Race.objects.filter(state_abbrev__icontains=slug)

    context = {}
    context['races'] = races

    return render_to_response('race_list.html', context, context_instance=RequestContext(request))


def race_create_view(request):

    context = {} 
    form = RaceModelCreateForm()
    context['form'] = form

    if request.method == 'POST':
        form = RaceModelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print form.is_valid()

            form.save()
            return redirect('race_list_view')
        else:
            context['errors'] = form.errors
    return render_to_response('race_create.html', context, context_instance=RequestContext(request))


def race_update_view(request, pk):

    context = {}

    race = Race.objects.get(pk=pk)

    context['race'] = race

    form = RaceModelUpdateForm(request.POST or None, instance=race)

    context['form'] = form

    if request.method == 'POST':
        form = RaceModelUpdateForm(request.POST, request.FILES, instance=race)
        if form.is_valid():
            form.save()

            return redirect('race_update_view', pk=pk)

        else:
            context['errors'] = form.errors

    return render_to_response('race_update.html', context, context_instance=RequestContext(request))


def race_delete_view(request, pk):

    Race.objects.get(pk=pk).delete()

    return redirect('race_list_view')


def candidate_compare_view(request, slug, pk):
    context = {}
    race = Race.objects.get(district=slug)
    context['race'] = race
    primary = race.candidate_set.get(pk=pk)
    context['primary'] = primary
    if len(race.candidate_set.all()) > 1:
        context['secondary'] = race.candidate_set.exclude(pk=primary.pk)[0]
        context['other'] = race.candidate_set.exclude(pk=primary.pk)
    else:
        context['secondary'] = False

    return render_to_response('candidate_compare.html', context, context_instance=RequestContext(request))


def switch_candidates(request):
    candi = Candidate.objects.get(pk=int(request.GET.get('pk')))
    if candi.image:
        url = candi.image.url
    else:
        url = ""
    in_up = request.user in list(candi.up_users.all())
    in_down = request.user in list(candi.down_users.all())

    return JsonResponse([candi.name, candi.hometown, candi.known_for, candi.political_party.initials, url, candi.pk, candi.up_vote_count, candi.down_vote_count, in_up, in_down], safe=False)