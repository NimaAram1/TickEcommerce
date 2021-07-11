from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from .serializers import RegisterationSerializer

# getting user model
User = get_user_model()

class RegisterationApiView(APIView):
    """
    Get username, email, phone number, and password from the user
    and save it in the database
    """
    def post(self, request):
        if request.user.is_anonymous:
            data = RegisterationSerializer(data=request.data)
            if data.is_valid():
                User.objects.create(email=data.validated_data["email"], username=data.validated_data["username"],
                password=data.validated_data["password"], phone_number=data.validated_data["phone_number"])
                return Response({
                "message": f'اکانت {data.validated_data["email"]} با موفقیت ساخته شد'
                })
            else:
                return Response(data.errors)
        else:
            return Response({
                "message": "شما از قبل احراز هویت کرده اید"
            })            

class LoginApiView(GenericAPIView):
    pass