from django.urls import path
from .views import PostList, PostDetail, PostCreate, Post_Filter, PostUpdate, PostDelete, add_subscribe, del_subscribe, \
   CategoryList, IndexView

urlpatterns = [
   path('', PostList.as_view(),name='post_list'),
   path('<int:pk>', PostDetail.as_view(),name='post_detail'),
   path('edit/', PostCreate.as_view(), name='edit'),
   path('search/',Post_Filter.as_view(),name='search'),
   path('<int:pk>/edit',PostUpdate.as_view(),name='edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='delete'),
   path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
   path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
   path('sub/', CategoryList.as_view(), name='categories'),
   path('sub/subscribe/', add_subscribe, name='subscribe'),
   path('', IndexView.as_view()),
]