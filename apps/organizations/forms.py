import re

from django import forms
from apps.operation.models import UserAsk

#添加咨询表单
#此处使用ModelForm 继承了model的基础处理，只需要进行from的再处理
class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)
    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        正则验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[3589]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
