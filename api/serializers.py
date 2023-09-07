# ? Packages
from rest_framework import serializers
# ? Models
from account.models import User
from base.models import Car, CarReports, Gallery, WeSellYouWin, DemandList

# ? Users Serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["f_name", "phone", "address", "date_joined"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password', 'write_only': True})

    class Meta:
        model = User
        fields = ['f_name', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# ? Posting Car Serializers
class AddCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = '__all__'


# ? add Gallery Field in car responce
class GallerySerializerForCar(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ('image',)


class CarSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"

    def get_gallery(self, obj):
        gallery_images = obj.gallery_set.all()
        gallery_urls = [image.image.url for image in gallery_images]
        return gallery_urls

# ? Reporting Cars


class CarReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarReports
        fields = "__all__"


class WeSellYouWinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeSellYouWin
        fields = '__all__'


class DemandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemandList
        fields = '__all__'
