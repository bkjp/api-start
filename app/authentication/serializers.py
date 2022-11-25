from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

from users.serializers import UserSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        # Validated data coming from parent class: TokenObtainPairSerializer
        # this dic is in the form data = {"refresh":s...p, "access": w...p}
        data = super().validate(attrs)

        """
            data already contains access and refresh attributes. If we want to obtain a lifetime
            of access token for example normally we do access.lifetime. But since access and refresh
            token are already delivered by TokenObtainPairSerializer in form of the string, if we do
            data["access"].lifetime you will get an error
            (AttributeError: 'str' object has no attribute 'lifetime').
            Then we need to generate news refresh and access tokens and get their lifetimes
            and replace the previous ones by the new ones
        """
        # generate new refresh and access tokens and replace the old ones
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Adding customs fields access_token_lifetime and access_token_expiry

        # Obtaining the lifetime of access token
        time = str(refresh.access_token.lifetime)

        # Converting the obtained time in seconds
        time_in_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))

        data["access_token_lifetime"] = time_in_seconds
        data["access_token_expiry"] = str(datetime.now() + refresh.access_token.lifetime)

        # Obtaining dic user_data of dic data coming from UserSerializer
        serializer = UserSerializer(self.user)
        user_data = serializer.data

        # Adding fields and values of dic user_data to the dic data of TokenObtainPairSerializer
        for k, v in user_data.items():
            data[k]= v

        return data