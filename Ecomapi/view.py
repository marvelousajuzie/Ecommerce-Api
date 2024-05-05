from serializer import PasswordResetSerializer
from rest_framework import viewsets
from models import CustomUsers
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken


class PasswordResetRequestView(viewsets.ModelViewSet):

    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.validated_data['email']
            user_qs = CustomUsers.objects.filter(email = email)
            if user_qs.exists():
                user = user_qs.first()
                token = AccessToken.for_user = user
                token['exp'] = datetime.utcnow() + timedelta(hours= 1)
                