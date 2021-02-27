from django.urls import path
from . import views

urlpatterns = [
    path('',views.test_view,name='test'),
    path('registerStudent/',views.RegisterStudent, name="RegisterStudent"),
    path('registerTeacher/',views.RegisterTeacher, name="RegisterTeacher"),
    path('index/',views.index, name="index"),
    path('login/',views.signin, name="login")
]