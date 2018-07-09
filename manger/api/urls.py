from django.urls import include, re_path, path
from rest_framework import routers

from manger.api.serializers import BabyViewSet, JournalViewSet
from manger.api.views import BabyStudyList

router = routers.DefaultRouter()
router.register('babies', BabyViewSet)
router.register('journal', JournalViewSet)

urlpatterns = [
    path('journal/study/', BabyStudyList.as_view(), name='journal-study'),
    re_path('^', include(router.urls)),

]
