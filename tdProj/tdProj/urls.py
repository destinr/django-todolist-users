from django.urls import include, path

urlpatterns = [
    path('', include('td_app.urls')),
]
