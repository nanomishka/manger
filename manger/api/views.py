
from rest_framework import generics

from manger.api.serializers import JournalSerializer
from manger.models import Journal


class BabyStudyList(generics.ListAPIView):
    serializer_class = JournalSerializer

    def get_queryset(self):
        return Journal.objects.filter(baby__is_study=True)
