from rest_framework import routers, serializers, viewsets
from rest_framework.relations import PrimaryKeyRelatedField

from manger.models import Baby, Journal


class BabySerializer(serializers.ModelSerializer):
    class Meta:
        model = Baby
        fields = ('id', 'name', 'gender', 'birthday', 'photo', 'grade', 'is_study')


class BabyViewSet(viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer


class JournalSerializer(serializers.ModelSerializer):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    baby = PrimaryKeyRelatedField(queryset=Baby.objects.all())

    def validate(self, attrs):
        if (attrs.get('income_time') is None) ^ (attrs.get('income_escort') is None):
            raise serializers.ValidationError('"income_time" and "income_escort" must be determined simultaneously')

        if (attrs.get('outcome_time') is None) ^ (attrs.get('outcome_escort') is None):
            raise serializers.ValidationError('"income_time" and "outcome_escort" must be determined simultaneously')

        if (
            attrs.get('income_time') and
            attrs.get('outcome_time') and
            attrs['outcome_time'] < attrs['income_time']
        ):
            raise serializers.ValidationError('"outcome_time" should be later than "income_time"')

        return attrs

    def create(self, validated_data):
        if validated_data.get('outcome_time') and validated_data.get('income_time') is None:
            raise serializers.ValidationError('can not create outcome without income')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('outcome_time') and validated_data.get('income_time') is None:
            raise serializers.ValidationError('can not create outcome without income')

        return super().update(instance, validated_data)

    class Meta:
        model = Journal
        fields = ('id', 'baby', 'income_time', 'income_escort', 'outcome_time', 'outcome_escort')


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
