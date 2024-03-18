from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsModerator
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_session, create_stripe_price


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('date_of_payment',)
    permission_classes = [IsAuthenticated]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsModerator]


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Choose a course')

        payment = serializer.save()

        payment.payment_id, payment.payment_link = create_stripe_session(create_stripe_price(payment))

        payment.save()
