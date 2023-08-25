from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from chatapp.models import Registeration
from django.http import HttpResponse

#from .models import Conversation,Message
# Create your views here.

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
import openai



# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#from .models import Conversation, Message

# def send_message(request, conversation_id):
#     if request.method == 'POST':
#         conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
#         content = request.POST.get('content')
#         if content:
#             message = Message.objects.create(conversation=conversation, sender=request.user, content=content)

#             # Your logic to generate a response using ChatGPT goes here
#             response = generate_response(content)  # Replace with actual response generation logic

#             message.response = response
# #             message.save()

#             return JsonResponse({'message': message.content, 'response': message.response, 'sender': message.sender.username, 'timestamp': str(message.timestamp)})
#         else:
#             return JsonResponse({'error': 'Message content cannot be empty.'})








openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer














import PyPDF2

import os
from datetime import datetime,timedelta

import magic


from django.shortcuts import render, redirect
from .models import Conversation, Message
from .forms import ConversationForm

# def start_chat(request):
#     if request.method == 'POST':
#         form = ConversationForm(request.POST, request.FILES)
#         if form.is_valid():
#             conversation = form.save(commit=False)
#             conversation.user = request.user
#             conversation.save()
#             return redirect('chat_detail', conversation_id=conversation.id)
#     else:
#         form = ConversationForm()
    
#     return render(request, 'start_chat.html', {'form': form})

def check_file_type(file_path):
    mime = magic.Magic()
    file_type = mime.from_file(file_path)
    return file_type

def read_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        pdf_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

    return pdf_text





def chat_detail(request, conversation_id):
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
        # Other context data
    
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    previous = today - timedelta(days=2)  # Calculate yesterday's date
    
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    document_file=conversation.document.name
    print(document_file)
    file_path = os.path.join("media", document_file)
    detected_type = check_file_type(file_path)
    print(f"Typeeeeeeeeeeeeeee {detected_type}")
    #pdf_text = read_pdf(file_path)
    #print(pdf_text)
    if request.method == 'POST':
        form_type= request.POST.get('form_type')
        if form_type == 'chat_form':
            form = ConversationForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                conversation = form.save(commit=False)
                conversation.user = request.user
                conversation.chat_title =title
                conversation.save()
                return redirect('chat_detail', conversation_id=conversation.id)
    else:
        form = ConversationForm()
        user = request.user
        conversations = Conversation.objects.filter(user=user)
    
    if request.method == 'POST':
          user_message = request.POST.get('message')
          response=ask_openai(user_message)
          
          if user_message:
                message = Message.objects.create(
                conversation=conversation,
                text=user_message,
                response=response,
                is_user_message=True
             )
                return JsonResponse({'message':user_message, 'response':response})
            # Call ChatGPT API to generate AI response and create a message
            # Save AI-generated response message
            # messages.append(message)  # Add the AI-generated message to the list
    
    return render(request, 'tester.html', {'conversations': conversations,'conversation': conversation, 'messages': messages,'form': form, 'today':today, 'yesterday':yesterday,'active_conversation_id':active_conversation_id})

def conversations_list(request):
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    
    return render(request, 'conversations_list.html', {'conversations': conversations})

def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.method == 'POST':
        conversation.delete()
        return redirect('start_chat')  # Redirect to a relevant page after deletion
    
    return render(request, 'delete_conversation.html', {'conversation': conversation})








def home(request):
    #chats = Message.objects.filter(user=request.user)
    # if request.method == 'POST':
    #     message = request.POST.get('message')
    #     response = ask_openai(message)
    #     chat= Message(user=request.user, content=message, response=response, sent_at=timezone.now())
    #     chat.save()
    #     return JsonResponse({'message':message, 'response':response})
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    print(f"today is {today}")
    print(f"yesterday was {yesterday}")
    if request.method == 'POST':
        dtypes= request.POST.get('form_type')
        print(dtypes)
        form = ConversationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.chat_title =title
            conversation.save()
            return redirect('chat_detail', conversation_id=conversation.id)
    else:
        form = ConversationForm()
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    return render(request, 'home.html',{'conversations': conversations,'form': form,'today':today,'yesterday':yesterday})

