from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def navigate(request):
    if request.method == "POST":
        button = request.POST['button']
        if button == 'admin':
            return redirect('admin_login')
        elif button == 'user':
            return redirect('login')
    return render(request, 'navigate.html')


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        messages.error(request, "You are admin, you can use only admin login !")
        return redirect('navigate')
    elif not request.user.is_authenticated:
        return redirect('login')
    service_obj = Service.objects.all()
    total_services = len(service_obj)
    query_obj = Query.objects.filter(approved=True)
    total_queries = len(query_obj)
    answer_obj = Answer.objects.all()
    total_answers = len(answer_obj)
    return render(request, 'home.html', {'total_services': total_services, 'total_queries': total_queries,
                                         'total_answers': total_answers})


def register(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username taken!')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'email already exist.')
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Successfully Registered!')
            return redirect('register')
    return render(request, 'register.html')


def login(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('navigate')


@login_required(login_url='login')
def services(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    service_list = Service.objects.all()
    return render(request, 'services.html', {'service_list': service_list})


@login_required(login_url='login')
def add_service(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        service_name = request.POST['service_name']
        service_provider = request.POST['service_provider']
        price = request.POST['price']
        contact_no = request.POST['contact_no']
        Service.objects.create(service_name=service_name, service_provider_name=service_provider, price=price,
                               contact_no=contact_no, posted_by=request.user)
        return redirect('services')
    return render(request, 'add_service.html')


@login_required(login_url='login')
def queries(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    query_list = Query.objects.filter(approved=True)
    print(query_list)
    return render(request, 'queries.html', {'query_list': query_list})


@login_required(login_url='login')
def ask_question(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        category = request.POST['category']
        question = request.POST['question']
        Query.objects.create(que_category=category, question=question, posted_by=request.user)
        messages.success(request, "We received your query, It will be live here after it will be approved by the authorised staff. ")
        return redirect('queries')
    return render(request, 'ask_question.html')


@login_required(login_url='login')
def discussion(request, pk):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    que = get_object_or_404(Query, pk=pk)
    que_id = que.id
    answer_list = Answer.objects.filter(que_id=que.id)
    if request.method == "POST":
        answer = request.POST['answer']
        Answer.objects.create(que_id=que_id, answer=answer, posted_by=request.user)
        return redirect('discussion', pk=pk)
    return render(request, 'discussion.html', {'que': que, 'answers': answer_list})


def contact(request):
    return render(request, 'contact.html')


def admin_login(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('admin_panel')
            else:
                messages.info(request, 'Sorry Only admin is allowed !')
                return redirect('admin_login')
        else:
            messages.info(request, 'Invalid Credentials !')
            return redirect('admin_login')
    return render(request, 'admin/admin_login.html')


def admin_panel(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    users = User.objects.all().exclude(is_staff=True)
    service_obj = Service.objects.all()
    total_services = len(service_obj)
    total_queries = len(Query.objects.all())
    query_approved = Query.objects.filter(approved=True)
    total_approved_queries = len(query_approved)
    unapproved_queries = len(Query.objects.filter(approved=False))
    answer_obj = Answer.objects.all()
    total_answers = len(answer_obj)
    return render(request, 'admin/admin_panel.html', {'users': len(users), 'total_services': total_services,
                                                      'total_approved_queries': total_approved_queries,
                                                      'total_queries': total_queries,
                                                      'unapproved_queries': unapproved_queries,
                                                      'total_answers': total_answers})


def users(request):
    if not request.user.is_staff:
        return redirect('admin_panel')
    users = User.objects.all().exclude(is_staff=True)
    return render(request, 'admin/users.html', {'users': users})


def user_details(request, pk):
    if not request.user.is_staff:
        return redirect('admin_panel')
    user = get_object_or_404(User, pk=pk)
    service_list = Service.objects.filter(posted_by=user.username)
    print(service_list, request.user)
    return render(request, 'admin/user_details.html', {'user': user, 'services': service_list})


def del_service(request, pk):
    if not request.user.is_staff:
        return redirect('admin_panel')
    service = get_object_or_404(Service, pk=pk)
    Service.objects.filter(id=service.id).delete()
    return render(request, 'admin/user_details.html')


def admin_queries(request):
    if not request.user.is_staff:
        return redirect('admin_panel')
    query_list = Query.objects.all()
    return render(request, 'admin/admin_queries.html', {'queries': query_list})


def change_sts(request, pk):
    if not request.user.is_staff:
        return redirect('admin_panel')
    query = get_object_or_404(Query, pk=pk)
    print(query.approved)
    if not query.approved:
        query.approved = True
        query.save()
    elif query.approved:
        query.approved = False
        query.save()
    return redirect('admin_queries')
