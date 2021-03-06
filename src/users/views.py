from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from helpers.pagination import paginateQueryset

from .utils import searchProfiles
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Skill
# Create your views here.


def loginUser(request):
    page = 'login'
    context = {
        'page': page
    }
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request, 'Username was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    profiles, paginator = paginateQueryset(request, profiles)
    context = {
        'profiles': profiles,
        'search_query': search_query
    }
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    skill = request.user.profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    skill = request.user.profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted')
        return redirect('account')

    context = {
        'object': skill
    }
    return render(request, 'delete_template.html', context)
