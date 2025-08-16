""" Manual approach """

""" from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializers
from drf_api.permissions import IsOwnerOrReadOnly


# Create your views here.
class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializers(
            profiles, many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    

class ProfileDetail(APIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsOwnerOrReadOnly]



    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializers(
            profile, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializers(
            profile, data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


""" Generic approach """

from django.db.models import Count
from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializers


# Create your views here.
class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializers
    ordering_fields = [
        'post_count',
        'followers_count', 
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
        'filterset_fields',
    ]
    queryset = Profile.objects.annotate(
        post_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
        filterset_fields=Count('owner__following__owner__profile', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter
    ]

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.annotate(
        post_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    permission_classes = [IsOwnerOrReadOnly]