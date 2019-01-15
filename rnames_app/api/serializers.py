
from rest_framework.serializers import (
#    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    )
from rnames_app.models import Location, Name, Reference

'''
Serializers -> JSON
Serializers -> validate data
'''

class LocationSerializer(ModelSerializer):
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


class NameSerializer(ModelSerializer):
#    nameCaption = serializers.CharField(source='name')
#    key = serializers.CharField(source='id')

    class Meta:
        model = Name
#        fields = ('key', 'name','created_on')
        fields = '__all__'


class ReferenceCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Reference
        fields = [
            'id',
            'first_author',
            'year',
            'title',
            'link',
            'created_by',
            'created_on',
        ]

class ReferenceDetailSerializer(ModelSerializer):

    class Meta:
        model = Reference
        fields = [
            'id',
            'first_author',
            'year',
            'title',
            'link',
            'created_by',
            'created_on',
        ]

class ReferenceListSerializer(ModelSerializer):

    created_by = SerializerMethodField()
    modified_by = SerializerMethodField()

    class Meta:
        model = Reference
        fields = [
            'id',
            'first_author',
            'year',
            'title',
            'link',
            'modified_by',
            'created_by',
            'created_on',
        ]

    def get_created_by(self, obj):
        try:
            created_by = obj.created_by.first_name
        except:
            created_by = None
        return str(created_by)

    def get_modified_by(self, obj):
        return str(obj.modified_by.last_name)
