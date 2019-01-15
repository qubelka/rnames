from rest_framework import serializers
from .models import Name, Location

'''
Serializers -> JSON
Serializers -> validate data
'''

class NameSerializer(serializers.ModelSerializer):
#    nameCaption = serializers.CharField(source='name')
#    key = serializers.CharField(source='id')

    class Meta:
        model = Name
#        fields = ('key', 'name','created_on')
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields =[
            'name',
        ]

    def validate(self, data):
        content = data.get("name", None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None:
            raise serializers.ValidationError("Content is required.")
        return data
