from django.shortcuts import render, redirect 
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import uuid 
from .models import StudentModel,TestModel,AnswerModel,StudentCheck
from . forms import StudentForm, TestForm, AnswerForm,ExcelForm
import random
import string
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

def home(request):
    context = {}
    return render(request, 'home.html',context)

def login_page(request):
    context = {}
    template_name = 'form.html'
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
       
        #self.cleaned_data['start_time']
       # self.cleaned_data['end_time']
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('4',password,username,user)
            if user is not None:
                print()
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('admin_panel')
            else:
                print('1')
                messages.error(request, "Invalid username or password.")
        else:
            print('2')
            messages.error(request, "Invalid username or password.")
    print('3')
    
    context['form'] = form
    return render(request,template_name,context)
    

@login_required(login_url='login_page')
def display_test(request):
    context={}
    template_name = 'display_test.html'

    email = request.user.email
    context['tests'] = TestModel.objects.filter(email=email)
    return render(request,template_name,context)

@login_required(login_url='login_page')
def admin_panel(request):
    context={}
    template_name = 'admin_home.html' 
    print(request.user.email)
    return render(request,template_name,context)

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')


@login_required(login_url='login_page')
def create_test(request):
    context={}
    template_name = 'create_test.html' 
    
    form = TestForm()
    
    if request.method == 'POST':
        form = TestForm(request.POST,request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            test.email = request.user.email
            test.test_id = uuid.uuid1()
            test.grading_id = uuid.uuid1()
            print(test.test_id)
            print(test.grading_id)
            test.save()
            return redirect('admin_panel')
        else:
            print('invalid form')
      

    context['form']= form
    return render(request,template_name,context)

def submit_response(request,test_id = None):
    context={}
    template_name = 'submit.html' 
    print(test_id)
    
    form = AnswerForm() 
    if request.method=='POST':
        print('Post testid',test_id)
        email = request.POST.get('Email')
        password = request.POST.get('password')
        print(email,password)
        student = StudentModel.objects.filter(email=email,password=password)                                                                                                                       
        if student.exists():
            name = student[0].name
            student = StudentCheck.objects.filter(email=email,test_id=test_id)
            if student.exists():
                form = AnswerForm(request.POST,request.FILES)
                if not form.is_valid():
                    print('form not valid')
                else:
                    test = form.save(commit=False)
                    test.test_id = test_id
                    test.name = name
                
                    test.save()
                    return redirect('home')
                
            else:
                print('Test id doesnt exist')
        else:
            print('Invalid username')
    
    context['form'] = form   
    context['test'] = TestModel.objects.get(test_id=test_id)
    return render(request,template_name,context)

def grading(request,test_id,grading_id):
    context={}
    template_name = 'grading.html'

    print(test_id,grading_id)
    tests = TestModel.objects.filter(test_id=test_id,grading_id=grading_id)
    if not tests.exists():
        template_name = 'invalid_url.html'
    else:
        tests = AnswerModel.objects.filter(test_id=test_id)
    
     
    if request.method=='POST':
        marks = request.POST.get('marks')
        name = request.POST.get('name')

        object = AnswerModel.objects.get(test_id=test_id, name=name)
        object.marks = marks
        object.save()
        return redirect('%s/%s' % (test_id,grading_id ))
    
    context['tests'] = tests
    return render(request,template_name,context)



@login_required(login_url='login_page')
def upload_excel(request):
    context={}
    template_name = 'upload-excel.html'

    form = ExcelForm()
    if request.method=='POST':
        #try:
        form=ExcelForm(request.POST,request.FILES)
        if form.is_valid():
            #print(request.FILES)
            #print(form)
            excel_file =  request.FILES.get('excel_file')
            print(excel_file)
            if (str(excel_file).split('.')[-1] == "xls"):
                data = xls_get(excel_file)#, column_limit=4)
            elif (str(excel_file).split('.')[-1] == "xlsx"):
                data = xlsx_get(excel_file)#, column_limit=4)
            else:
                return redirect('not excel file/')
            print(data)
            print(data['Sheet1']) # very very wrong!
            rows = data['Sheet1']
            print(type(rows))
            for i in rows[1:]:
                name = i[0]
                email = i[1]
                
                length = 8
                letters = string.ascii_letters
                password = ''.join(random.choice(letters) for i in range(length))
                print(password)
                
                StudentModel.objects.create(name=name,email=email,password=password)
            '''
            names = data["name"]
            emails = data["emails"]

            for i in range(1,names.len()):
                password = get_random_string(8)
                StudentModel.objects.create(name=names[i],email=emails[i],password=password)
            '''    
            return redirect('file_done/')
            #except MultiValueKeyDictKeyError:
             #   return redirect('keyerror/')
    
    context['form'] = form
    return render(request,template_name,context)


@login_required(login_url='login_page')
def upload_test_student(request):
    context={}
    template_name = 'upload_test_student.html'

    form = ExcelForm()
    if request.method=='POST':
        #try:
        form=ExcelForm(request.POST,request.FILES)
        if form.is_valid():
            #print(request.FILES)
            #print(form)
            excel_file =  request.FILES.get('excel_file')
            print(excel_file)
            if (str(excel_file).split('.')[-1] == "xls"):
                data = xls_get(excel_file)#, column_limit=4)
            elif (str(excel_file).split('.')[-1] == "xlsx"):
                data = xlsx_get(excel_file)#, column_limit=4)
            else:
                return redirect('not excel file/')
            print(data)
            print(data['Sheet1']) # very very wrong!
            rows = data['Sheet1']
            print(type(rows))
            for i in rows[1:]:
                #name = i[0]
                email = i[1]                
                
                StudentCheck.objects.create(email=email,test_id = form.cleaned_data['test_id'])
            '''
            names = data["name"]
            emails = data["emails"]

            for i in range(1,names.len()):
                password = get_random_string(8)
                StudentModel.objects.create(name=names[i],email=emails[i],password=password)
            '''    
            return redirect('studentCheck_file_done/')
            #except MultiValueKeyDictKeyError:
             #   return redirect('keyerror/')
    
    context['form'] = form
    return render(request,template_name,context)



def about_page(request):
    context = {}
    template_name = 'about.html'

    return render(request, template_name, context)   

def contact_page(request):
    context = {}
    template_name = 'contact.html'

    return render(request, template_name, context)   
    
     
