
from django.contrib import admin
from django.urls import path
from .views import home_view,about_view
from auth import views as auth_views
urlpatterns = [
  path("",home_view),
  path('about/',about_view),
  path('login/',auth_views.login_view),
  path('register/',auth_views.register_view),
   path('hello-world/',home_view),
   path('hello-world.html/',home_view),
    path("admin/", admin.site.urls),
    ]
