from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    '''
    课程机构显示
    '''
    def get(self,request):
        #查询数据
        citys = CityDict.objects.all()
        objs = CourseOrg.objects.all()
        hot_orgs = objs.order_by('click_nums')[:3]
        #获得参数
        city_id = request.GET.get('city','')
        category = request.GET.get('ct','')
        #根据城市筛选数据
        if city_id:
            objs = objs.filter(city_id=int(city_id))
        #根据类别筛选数据
        if category:
            objs = objs.filter(category=category)
        sort = request.GET.get('sort','')
        #排序
        if sort:
            if sort == 'students':
                objs = objs.order_by('-students')
            elif sort == 'courses':
                objs = objs.order_by('-course_nums')
        #获得数量
        obj_num = objs.count()
        #分页
        try:
            #page参数自动加上
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(objs,3, request=request)
        objs = p.page(page)
        return render(request,'org_list.html',{'objs':objs,
                                               'citys':citys,
                                               'obj_num':obj_num,
                                               'city_id':city_id,
                                               'category':category,
                                               'hot_orgs':hot_orgs,
                                               'sort':sort
                                               })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # commit=True将数据提交到数据库
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    '''
    授课机构主页
    '''
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-homepage.html',
                      {'all_courses':all_courses,
                       'all_teachers':all_teachers,
                       'course_org':course_org,
                       'current_page':current_page,
                       'has_fav':has_fav}
                      )


class CourseView(View):
    '''
    机构课程首页
    '''
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-course.html',
                      {'all_courses':all_courses,
                       'course_org':course_org,
                       'current_page':current_page,
                       'has_fav':has_fav}
                      )


class DescView(View):
    '''
    机构介绍页
    '''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',
                      {'course_org':course_org,
                       'current_page':current_page,
                       'has_fav':has_fav}
                      )


class OrgTeacherView(View):
    '''
    机构讲师
    '''
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',
                      {'all_teachers':all_teachers,
                       'course_org':course_org,
                       'current_page':current_page,
                       'has_fav':has_fav}
                      )


class AddFavView(View):
    '''
    添加收藏
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
