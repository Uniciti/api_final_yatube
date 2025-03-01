from rest_framework.routers import SimpleRouter

from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

appname = 'api'

router = SimpleRouter()
router.register('v1/posts', PostViewSet, basename='posts')
router.register('v1/groups', GroupViewSet, basename='groups')
router.register('v1/follow', FollowViewSet, basename='follow')
router.register(r'^v1/posts/(?P<post_pk>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/jwt/create/', jwt_views.TokenObtainPairView.as_view()),
    path('v1/jwt/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('v1/jwt/verify/', jwt_views.TokenVerifyView.as_view()),
    path('', include(router.urls)),
]
