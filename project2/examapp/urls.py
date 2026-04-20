from django.urls import path

from . import views

urlpatterns = [
    path('givemequestion/',views.giveMeQuestion),
    path('viewquestion/',views.viewQuestion),
    path('addquestion/',views.addQuestion),
    path('updatequestion/',views.updateQuestion),
    path('deletequestion/',views.deleteQuestion),
    path('givemeregister/',views.giveMeRegister),
    path('login/',views.login),
    path('register/', views.register),
    path('givemelogin/', views.giveMeLogin),
    path('nextquestion/',views.nextQuestion),
    path('previousquestion/',views.previousQuestion),
    path('starttest/',views.startTest),
    path('endexam/',views.endExam),
    path('senddata/',views.sendData),
    path('getuser/<uname>',views.getUser),
    path('getuser2/<uname>',views.getUser2),
    path('adduser/',views.addUser),
    path('updateuser/',views.updateUser),
    path('deleteuser/<uname>',views.deleteUser),
    path('getalluser/',views.getAllUser)
    
]
   