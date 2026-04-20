from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from examapp.models import Question, Result, UserData
from examapp.serializers import UserDataSerializer

# Create your views here.
next=-1

@api_view(['GET'])
def sendData(request):
    return HttpResponse("{'id':101,'name':'Ravi'}")

@api_view(['GET'])
def getUser(request,uname):
    #select * from userdata where username=uname
    userdb=UserData.objects.get(username=uname)
    response=Response({"username":userdb.username,"password":userdb.password,"phno":userdb.phno})
    return response

@api_view(['GET'])
def getUser2(request,uname):
    #select * from userdata where username=uname
    userdb=UserData.objects.get(username=uname)
    userserializer=UserDataSerializer(userdb)
    response=Response(userserializer)
    return response

@api_view(['POST'])
def addUser(request):
    userfromclient=request.data
    UserData.objects.create(username=userfromclient['username'],password=userfromclient['password'],phno=userfromclient['phno'])
    response=Response(userfromclient)
    return response

@api_view(['PUT'])
def updateUser(request):
    userfromclient=request.data
    userdb=UserData.objects.get(username=userfromclient['username'])
    userdb.phno=userfromclient['phno']
    userdb.password=userfromclient['password']
    userdb.save()
    response=Response(userfromclient)
    return response

@api_view(['DELETE'])
def deleteUser(request,uname):
    UserData.objects.filter(username=uname).delete()
    responses=Response('Data deleted')
    return responses

@api_view(['GET'])
def getAllUser(request):
    queryset=UserData.objects.all().values()
    listofusers=list(queryset)
    return Response(listofusers)

def giveMeQuestion(request):
    return render(request,'examapp/templates/questionform.html')

def viewQuestion(request):
    nofrombrowser=request.GET['qno']
    qdata=Question.objects.get(qno=nofrombrowser)
    return render(request,'examapp/templates/questionform.html',{'questiondata':qdata})

def addQuestion(request):
    no=request.GET['qno']
    que=request.GET['qtext']
    ans=request.GET['answer']
    op1=request.GET['op1']
    op2=request.GET['op2']
    op3=request.GET['op3']
    op4=request.GET['op4']
    subject=request.GET['subject']
    Question.objects.create(qno=no,qtext=que, subject=subject,answer=ans,op1=op1,op2=op2,op3=op3,op4=op4)
    return render(request,'examapp/templates/questionform.html',{'message':'question added successfully'})

def updateQuestion(request):
    qdb=Question.objects.filter(qno=request.GET['qno'],subject=request.GET['subject'])
    qdb.update(qno=request.GET['qno'],qtext=request.GET['qtext'], subject=request.GET['subject'],answer=request.GET['answer'],op1=request.GET['op1'],op2=request.GET['op2'],op3=request.GET['op3'],op4=request.GET['op4'])
    return render(request,'examapp/templates/questionform.html',{'message':'question updated successfully'})

def deleteQuestion(request):
    Question.objects.filter(qno=request.GET['qno'],subject=request.GET['subject']).delete()
    print(connection.queries)
    return render(request,'examapp/templates/questionform.html',{'message':'question deleted successfully'})

def giveMeLogin(request):
    return render(request, "examapp/templates/login.html")

def giveMeRegister(request):
    return render(request, "examapp/templates/registration.html")

def register(request):
    userfrombrowser=request.GET['username'] #aaa
    pswrdfrombrowser=request.GET['password'] #aaa123
    phnofrombrowser=request.GET['phno'] #12345

    #the create method helps us to create an insert query
    UserData.objects.create(username=userfrombrowser,password=pswrdfrombrowser,phno=phnofrombrowser)
    print(connection.queries)
    #insert into userdata(username,password,mobno)values(userfrombrowser,pswdfrombrowser,mobnofrombrowser)
    return render(request,"examapp/templates/login.html",{"message":"You are registered successfully"})

def login(request):
    uname=request.GET["username"] #abc
    pswrd=request.GET["password"] #abc123
    request.session['usrnmdata']=uname   #abc
   
    try:
        # it is writing a select query to select the data from the table 
        # in return it is getting an object
        userobj=UserData.objects.get(username=uname)
        # select * from userdata where username=uname
    except:
        return render(request,"examapp/templates/login.html",{"message":"Wrong username"})
    if userobj.password==pswrd:
         request.session['answer']={}
         request.session['score']=0
         request.session['qno']=0
        #  queryset=Question.objects.filter(subject='maths').values()
        #  listofquestions=list(queryset)
        #  request.session['listofquestions']=listofquestions
         return render(request,"examapp/templates/subject.html",{"message":"You have logged in successfully. Welcome "+uname})
    else:
        #we will give him wrong input message and stay page
        return render(request,"examapp/templates/login.html",{"message":"Wrong password"})
    
def nextQuestion(request):
    # global next
    # next=next+1
    # print(next)
    allquestions=request.session['listofquestions']
    questionindex=request.session['qno']

    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswers[1]=[1,2+2,4,7]
        #{1:[1,2+2,4,7],2:[2,4+5,9,4]}
    
    if(questionindex<len(allquestions)-1):
       request.session['qno']=request.session['qno']+1
       quesstion=allquestions[request.session['qno']]
    else:
       return render(request,'examapp/templates/questionnavigation.html',{'message':'Click on Previous or End Exam'})
    return render(request,'examapp/templates/questionnavigation.html',{'question':quesstion})

def previousQuestion(request):
    allquestions=request.session['listofquestions']
    questionindex=request.session['qno']
    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswers[1]=[1,2+2,4,7]
        #{1:[1,2+2,4,7],2:[2,4+5,9,4]}

    if (questionindex>0):
        request.session['qno']=request.session['qno']-1
        quesstion=allquestions[request.session['qno']]
    else:
       return render(request,'examapp/templates/questionnavigation.html',{'message':'Click on next'})
    return render(request,'examapp/templates/questionnavigation.html',{'question':quesstion})
    


def startTest(request):
    queryset=Question.objects.filter(subject=request.GET['subject']).values()
    listofquestions=list(queryset)
    request.session['listofquestions']=listofquestions
    request.session['subject']=request.GET['subject']
    return render(request,'examapp/templates/questionnavigation.html',{'question':listofquestions[0]})

def endExam(request):
    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswers[1]=[1,2+2,4,7]
        #{1:[1,2+2,4,7],2:[2,4+5,9,4]}

        responses=request.session['answer']
        allresponses=responses.values()

        for ans in allresponses:
            print(f'The correct answer is {ans[2]} and the user gave {ans[3]}')
            if ans[2]== ans[3]:
                request.session['score']=request.session['score']+1
            finalscore=request.session['score']
    try:
        Result.objects.create(username=request.session['usrnmdata'],subject=request.session['subject'],marks=request.session['score'])
        return render(request,'examapp/templates/score.html',{'finalscore':finalscore,'responses':allresponses})
    except:
        return render(request,'examapp/templates/login.html',{'message':'use different user'})