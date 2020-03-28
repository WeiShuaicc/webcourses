from django.db.models import Sum

import xadmin

from apps.courses.models import Course, Lesson, Video, BannerCourse, CourseResource, CourseTag
from apps.courses.views import TestView, Xadmin_addVideoView, xadmin_returnView
from apps.trades.models import OrderInfo
from xadmin.layout import Fieldset, Main, Side, Row
from xadmin.views import BaseAdminObject


class GlobalSettings(BaseAdminObject):
    site_title = "精品课程后台管理系统"
    site_footer = "精品课程在线网"
    # menu_style = "accordion"  #菜单标签

    #菜单
    def get_site_menu(self):  # 名称不能改
        return [
            {
                'menus': (
                    {
                        'title': '移动直播生成器',  # 这里是你菜单的名称
                        'url': '/xadmin/test_view',  # 这里填写你将要跳转url
                        # 'icon': 'fa fa-cny'     #这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                    {
                        'title': '课程视频添加',  # 这里是你菜单的名称
                        'url': '/xadmin/addvideo_view',  # 这里填写你将要跳转url
                    }
                )
            }
        ]


# 注册要跳转的视图函数
xadmin.site.register_view(r'test_view/$', TestView, name='test')
xadmin.site.register_view(r'addvideo_view/$', Xadmin_addVideoView, name='addvideo')
#debugrecord: 所有的对xadmin的处理必须在xadmin中注册！！！
xadmin.site.register_view(r'upvideofile/',xadmin_returnView,name="upvideofile" )

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

#设置项  tab显示 目前xadmin的一个小bug 上下不可以同时设置tab
class LessonInline(object):
    model = Lesson
    #style = "tab"
    extra = 0
    exclude = ["add_time"]


class CourseResourceInline(object):
    model = CourseResource
    style = "tab"
    extra = 1


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


from import_export import resources

class MyResource(resources.ModelResource):
    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()


#固定的ip  设置项：xadmin自定义def get_form_layout(self):布局
#1. 本地的ip是一个动态分配的ip地址
#2. 数据包转发问题 scp
class NewCourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_display = ['name', 'desc', 'show_image', 'go_to', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']#teacher_name 实现在教师后再过滤名字
    list_editable = ["degree", "desc"]
    readonly_fields = ["students", "add_time"] #只读
    # exclude = ["click_nums", "fav_nums"]
    ordering = ["click_nums"]
    model_icon = 'fa fa-address-book'
    inlines = [LessonInline, CourseResourceInline]
    #修改 使用富文本编辑插件
    style_fields = {
        "detail":"ueditor"
    }
    #后台数据绑定 一个管理用户（非超级用户）绑定一个教师身份，并只对该教师课程显示
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs
    #category 在这只显示选项
    def get_form_layout(self):
        #判断是否为编辑页
        if self.org_obj:
            self.form_layout = (
                    Main(
                        Fieldset("讲师信息",
                                 'teacher','course_org',
                                 css_class='unsort no_title'
                                 ),
                        Fieldset("基本信息",
                                 'name', 'desc',
                                 Row('learn_times', 'degree'),
                                 Row('category', 'tag'),
                                 'youneed_know', 'teacher_tell', 'detail',
                                 ),
                    ),
                    Side(
                        Fieldset("访问信息",
                                 'fav_nums', 'click_nums', 'students','add_time'
                                 ),
                    ),
                    Side(
                        Fieldset("选择信息",
                                 'is_banner', 'is_classics'
                                 ),
                    )
            )
        return super(NewCourseAdmin, self).get_form_layout()

    data_charts = {
        "user_count": {'title': u" 课程点击量",
                       "x-field": "add_time",
                       "y-field": "click_nums",
                       },
        # "num_count": {'title': u" 课程点击量 柱形表",
        #               "x-field": "id",
        #               "y-field": ("click_nums"),
        #               'option': {
        #                   "series": {"bars": {"align": "center", "barWidth": 0.8, "show": True}},
        #                   #"xaxis": {"order_mount": "count", "order_sn": "categories"}
        #               },
        #               },

    }



class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


# file 课程资源
class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']

#后台admin tag
class CourseTagAdmin(object):
    list_display = ['course', 'tag','add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag','add_time']


#课程订单
class OrderAdmin(object):
    list_display = ['course','order_sn', 'trade_no', 'user',  'pay_status', 'order_mount', 'add_time',
                    'singer_mobile']
    search_fields = ['trade_no', 'user__username', 'pay_status', 'course__name', 'add_time']
    list_filter = ['trade_no', 'user', 'pay_status', 'course']
    readonly_fields = ['order_sn', 'trade_no', 'user','course','order_mount']  # 只读
    # data_charts = {
    #     "user_count": {'title': u"支付情况",
    #                    "x-field": "add_day",
    #                    "y-field": "order_mount",
    #                    },
    # }
    def total_money(self):
        return OrderInfo.objects.filter(
            pay_status='TRADE_CLOSED',
        ).aggregate(
            order_mount=Sum('order_mount')
        )['order_mount'] or 0

    total_money.short_description = '总额'
    data_charts = {
        "user_count": {'title': u"sc 金额变化表折现表",
                       "x-field": "add_day",
                       "y-field": total_money,
                       },
        "num_count": {'title': u"sc 金额变化表 1 柱形表",
                      "x-field": "add_day",
                      "y-field": ("order_mount"),
                      'option': {
                          "series": {"bars": {"align": "center", "barWidth": 0.8, "show": True}},
                          #"xaxis": {"order_mount": "count", "order_sn": "categories"}
                      },
                      },

    }


#数据可视化





#对一张表进行多个管理
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)

xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)#注册 Global
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)  #注册 Base 皮肤
xadmin.site.register(OrderInfo, OrderAdmin)

