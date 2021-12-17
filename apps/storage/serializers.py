from rest_framework import serializers

from apps.storage.models import *

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageFacility
        fields = '__all__'

    def create(self):
        StorageFacility.objects.create(**self.validated_data)

class UpdateStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageFacility
        fields = ['name']

    def update(self,instance):
        instance.name = self.validated_data['name']
        instance.save()
        return instance