from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only = True)
    isAdmin = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone",

            "social_number",
            "driving_license",
            "citizen_status",
            "marital_status",

            "profile_image",
            "street_number",
            "street_name",
            "postal_code",
            "town",
            "province",
            "country",
            "created_at",

            "is_active",
            "is_superuser",
            "is_staff",
            "isAdmin",
            "is_worker",
            "is_job_owner"
        ]

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_user_id(self,obj):
        return obj.id

class UserSerializerWithToken(UserSerializer):
    #refresh = serializers.SerializerMethodField(read_only = True)
    #access = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = "__all__"

    # def get_refresh(self,obj):
    #     refresh = RefreshToken.for_user(obj)
    #     return str(refresh)

    # def get_access(self, obj):
    #     access = RefreshToken.for_user(obj).access_token
    #     lifetime = access.lifetime
    #     access_and_lifetime = str(access) + "=" + str(lifetime)
    #     return access_and_lifetime
