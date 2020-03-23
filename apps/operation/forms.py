import re

from django import forms
from apps.operation.models import UserFavorite, CourseComments

#继承ModelForm 定义验证字段
class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]

#评论表单验证
class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]
