from django.urls import path,include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    
    path('list/',views.movie_list,name="movie-list"),
    path('list/<int:pk>',views.movie_detail,name="watchlist-detail"),
    path('stream/',views.Stream_list.as_view(),name="stream-platform"),
    path('stream/<int:pk>',views.Stream_detail.as_view(),name="streamplaform-detail"),
   
    path('review/<int:pk>',views.ReviewDetailView.as_view(),name="review-detail"),
    path('list/<int:pk>/review/',views.ReviewListView.as_view(),name="review-list"),
    path('list/<int:pk>/review-create/',views.ReviewCreate.as_view(),name="review-create"),
    path('list/review/<int:pk>',views.ReviewDetailView.as_view(),name="review-detail"),
    path('', views.api_root),
]
urlpatterns = format_suffix_patterns(urlpatterns)