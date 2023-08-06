from blog.views import blog_article
from django.shortcuts import redirect, render
from blog.models import BlogArticles
from django.utils import timezone
from .froms import Write
from login.models import Userpass
# Create your views here.
def write(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/login/')
    if request.method == "POST":
        write_form = Write(request.POST)
        message = "请检查填写的内容！"
        if write_form.is_valid():  # 获取数据
            username = request.session.get('user_name')
            title3 = write_form.cleaned_data['title2']
            body2 = write_form.cleaned_data['body']
            time2 = timezone.now()
            username = Userpass.objects.get(id=1)
            newuser = BlogArticles.objects.create(title=title3,author=username,body=body2,publish=time2)
            newuser.save()
            return redirect('/blog/')  # 自动跳转到登录页面
    write_form = Write()
    return render(request, 'write.html', locals())