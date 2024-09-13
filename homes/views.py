from math import radians, cos, sin, asin, sqrt

from django.views.generic import TemplateView
from django_filters import rest_framework as filters
from geopy.geocoders import Nominatim
from rest_framework import viewsets

from .models import Home
from .serializers import HomeSerializer


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def find_address(address):
    geolocator = Nominatim(user_agent='Jimmy')
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None


class FrontendView(TemplateView):
    template_name = "homes/index.html"


class HomeFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_rooms = filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    max_rooms = filters.NumberFilter(field_name="rooms", lookup_expr='lte')
    balcony = filters.BooleanFilter(field_name="balcony")
    garden = filters.BooleanFilter(field_name="garden")
    furnished = filters.BooleanFilter(field_name="furnished")

    class Meta:
        model = Home
        fields = ['min_price', 'max_price', 'min_rooms', 'max_rooms', 'balcony', 'garden', 'furnished']


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HomeFilter

    def get_queryset(self):
        queryset = Home.objects.all()
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        distance = self.request.query_params.get('distance')

        if self.request.query_params.get('address'):
            lat, lon = find_address(self.request.query_params.get('address'))

        if lat and lon and distance:
            lat, lon, distance = float(lat), float(lon), float(distance)
            queryset = self.filter_by_distance(queryset, lat, lon, distance)

        return queryset

    def filter_by_distance(self, queryset, lat, lon, max_distance):
        filtered_ids = []
        for home in queryset:
            dist = haversine(lon, lat, home.lon, home.lat)
            if dist <= max_distance:
                filtered_ids.append(home.id)
        return queryset.filter(id__in=filtered_ids)
