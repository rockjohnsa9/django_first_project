from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .utils import searchProject
from .models import Project
from .forms import ProjectForm, ReviewFrom
from helpers.pagination import paginateQueryset


def projects(request):
    projects, search_query = searchProject(request)
    projects, paginator = paginateQueryset(request, projects)
    context = {
        'projects': projects,
        'search_query': search_query,
        'paginator': paginator,
        # 'custom_range': custom_range
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewFrom()

    if request.method == 'POST':
        form = ReviewFrom(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            projectObj.getVoteCount

            messages.success(request, 'Your review was successfully submitted')
            return redirect('project', pk=projectObj.id)

    context = {
        'project': projectObj,
        'form': form
    }
    return render(request, "projects/single_project.html", context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {
        'object': project
    }
    return render(request, "delete_template.html", context)