# def message_list(request, conversation_id):
#     # conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
#     # messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
#     conversations = Conversation.objects.all()
#     conversation = get_object_or_404(Conversation, pk=conversation_id)
#     messages = Message.objects.filter(conversation=conversation)
    
#     return render(request, 'tester.html', {'conversations': conversations,'conversation': conversation, 'messages': messages})

def register(request):
    return render(request, "auth-register.html")


def loginpage(request):
    return render(request, "auth-login.html")


# Authentication APIs
def handlesignup(request):
    if request.method=="POST":
        print("got it")
        #get the post parameters
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        
        # Check for errorneous inputs
        #username should be under 10
        if len(username)>10:
            messages.warning(request,"Username must be under 10 characters")
            return redirect('registeration')
        if password1 != password2:
            messages.warning(request,"Password do not match")
            return redirect('registeration')
        #Create the user


        registeration = Registeration(user_name=username, first_name=fname,last_name=lname, user_email=email,user_password=password1)
        registeration.save()
        messages.success(request,"Your account is created")
        return redirect('login-page')   

    else:
        messages.warning(request,"Enter all the missing values")
        return redirect('registeration')
        
    #     # Check for errorneous inputs
    #     #username should be under 10
    #     if len(username)>10:
    #         messages.warning(request,"Username must be under 10 characters")
    #         return redirect('registeration')
    #     if password1 != password2:
    #         messages.warning(request,"Password do not match")
    #         return redirect('registeration')
    #     #Create the user
    #     myuser= Registeration.objects.create_user(username,email,password1)
    #     myuser.first_name=fname
    #     myuser.last_name=lname
    #     myuser.save()
        
    #     



def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user= authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect('home')
            messages.success(request,"Successfully Logged In")
            
        else:
            messages.warning(request,"Invalid Credentials , Please try again")
            return redirect('login-page')


def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged out")
    return redirect('login-page')



def approve_user(request, user_id):
    user_for_approval=Registeration.objects.get(user_id=user_id)

    username = user_for_approval.user_name
    email = user_for_approval.user_email
    password = user_for_approval.user_password
    
    # Create the user
    newuser = User.objects.create_user(username, email, password)
    newuser.first_name= user_for_approval.first_name
    newuser.last_name= user_for_approval.last_name
    newuser.id
    newuser.save()
    approved_user=Registeration.objects.get(user_id=user_id)
    approved_user.delete()
    messages.success(request, " User Approved")
    return redirect('admin-panel')

def delete_applicant(request,user_id):
    approved_user=Registeration.objects.get(user_id=user_id)
    approved_user.delete()
    messages.success(request, "Application Deleted")
    return redirect('admin-panel')

def delete_user(request,id):
    delete_user=User.objects.get(id=id)
    delete_user.delete()
    messages.success(request, "Application Deleted")
    return redirect('admin-panel')




def chatbot_view(request, conversation_id=None):
   conversations = Message.objects.values('user', 'sent_at').distinct()
   if conversation_id:
        selected_conversation = Message.objects.filter(user=request.user, id=conversation_id)
   else:
        selected_conversation = None
         
   return render(request, 'tester.html', {
        'conversations': conversations,
        'selected_conversation': selected_conversation
    })


def convert_bytes_to_human_readable(bytes):
    # Define the suffixes for KB, MB, GB, etc.
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']

    # Determine the appropriate suffix and scale the size down
    index = 0
    while bytes >= 1024 and index < len(suffixes) - 1:
        bytes /= 1024
        index += 1

    # Format the size with the determined suffix
    size_formatted = "{:.2f} {}".format(bytes, suffixes[index])
    return size_formatted
def adminlogin(request):
    registration_list=Registeration.objects.all()
    document_files = Conversation.objects.all()
    file_info_list = []
    
    for conversation in document_files:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        
       
        user = conversation.user
        chat = conversation.chat_title
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable}
        file_info_list.append(conversation_info)
        
    user_list=User.objects.all()
    
    params={'registration_list':registration_list, 'user_list':user_list,'file_names': file_info_list}
    return render(request, "admin-panel.html",params)

