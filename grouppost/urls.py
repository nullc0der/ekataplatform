from rest_framework.routers import DefaultRouter

from grouppost import views

router = DefaultRouter()
router.register('', views.PostViewSets, base_name='post')
router.register(r'comment', views.CommentViewset, base_name='comment')
urlpatterns = router.urls
