from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import EventViewSet
from .views import UserViewSet

# Create a router and register our viewsets with it 
router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls


'''ALL THE CODE BELOW WAS BEFORE ADJUSTMENTS TO THE API'''
# from django.urls import path 
# from events.views import *
# from rest_framework_simplejwt.views import  TokenObtainPairView

# from rest_framework.routers import DefaultRouter
# from .views import *

# router = DefaultRouter()
# router.register(r'events', EventViewSet)
# router.register(r'users', UserViewSet)



# urlpatterns = [
#     # These are endpoints for events and participants 
#     path('events/', EventListView.as_view(), name='event-list'),
#     path('events/create/', EventCreateView.as_view(), name='event-create'),
#     path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
#     path('events/<int:event_id>/register/', EventRegisterView.as_view(), name='event-register'),
#     path('events/<int:event_id>/participants/', EventParticipantsView.as_view(), name='event-participants'),

#     # JWT token obtain view 
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

#     # User registration endpoint 
#     path('register/', UserRegisterView.as_view(), name='user-register'),

#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('token/', CustomAuthToken.as_view(), name='token'),
# ]

# urlpatterns += router.urls