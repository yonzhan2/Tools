from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from vminfo.models import VCInfo, VMList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# @login_required
def vminfo(request):
    vc_list = VCInfo.objects.all()
    vm_list = VMList.objects.all()
    # username = request.COOKIES.get('user','')
    username = request.session.get('user', '')
    search_name = request.GET.get("vmname", "")
    search_ip = request.GET.get("vmip", "")
    search_vc = request.GET.get("vcname", "")

    if search_name and not search_ip and not search_vc:
        vms = VMList.objects.filter(vmname__contains=search_name)
    elif search_ip and not search_name and not search_vc:
        vms = VMList.objects.filter(vmip__contains=search_ip)
    elif search_vc and not search_name and not search_ip:
        vms = VMList.objects.filter(vcname=search_vc)
    elif search_name and search_ip and not search_vc:
        vms = VMList.objects.filter(vmname__contains=search_name, vmip__contains=search_ip)
    elif search_name and search_vc and not search_ip:
        vms = VMList.objects.filter(vmname__contains=search_name, vcname=search_vc)
    elif search_ip and search_vc and not search_name:
        vms = VMList.objects.filter(vmip__contains=search_ip, vcname=search_vc)
    elif search_name and search_ip and search_vc:
        vms = VMList.objects.filter(vmname__contains=search_name, vmip__contains=search_ip, vcname=search_vc)
    else:
        vms = VMList.objects.all()

    count = vms.count()
    paginator = Paginator(vms, 20)
    page = request.GET.get('page')
    try:
        vms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        vms = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g. 9999),deliver last page of results.
        vms = paginator.page(paginator.num_pages)
    return render(request, "vminfo.html", {'user': username,
                                           'vmlist': vms,
                                           'vclist': vc_list,
                                           'search_name': search_name,
                                           'search_ip': search_ip,
                                           'search_vc': search_vc,
                                           'count': count})
