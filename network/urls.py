from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("profile/<int:useee>",views.profile,name="profile"),
    path("edited/<int:id>/<str:edited>",views.edited,name="edited"),
    path("follow/<int:user>",views.follow,name="follow"),
    path("following",views.following,name="following"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),



    #api routes
    path("pros/<int:id>",views.pros,name="pros")
]
