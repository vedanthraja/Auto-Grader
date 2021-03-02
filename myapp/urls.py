from django.urls import path
from . import views

urlpatterns = [
    # path('',views.test_view,name='test'),
    path('', views.home, name="home"),
    path('registerStudent/',views.RegisterStudent, name="RegisterStudent"),
    path('registerTeacher/',views.RegisterTeacher, name="RegisterTeacher"),
    path('index/',views.index, name="index"),
    path('login/',views.signin, name="login"),
    path('logout/',views.signout, name="logout"),
    path('dashboard_student/<str:pk>/',views.dashboard_student,name="dashboard_student"),
    path('dashboard_teacher/<str:pk>/',views.dashboard_teacher,name="dashboard_teacher"),
    path('<str:pk>/addquestion/', views.Addquestion, name="addquestion"),
    path('<str:pk>/addquiz/', views.Addquiz, name="addquiz"),
    path('<str:pk1>/<str:pk2>/', views.quiz_start, name="quiz_start"),
    path('<str:pk1>/<str:pk2>/<str:pk3>/', views.quiz_questions, name="quiz_questions"),
    path('dashboard_student/<str:pk1>/<str:pk2>/result', views.result, name="result")
]