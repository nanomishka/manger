from django.urls import include, re_path
from rest_framework import routers

from manger.api.serializers import BabyViewSet, JournalViewSet

router = routers.DefaultRouter()
router.register('babies', BabyViewSet)
router.register('journal', JournalViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]
