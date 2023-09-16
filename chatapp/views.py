from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from chatapp.models import Registeration,Admin
from django.http import HttpResponse
from django.core.mail import send_mail
import PyPDF2
import os
from datetime import datetime,timedelta
from django.contrib.auth.views import PasswordChangeView

from django.shortcuts import render, redirect
from .models import Conversation, Message
from .forms import ConversationForm, PasswordChangingForm
#from .models import Conversation,Message
# Create your views here.

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
import openai
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required












from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Conversation, Message





def chat_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat_list.html', {'conversations': conversations})


def get_chat_messages(request, conversation_id):
    print('yes')
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    print(f'messages {messages}')
    # Serialize the messages data
    message_data = [{'user': message.text, 'content': message.response, 'created_at': message.created_at} for message in messages]

    return JsonResponse({'messages': message_data})








# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse



import os
#os.environ['OPENAI_API_KEY'] =

# openai_api_key = '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'
# openai.api_key = openai_api_key

# def ask_openai(message):
#     response = openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an helpful assistant."},
#             {"role": "user", "content": message},
#         ]
#     )
    
#     answer = response.choices[0].message.content.strip()
#     return answer

from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.llms import OpenAI
import textwrap
from langchain.chat_models import ChatOpenAI
import os

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import PromptTemplate, FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import os
from langchain.document_loaders import CSVLoader
from langchain.chains.conversation.memory import ConversationBufferMemory
import chardet

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import os
from langchain.prompts import PromptTemplate
import dotenv

dotenv.load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')




#Text wrapping code
def print_wrapped_text(text, line_width=80):
    wrapped_text = textwrap.fill(text, width=line_width)
    return wrapped_text

#Read Pdf code
def read_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        pdf_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

    return pdf_text



#Encoding detection code
def detect_csv_encoding(file_path):
    # Detect the encoding of the CSV file
    with open(file_path, "rb") as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    return result["encoding"]

#Csv Memory Loading to keep History
csv_memory = ConversationBufferMemory(memory_key='chat_history', k=10, return_messages=True, output_key='answer')

#Code to chat with a Csv File
def datachat_process_csv(file_path,user_message):
    os.environ['OPENAI_API_KEY'] = "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"
    encoding = detect_csv_encoding(file_path)
    print(encoding)

    loader = CSVLoader(file_path=file_path, encoding=encoding)
    data = loader.load()
    length = len(data)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embeddings)

    prompt_template = """you are helpful assistant for my documents.
        {context}
        Question:{question}
        Thought: I should look at the data in the csv file to see what I can query based on the question and history.  
        Answer here:"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo-16k"),
        # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        # verbose=True,
        memory=csv_memory,
        retriever=vectorstore.as_retriever(search_kwargs={"k": length}),
        combine_docs_chain_kwargs={"prompt": PROMPT},
       )

    response = chain({"question": user_message})
    answer = response['answer']
    return answer






#Code to chat with a Text File

def datachat_process_text(file_path,user_message):
    loader= TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    docsearch = Chroma.from_documents(texts, embeddings)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    prompt_template = """you are helpful assistant for my documents.
    {context}
    Question:{question}
    Answer here:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        memory=memory,
        retriever=docsearch.as_retriever(),
        combine_docs_chain_kwargs={"prompt": PROMPT},
    )
    response = qa.run(question=user_message)
    print(f" Memory data:  {memory.load_memory_variables({})}")
    return print_wrapped_text(response)


# Code to chat with a PDF file
def datachat_process_pdf(file_path,user_message):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
        )
    chunks = text_splitter.split_text(text=text)
    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages=True , output_key = 'answer')

    prompt_template="""you are helpful assistant for my documents.
    {context}
    Question:{question}
    Answer here:"""
    PROMPT= PromptTemplate(
        template=prompt_template, input_variables=["context","question"]
    )
    chain_type_kwargs={"prompt":PROMPT}
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        memory=memory,
        retriever=VectorStore.as_retriever(),
        combine_docs_chain_kwargs={"prompt":PROMPT},
     )
    response = qa.run(question=user_message)
    return print_wrapped_text(response)


