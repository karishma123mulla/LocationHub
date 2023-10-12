from rest_framework import serializers
from .models import *


class T_Location_Serializer(serializers.ModelSerializer):

    class Meta:
        model = LocationHub
        fields = '__all__'