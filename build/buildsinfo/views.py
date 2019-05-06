from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Envs, BuildInfo
import time
from django.shortcuts import redirect
import os


# Create your views here.


def timeConvert(s):
    try:
        timestruct = time.strptime(s, "%a %b %d %H:%M:%S %Y")
    except:
        timestruct = time.strptime(s, "%a %d %b %Y %H:%M:%S %p GMT")
    timeformat = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    timestamp = time.mktime(timestruct)
    return timeformat, timestamp


def version(request, search_env=None):
    # names = Employee.objects()
    buildsinfo = BuildInfo.objects.all()
    # envs = Envs.objects.all()
    envs = buildsinfo.distinct("env")
    search_name = request.GET.get("hostname", "")
    search_ip = request.GET.get("ipaddr", "")
    search_env = search_env if search_env else request.GET.get("env", "QA-hf3wd")

    if search_name and not search_ip and not search_env:
        buildsinfo = buildsinfo.filter(hostname__contains=search_name)
    elif search_ip and not search_name and not search_env:
        buildsinfo = buildsinfo.filter(ipaddr__contains=search_ip)
    elif search_env and not search_name and not search_ip:
        buildsinfo = buildsinfo.filter(env=search_env)
    elif search_name and search_ip and not search_env:
        buildsinfo = buildsinfo.filter(hostname__contains=search_name, ipaddr__contains=search_ip)
    elif search_name and search_env and not search_ip:
        buildsinfo = buildsinfo.filter(hostname__contains=search_name, env=search_env)
    elif search_ip and search_env and not search_name:
        buildsinfo = buildsinfo.filter(ipaddr__contains=search_ip, env=search_env)
    elif search_name and search_ip and search_env:
        buildsinfo = buildsinfo.filter(hostname__contains=search_name, ipaddr__contains=search_ip, env=search_env)
    else:
        buildsinfo = buildsinfo

    filter_env = buildsinfo.filter(env=search_env)
    lastbuild_list = [build[0] for last in filter_env for build in last.lastbuild]

    count = buildsinfo.count()
    paginator = Paginator(buildsinfo, 50)
    page = request.GET.get('page')
    try:
        buildsinfo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        buildsinfo = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g. 9999),deliver last page of results.
        buildsinfo = paginator.page(paginator.num_pages)

    # return HttpResponse(u"Hello World!")
    return render(request, "versionlist.html", {"buildsinfo": buildsinfo,
                                                "envs": envs,
                                                'search_env': search_env,
                                                'search_name': search_name,
                                                'search_ip': search_ip,
                                                'lastbuild_list': lastbuild_list,
                                                'count': count
                                                })


def history(request):
    path = "/Users/yonzhan2/Documents/PythonScripts/Tools/build/buildsinfo/history/"  # insert the path to your directory
    img_list = os.listdir(path)
    return render(request, 'history.html', {'images': img_list})


def history_detail(request, subfile):
    return StreamingHttpResponse(open(subfile))


def szwd(request):
    return redirect("http://localhost:8000/version?env=QA-szwd")


def hfwd(request):
    return redirect("http://localhost:8000/version?env=QA-hfwd")


def hf2wd(request):
    return redirect("http://localhost:8000/version?env=Firedrill-hf2wd")


def hf3wd(request):
    return redirect("http://localhost:8000/version?env=QA-hf3wd")


def ats(request):
    return redirect("http://localhost:8000/version?env=ATS")


def sawd(request):
    return redirect("http://localhost:8000/version?env=QADMZ")


def sqwd(request):
    return redirect("http://localhost:8000/version?env=DEVDMZ")
