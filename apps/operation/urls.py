from django.conf.urls import url

from apps.operation.views import AddFavView, CommentView, UserAskView

#操作接口
urlpatterns = [
    url(r'^fav/$', AddFavView.as_view(), name="fav"),
    url(r'^comment/$', CommentView.as_view(), name="comment"),
    url(r'^add_ask/$', UserAskView.as_view(), name="add_ask"),
]
