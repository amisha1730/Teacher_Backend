from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from .serializers import TeacherSerializer
from .models import Teacher
import jwt, datetime
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


# def get_tokens_for_teacher(teacher):
#     refresh = RefreshToken.for_teacher(teacher)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, teacher):
#         token = super().get_token(teacher)

#         # Add custom claims
#         token['email'] = teacher.email
#         token['role'] = teacher.role
#         # ...

#         return {email:email,token:token}


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# class RegisterView(APIView):
class RegisterView(APIView):
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher=serializer.save()
        tokenr = TokenObtainPairSerializer().get_token(teacher)  
        tokena = AccessToken().for_user(teacher)
        tokena['email'] = teacher.email
        tokena['role'] = teacher.role
        response = Response()
        response.data = {
            'teacher':serializer.data,
            'accessToken':str(tokena),
            'refreshToken': str(tokenr)
        }
        return response




class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        teacher = Teacher.objects.filter(email=email).first()
        if teacher is None:
            raise AuthenticationFailed('teacher not found!')

        if not teacher.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        tokenr = TokenObtainPairSerializer().get_token(teacher)  
        tokena = AccessToken().for_user(teacher)
        tokena['email'] = teacher.email
        tokena['role'] = teacher.role
        response = Response()
        print("this is the response",response.data)
        response.set_cookie(key='jwt', value=tokena, httponly=True)
        response.data = {
            'id':teacher.id,
            'email':teacher.email,
            'accessToken':str(tokena),
            'refreshToken': str(tokenr)
        }
        return response


class getTeacher(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher,many=True)
        return Response(serializer.data)

class getTeacherById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        teacher = Teacher.objects.get(id=id)
        serializer=TeacherSerializer(teacher,many=False)
        return Response(serializer.data)

class updateTeacher(APIView):
    # permission_classes = [IsAuthenticated]

    def patch(self, request,id):
        teacher = Teacher.objects.get(id=id)
        serializer=TeacherSerializer(instance=teacher,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class deleteTeacher(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request,id):
        teacher = Teacher.objects.get(id=id)
        teacher.delete()
        return Response("Item Successfully Deleted")

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ValidateToken(APIView):
    def get(self, request):
        try:
            print("asdasdsadsadasdasd")
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            data=jwt.decode(token, "secret", algorithms=["HS256"])
            return Response(data)
        except Exception as e:
            return Response(e)
        
