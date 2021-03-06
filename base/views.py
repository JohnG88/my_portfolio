import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Project, Skill, Message, Endorsement, Comment, Question
from .forms import ProjectForm, MessageForm, SkillForm, EndorsementForm, CommentForm, QuestionForm

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib import messages

from django.db.utils import OperationalError

# format_list = [('', '(all)')]
# geom_type_list = [('', '(all)')]
# try:
#     format_list.extend([(i[0],i[0]) 
#         for i in Format.objects.values_list('name')])
#     geom_type_list.extend([(i[0],i[0]) 
#         for i in Geom_type.objects.values_list('name')])
# except OperationalError:
#     pass  
#         # happens when db doesn't exist yet, views.py should be
#         # importable without this side effect

# Create your views here.

def homePage(request):
    project = Project.objects.all()
    detailed_skills = Skill.objects.exclude(body='')

    skills = Skill.objects.filter(body='')
    endorsements = Endorsement.objects.filter(approved=True)

    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            form = MessageForm()
            messages.success(request, 'Your message was successfully sent.')


    context = {'project': project, 'skills': skills, 'detailed_skills': detailed_skills, 'form': form, 'endorsements': endorsements}
    return render(request, 'base/home.html', context)

def projectPage(request, pk):
    project = Project.objects.get(id=pk)
    count = project.comment_set.count()
    comments = project.comment_set.all().order_by('-created')

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
            form = CommentForm()
            messages.success(request, 'Your comment was successfully sent.')

    context = {'project': project, 'count': count, 'comments': comments, 'form': form}
    return render(request, 'base/project.html', context)

def addProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)

def editProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    # adding the instance below will tell form what to update from
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)

def inboxPage(request):
    # messages that haven't been read top priority
    inbox = Message.objects.all().order_by('is_read')

    # unread
    unreadCount = Message.objects.filter(is_read=False).count()

    context = {'inbox': inbox, 'unreadCount': unreadCount}
    return render(request, 'base/inbox.html', context)

def messagePage(request, pk):
    message = Message.objects.get(id=pk)
    message.is_read = True
    message.save()

    context = {'message': message}
    return render(request, 'base/message.html', context)

def addSkill(request):
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your skill was successfully sent.')
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/skill_form.html', context)

def addEndorsement(request):
    form = EndorsementForm()
    
    if request.method == 'POST':
        form = EndorsementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you, your endorsement was successfully sent.')
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/endorsement_form.html', context)

def donationPage(request):

    return render(request, 'base/donation.html')


def chartPage(request):
    all_answers = Question.objects.all()
    print(f"All Answers: {all_answers}")
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        data = json.loads(request.body)
        data_answer = data.get('answer')
        answer = Question.objects.create()
        answer.answer = data_answer
        answer.save()

        backend = Question.objects.filter(answer='backend').count()
        frontend = Question.objects.filter(answer='frontend').count()
        fullstack = Question.objects.filter(answer='fullstack').count()

        return JsonResponse({
                'backend': backend,
                'frontend': frontend,
                'fullstack': fullstack
            })
        
        # print(f'Data Answer: {data_answer}')
        # if form.is_valid():
        #     data = json.loads(request.body.decode("utf-8"))
        #     tag = data['answer']
        #     item_form = form.save(commit=False)
        #     item_form.answer = data_answer
        #     # answer = Question(answer=data_answer)
        #     # answer.save()
        #     item_form.save()
        #     return JsonResponse({
        #         'answer': form.answer
        #     })
            # messages.success(request, 'Thank you, you voted successfully.')
            # return redirect('chart')
            # form = QuestionForm()
        # print(f"Form: {form}")

    context = {'form': form}
    return render(request, 'base/chart.html', context)