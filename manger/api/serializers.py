from rest_framework import routers, serializers, viewsets

from manger.models import Baby, Journal


class BabySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Baby
        fields = ('id', 'name', 'gender', 'birthday', 'photo', 'grade', 'is_study')


class BabySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=Baby.MAX_LENGTH_NAME)
    gender = serializers.ChoiceField(choices=Baby.GENDER_CHOICES)
    birthday = serializers.DateField()
    photo = serializers.CharField(max_length=Baby.MAX_LENGTH_PHOTO, required=False)
    grade = serializers.IntegerField(required=False)
    is_study = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        return Baby.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.is_study = validated_data.get('is_study', instance.is_study)

        instance.save()
        return instance


class BabyViewSet(viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer


class JournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Journal
        fields = ('id', 'baby_id', 'income_time', 'income_escort', 'outcome_time', 'outcome_escort')


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
