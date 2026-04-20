
from rest_framework import serializers

from examapp.models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserData
        #exclude=['password']
        fields='__all__'