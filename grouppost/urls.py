from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from grouppost import views

urlpatterns = [
    url(r'uploadimage/$', views.UploadImage.as_view())
]

router = DefaultRouter()
router.register('', views.PostViewSets, base_name='post')
router.register(r'comment', views.CommentViewset, base_name='comment')
urlpatterns += router.urls
