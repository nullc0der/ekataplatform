from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from grouppost import views

urlpatterns = [
    url(r'uploadimage/$', views.UploadImage.as_view())
]

router = DefaultRouter()
router.register(r'comment', views.CommentViewset, base_name='comment')
router.register(r'', views.PostViewSets, base_name='post')
urlpatterns += router.urls
