
from rest_framework.serializers import (
#    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    )
from rnames_app.models import Location, Name, Reference, Relation, Location

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
            'created_by',
            'created_on',
            'modified_by',
        ]

    def get_created_by(self, obj):
        try:
            created_by = obj.created_by.first_name
        except:
            created_by = None
        return str(created_by)

    def get_modified_by(self, obj):
        return str(obj.modified_by.last_name)

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

class RelationListSerializer(ModelSerializer):
#    year = ReferenceDetailSerializer()
    reference_id = SerializerMethodField()
    reference_year = SerializerMethodField()
    level_1 = SerializerMethodField()
    level_2 = SerializerMethodField()
    name_1 = SerializerMethodField()
    name_2 = SerializerMethodField()
    locality_name_1 = SerializerMethodField()
    locality_name_2 = SerializerMethodField()
    qualifier_name_1 = SerializerMethodField()
    qualifier_name_2 = SerializerMethodField()
    strat_qualifier_1 = SerializerMethodField()
    strat_qualifier_2 = SerializerMethodField()

    class Meta:
        model = Relation
        fields = [
            'id',
            'reference_id',
            'reference_year',
            'name_1',
            'qualifier_name_1',
            'strat_qualifier_1',
            'level_1',
            'locality_name_1',
            'name_2',
            'qualifier_name_2',
            'strat_qualifier_2',
            'level_2',
            'locality_name_2',
#            'belongs_to',
        ]
#        fields = '__all__'
#        read_only_fields = [
#            'reference',
#            'name_1',
#            'name_2',
#            'locality_name_1',
#            'locality_name_2',
#        ]
#        depth = 4
    def get_level_1(self, obj):
        try:
            level_1 = obj['name_one__qualifier__level']
        except:
            level_1 = None
        return str(level_1)

    def get_level_2(self, obj):
        try:
            level_2 = obj['name_two__qualifier__level']
        except:
            level_2 = None
        return str(level_2)

    def get_locality_name_1(self, obj):
        try:
            locality_name_1 = obj['name_one__location__name']
        except:
            locality_name_1 = None
        return str(locality_name_1)

    def get_locality_name_2(self, obj):
        try:
            locality_name_2 = obj['name_two__location__name']
        except:
            locality_name_2 = None
        return str(locality_name_2)

    def get_name_1(self, obj):
        try:
            name_1 = obj['name_one__name__name']
        except:
            name_1 = None
        return str(name_1)

    def get_name_2(self, obj):
        try:
            name_2 = obj['name_two__name__name']
        except:
            name_2 = None
        return str(name_2)

    def get_qualifier_name_1(self, obj):
        try:
            qualifier_name_1 = obj['name_one__qualifier__qualifier_name__name']
        except:
            qualifier_name_1 = None
        return str(qualifier_name_1)

    def get_qualifier_name_2(self, obj):
        try:
            qualifier_name_2 = obj['name_two__qualifier__qualifier_name__name']
        except:
            qualifier_name_2 = None
        return str(qualifier_name_2)

    def get_strat_qualifier_1(self, obj):
        try:
            strat_qualifier_1 = obj['name_one__qualifier__stratigraphic_qualifier__name']
        except:
            strat_qualifier_1 = None
        return str(strat_qualifier_1)

    def get_strat_qualifier_2(self, obj):
        try:
            strat_qualifier_2 = obj['name_two__qualifier__stratigraphic_qualifier__name']
        except:
            strat_qualifier_2 = None
        return str(strat_qualifier_2)

    def get_reference_id(self, obj):
        try:
            reference_id = obj['reference']
        except:
            reference_id = None
        return str(reference_id)

    def get_reference_year(self, obj):
        try:
            reference_year = obj['reference__year']
        except:
            reference_year = None
        return str(reference_year)
