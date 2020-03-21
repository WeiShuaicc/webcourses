from django import forms
from captcha.fields import CaptchaField
import redis

from webcourse.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


class UpdateMobileForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birthday", "address"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]

#注册 验证码
class RegisterGetForm(forms.Form):
    captcha = CaptchaField()

#注册验证接口
class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)
  #分字段验证 1.手机号  2.验证码  这样做就可以获取哪个字段的问题了
    #注册手机号验证
    def clean_mobile(self):
        mobile = self.data.get("mobile")
        # 验证手机号码是否已经注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号码已注册")
        return mobile
    #获取redis中的code进行验证
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")

        return code
#表单验证 必填项，先设置密码长度限制
class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)

#动态验证登录手机号接口
class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()

#动态登录验证码接口
class DynamicLoginPostForm(forms.Form):
    #验证码相关设置更改目前设置 验证码4位
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    #验证码判断： 获取redis数据库中的数据验证code （code具有唯一key,手机号）
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data
    # 注：forms 的clean 是对所有的字段抛出异常，所有无法获取具体的异常，这时需要使用clean_code()方法
    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #     #连接redis
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
    #     redis_code = r.get(str(mobile))
    #     #debugrecord ：无法获取字段code错误
    #     if code != redis_code:
    #         raise forms.ValidationError("验证码不正确")
    #     return self.cleaned_data


