from django.urls import include, path

urlpatterns = [
    path('', include('manger.api.urls')),
]
