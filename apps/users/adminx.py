import xadmin
from users.models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):
    #增加xadmin的主题样式
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    #修改xadmin的左上角和页脚的字
    site_title = 'Demo_Study后台管理系统'
    site_footer = 'Demo_Study在线教育平台'
    #将注册的model给收起来
    menu_style = 'accordion'


#以下为注册model到xadmin中以便于后台管理

class EmailVerifyRecordAdmin(object):
    #显示字段
    list_display = ['code','email','send_type','send_time']
    #搜索字段
    search_fields = ['code','email','send_type']
    #过滤字段
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

#注册
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)