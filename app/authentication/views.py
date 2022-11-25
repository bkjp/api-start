from rest_framework_simplejwt.views import TokenObtainPairView
from core.models import User
from .serializers import MyTokenObtainPairSerializer




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer