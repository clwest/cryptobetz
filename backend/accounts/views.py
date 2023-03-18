
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = CustomUserSerializer
  
class LoginView(generics.GenericAPIView):
  permissions_classes = [permissions.AllowAny]
  serializer_class = CustomUserSerializer
  
  def post(self, request):
    email = request.data['email']
    password = request.data['password']
    user = CustomUser.objects.filter(email=email).first()
    
    if user and user.check_password(password):
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        
      })
    else:
      return Response({'detail': 'Invalid email or password'}, status=400)