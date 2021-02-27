from django.urls import path
from . import views

urlpatterns = [
    path('',views.test_view,name='test'),
    path('registerStudent/',views.RegisterStudent, name="RegisterStudent"),
    path('registerTeacher/',views.RegisterTeacher, name="RegisterTeacher"),
    path('index/',views.index, name="index"),
    path('login/',views.signin, name="login"),
    path('dashboard_student/<str:pk>/',views.dashboard_student,name="dashboard_student"),
    path('<str:pk1>/<str:pk2>/', views.quiz_start, name="quiz_start"),
    path('<str:pk1>/<str:pk2>/<str:pk3>', views.quiz_questions, name="quiz_questions")
]