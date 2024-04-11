from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import StreamPlaform, WatchList,Review
from .serializers import WatchListSerializer,StreamPlaformSerailizer,ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'watchlist': reverse('movie-list', request=request, format=format),
        'streamplatform': reverse('stream-platform', request=request, format=format)
    })
@api_view(['GET'])
def movie_list(request):
    movie_list=WatchList.objects.all()
    serialized=WatchListSerializer(movie_list, many= True)
    return Response(serialized.data)
@api_view(['GET'])
def movie_detail(request,pk):
    movie=WatchList.objects.get(pk=pk)
    serialized=WatchListSerializer(movie)
    return Response(serialized.data)
#@api_view(['GET', 'POST'])
#def stream_list(request,format=None):
#    if request.method=='GET':
#        stream_list=StreamPlaform.objects.all()
#        serialized=StreamPlaformSerailizer(stream_list, many= True)
#        return Response(serialized.data)
#    elif request.method=='POST':
#        _data=request.data
#        serialized=StreamPlaformSerailizer(data=_data)
#        if serialized.is_valid():
#            serialized.save()
#            return Response(serialized.data,status=status.HTTP_201_CREATED)
#        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
#    
#@api_view(['GET', 'PUT', 'DELETE'])    
#def stream_detail(request,pk,format=None):
#    try:
#        stream_platform=StreamPlaform.objects.get(pk=pk)
#    except StreamPlaform.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#    
#    if request.method == 'GET':
#        serializer = StreamPlaformSerailizer(stream_platform)
#        return Response(serializer.data)
#
#    elif request.method == 'PUT':
#        _data=request.data
#        serializer = StreamPlaformSerailizer(stream_platform, data=_data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    elif request.method == 'DELETE':
#        StreamPlaform.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
#    

class Stream_list(generics.ListCreateAPIView):
    queryset = StreamPlaform.objects.all()
    serializer_class = StreamPlaformSerailizer

class Stream_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamPlaform.objects.all()
    serializer_class = StreamPlaformSerailizer
class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    def perform_create(self, serializer):
        pk=self.kwargs['pk']
        movie=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(review_user=review_user,watchlist=movie)
        if review_queryset.exists():
            raise ValidationError("cant review")
        if movie.number_rating==0:
            movie.av_rating=serializer.validated_data['rating']
        else:
            movie.av_rating=(movie.av_rating+serializer.validated_data['rating'])/2

        movie.number_rating+=1
        movie.save()
        serializer.save(review_user=review_user, watchlist=movie)
class ReviewListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
       permission_classes=[IsAuthenticatedOrReadOnly]
       queryset = Review.objects.all()
       serializer_class = ReviewSerializer