#Code to detect File Type
def detect_file_type(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    if file_extension == '.pdf':
        return 'pdf'
    elif file_extension == '.txt':
        return 'text'
    elif file_extension == '.csv':
        return 'csv'
    else:
        return 'unknown'



#Code to select specific chat option based on the file type
def datachat(file_path, user_message):
    file_type = detect_file_type(file_path)
    print(f"file type {file_type}")
    
    if file_type == 'pdf':
        return datachat_process_pdf(file_path, user_message)
    elif file_type == 'text':
        return datachat_process_text(file_path, user_message)
    elif file_type == 'csv':
        return datachat_process_csv(file_path, user_message)
    else:
        return "Unsupported file type. Please provide a PDF, text, or CSV file."



def chat_detail(request, conversation_id):
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
        # Other context data
    
    file_list = []
    user = request.user
    conversations = Conversation.objects.filter(user=user)

    for conversation in conversations:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    previous = today - timedelta(days=2)  # Calculate yesterday's date
    
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    document_file = conversation.document.name
    file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
    chat_file_size = convert_bytes_to_human_readable(file_size)
    filename = os.path.basename(document_file)
    file_path = os.path.join("media", document_file)
    print(f'type {file_path}')
        
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
          response=datachat(file_path,user_message)
                   
          if user_message:
                message = Message.objects.create(
                conversation=conversation,
                text=user_message,
                response=response,
                is_user_message=True
             )
                return JsonResponse({'message':user_message, 'response':response})
            
    
    return render(request, 'tester.html', {'conversations': conversations,'conversation': conversation, 'messages': messages,'form': form, 'today':today, 'yesterday':yesterday,'active_conversation_id':active_conversation_id, 'document_file':filename,'file_list':file_list, 'chat_file_size':chat_file_size})

def conversations_list(request):
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    
    return render(request, 'conversations_list.html', {'conversations': conversations})



#Chat deletion codes
#Delete chat from the main menu
# def delete_conversation(request, conversation_id):
#     conversation = get_object_or_404(Conversation, id=conversation_id) 
#     if request.method == 'POST':
#         conversation.delete()
#         return redirect('home')  # Redirect to a relevant page after deletion


def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == 'POST':
        # Delete attached document
        if conversation.document:  # Check if a document is attached
            # Delete the document file from the media folder
            if os.path.exists(conversation.document.path):
                os.remove(conversation.document.path)
        
        conversation.delete()
        return redirect('home') 


#Delete chat from top right menu
def user_delete_chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.delete()
    return redirect('home')  # Redirect to a relevant page after deletion
    
   



#User Main page after login
@login_required
def home(request):
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    #File upload form request
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
# file detail handling name and type
    file_list = []
    for conversation in conversations:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    return render(request, 'home.html',{'conversations': conversations,'form': form,'today':today,'yesterday':yesterday,'file_list':file_list})

# def message_list(request, conversation_id):
#     # conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
#     # messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
#     conversations = Conversation.objects.all()
#     conversation = get_object_or_404(Conversation, pk=conversation_id)
#     messages = Message.objects.filter(conversation=conversation)
    
#     return render(request, 'tester.html', {'conversations': conversations,'conversation': conversation, 'messages': messages})


#User Main signup

def register(request):
    return render(request, "auth-register.html")

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
        messages.warning(request,"Registration Request Submitted,\n Kindly Wait For Approval")
        return redirect('login-page')   

    else:
        messages.warning(request,"Enter all the missing values")
        return redirect('registeration')

#User Main login

def loginpage(request):
    return render(request, "auth-login.html")


def handleuserlogin(request):
   if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user= authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
            
        else:
            messages.warning(request,"Invalid Credentials , Please try again")
            return redirect('login-page')


#User Logout

def user_logout(request):
    logout(request)
    messages.success(request,"Successfully Logged out")
    return redirect('login-page')



#Admin Approval

def approve_user(request, user_id):
    user_for_approval=Registeration.objects.get(user_id=user_id)

    username = user_for_approval.user_name
    name = user_for_approval.first_name
    email = user_for_approval.user_email
    password = user_for_approval.user_password
    # Send Email
     # Send email to the user
    user_email = email  # Get the user's email from your database
    subject = "Your Registration Request is Approved"
    message = f"Dear {name},\nWe are pleased to inform you that your registration request has been approved by Datachat. We welcome you to our platform and are excited to have you on board.\nWith your registration approved, you can now fully utilize Datachat to engage in meaningful conversations with your data. Whether it's analyzing trends, making informed decisions, or gaining insights, Datachat is here to empower you every step of the way.\nYour journey with Datachat has just begun. We encourage you to explore the features, connect with our community, and discover the vast potential that data-driven conversations can offer. Should you have any questions or need assistance, our support team is readily available to assist you.\nOnce again, congratulations on becoming a part of the Datachat family. We look forward to witnessing your data journey and the value you'll bring to our platform."
    from_email = 'faranpeerzada253@gmail.com'  # Sender's email (same as EMAIL_HOST_USER)
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    # Create the user
    newuser = User.objects.create_user(username, email, password)
    newuser.first_name= user_for_approval.first_name
    newuser.last_name= user_for_approval.last_name
    newuser.id
    newuser.save()
    approved_user=Registeration.objects.get(user_id=user_id)
    approved_user.delete()
    return redirect('admin-panel')

#Admin Delete Registered Applicant

def delete_applicant(request,user_id):
    approved_user=Registeration.objects.get(user_id=user_id)
    approved_user.delete()
    messages.success(request, "Application Deleted")
    return redirect('admin-panel')

#Admin Delete Approved User

def delete_user(request,id):
    delete_user=User.objects.get(id=id)
    delete_user.delete()
    messages.success(request, "Application Deleted")
    return redirect('admin-panel')




# def chatbot_view(request, conversation_id=None):
#    conversations = Message.objects.values('user', 'sent_at').distinct()
#    if conversation_id:
#         selected_conversation = Message.objects.filter(user=request.user, id=conversation_id)
#    else:
#         selected_conversation = None
         
#    return render(request, 'tester.html', {
#         'conversations': conversations,
#         'selected_conversation': selected_conversation
#     })


def adminlogin(request):
    return render(request, "admin-login.html")




def handleadminlogin(request):
    user = Admin.objects.get(admin_id=1)
    print(f"usersss {user}{user.admin_id}  ")
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
         
        
        # Check if the provided email and password match the admin credentials
        if loginusername == user.admin_name and loginpassword == user.admin_password:
            authenticated_user = authenticate(username=loginusername, password=loginpassword)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('admin-panel')
            else:
                messages.warning(request, "Authentication Failed")
        else:
             messages.warning(request, "Invalid Credentials, Please try again")
            
    return redirect("admin-login")



def admin_logout(request):
    logout(request)
    messages.success(request,"Successfully Logged out")
    return render(request, "admin-login.html")
   


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


@login_required
def adminpanel(request):
    admin = Admin.objects.get(admin_id=1)
    registration_list=Registeration.objects.all()
    conversations = Conversation.objects.all()
    
    document_files=conversations
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    
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
    
    
    params={'registration_list':registration_list, 'user_list':user_list,'file_names': file_info_list, 'admin':admin,"conversations":conversations,'today':today,'yesterday':yesterday}
    return render(request, "admin-panel.html",params)



def user_chats_detail(request,user_id):
    admin = Admin.objects.get(admin_id=1)
    registration_list=Registeration.objects.all()
    conversations = Conversation.objects.all()
    document_files=conversations
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    user_list=User.objects.all()
    selected_user = User.objects.get(id=user_id)
    
#file detail handling of all the users
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
    
    
#file detail handling of the specific selected user
    user_chats = Conversation.objects.filter(user=selected_user)
    file_list = []
    for conversation in user_chats:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    return render(request, 'user-chats-detail.html',{'registration_list':registration_list, 'user_list':user_list,'file_names': file_info_list, 'admin':admin,'conversations': user_chats,'today':today,'yesterday':yesterday,'file_list':file_list,'selected_user':selected_user})





def userchatview(request, conversation_id,user_id):
    admin = Admin.objects.get(admin_id=1)
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
    active_conversation_title=active_conversation.chat_title
    registration_list=Registeration.objects.all()
    selected_user = User.objects.get(id=user_id)
    print(selected_user)
    print(active_conversation_title)
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
        # Other context data
    
    file_list = []
    #user = user
    conversations = Conversation.objects.filter(user=selected_user)

    for conversation in conversations:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
     
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    # user = request.user
    # conversations = Conversation.objects.filter(user=user)
    document_file = conversation.document.name
    
    file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
    chat_file_size = convert_bytes_to_human_readable(file_size)
    print(chat_file_size)
    filename = os.path.basename(document_file)
    file_path = os.path.join("media", document_file)
    # # detected_type = check_file_type(file_path)
    # # print(f"Typeeeeeeeeeeeeeee {detected_type}")
    # #pdf_text = read_pdf(file_path)
    # #print(pdf_text)
    conversations = Conversation.objects.all()
    
    document_files=conversations
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    
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
        
    print(f'filenamessss {file_info_list}')
    if request.method == 'POST':
          user_message = request.POST.get('message')
          response=ask_openai(user_message)
          print(user_message)
          
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
    conversation = Conversation.objects.get(id=conversation_id)

    return render(request, 'user-chats-view.html',{'registration_list':registration_list,'admin':admin,'file_names':file_info_list, 'conversations': conversations,'selected_user':selected_user,'conversation': conversation, 'messages': messages,'today':today, 'yesterday':yesterday,'active_conversation_id':active_conversation_id, 'document_file':filename,'file_list':file_list, 'chat_file_size':chat_file_size})

def adminchats(request,conversation_id):
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
    
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    admin = Admin.objects.get(admin_id=1)
    registration_list=Registeration.objects.all()
    conversations = Conversation.objects.all()
    
    document_files=conversations
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    
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
    conversation = Conversation.objects.get(id=conversation_id)
    document_file = conversation.document.name
    document_file = os.path.basename(document_file)
    
    file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
    user_list=User.objects.all()
    chat_file_size = convert_bytes_to_human_readable(file_size)
    params={'chat_file_size':chat_file_size,'document_file':document_file,'conversation':conversation,'active_conversation_id':active_conversation_id,'messages':messages,'registration_list':registration_list, 'user_list':user_list,'file_names': file_info_list, 'admin':admin,"conversations":conversations,'today':today,'yesterday':yesterday}
    
    return render(request, 'admin-panel.html',params)
    

def handling404(request,exception):
    return render(request,'404.html',{})
from django.urls import reverse_lazy


class PasswordChangeView(PasswordChangeView):
    template_name ="auth-changepassword.html"
    success_url = reverse_lazy('password_success')

def password_success(request):
    logout(request)
    messages.warning(request, "Password Changed!, Please try again using New Password")
           
    return redirect('login-page')