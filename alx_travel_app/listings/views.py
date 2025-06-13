from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

from listings import serializers

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Optionally filter listings by location or price range"""
        queryset = super().get_queryset()
        location = self.request.query_params.get('location')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users see only their bookings, staff sees all"""
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            listing=listing,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()
        
        if overlapping:
            raise serializers.ValidationError("This listing is already booked for the selected dates.")
        
        # Calculate total price
        days = (end_date - start_date).days
        total_price = days * listing.price_per_night
        
        serializer.save(
            user=self.request.user,
            total_price=total_price
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Custom action to cancel a booking"""
        booking = self.get_object()
        
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You don't have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status == 'cancelled':
            return Response(
                {"detail": "This booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        return Response(
            {"status": "Booking cancelled successfully."},
            status=status.HTTP_200_OK
        )
