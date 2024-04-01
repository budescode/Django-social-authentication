from django.urls import path
from .import views 
app_name = "userurl"

urlpatterns = [
    path("", views.signin_view, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("facebook", views.facebook_signin, name="facebook"),
    path("linkedin", views.linked_in_oauth, name="linkedin"),
    path("github", views.github_signin, name="github"),
    path("google", views.google_signin, name="google"),
    

]