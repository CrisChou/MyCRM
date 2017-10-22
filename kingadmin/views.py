from django.shortcuts import render, redirect
from kingadmin import app_setup
from kingadmin.sites import site
from django.contrib.auth.decorators import login_required
from kingadmin.static.mod.peag_fuc import Pagefunc
from django.db.models import Q
from kingadmin.create_model_form import create_model_form
import json
from kingadmin.permissions import check_permission
app_setup.kingadmin_setup()

# Create your views here.


@login_required
def admin(request):
    return render(request, 'kingadmin/admin.html', {'site': site})


@check_permission
def get_filter_result(request, querysets):
    '''
    获得所有的过滤条件
    '''
    filter_conditions = {}
    for key, val in request.GET.items():
        if key in ('page', '_o', '_q'):
            continue
        if val:
            filter_conditions[key] = val

    return querysets.filter(**filter_conditions), filter_conditions


def render_filter_args(admin_class):
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += '&%s=%s' % (k, v)
        return ele

    else:
        return ''


@check_permission
def get_orderby_result(request, qs, admin_class):
    sorted_ele = request.GET.get('_o')
    current_sorted_column = {}
    if sorted_ele:
        sorted_key = admin_class.list_display[abs(int(sorted_ele))]
        current_sorted_column[sorted_key] = sorted_ele
        if sorted_ele.startswith('-'):
            sorted_key = '-' + sorted_key
        return qs.order_by(sorted_key), current_sorted_column

    return qs, current_sorted_column


@check_permission
def searched(request, qs, admin_class):
    search_arg = request.GET.get('_q')
    if search_arg:
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(('%s__contains' % search_field, search_arg))
        return qs.filter(q)
    return qs


@check_permission
@login_required
def show_model_table(request, app_name, model_name):
    admin_class = site.init_admin_dict[app_name][model_name]
    if request.method == "POST":
        action = request.POST.get('action')
        select_ids = request.POST.get('select_ids')
        select_ids = json.loads(select_ids)
        fuc = getattr(admin_class, action)
        qs_obj_list = []
        for i in select_ids:
            qs_obj = admin_class.model.objects.get(id=int(i))
            qs_obj_list.append(qs_obj)
        response = fuc(request, qs_obj_list)
        if response:
            return response

    qs = admin_class.model.objects.all()
    qs, filter_conditions = get_filter_result(request, qs)
    admin_class.filter_conditions = filter_conditions
    qs, current_sorted_column = get_orderby_result(request, qs, admin_class)
    qs = searched(request, qs, admin_class)
    filter_ele = render_filter_args(admin_class)
    sorted_ele = request.GET.get('_o')
    sorted_ele = '&_o=%s' % sorted_ele if sorted_ele else None
    current_page = request.GET.get('page')
    admin_class.search_arg = request.GET.get('_q', '')
    admin_class.filter_conditions['page'] = current_page
    all_count = qs.count()
    page_fuc = Pagefunc(
        current_page=current_page,
        all_count=all_count,
        sorted_ele=sorted_ele,
        filter_ele=filter_ele)
    page_btn = page_fuc.page()
    return render(request, 'kingadmin/show_model_table.html', {
        'admin_class': admin_class,
        'qs': qs[page_fuc.start:page_fuc.stop],
        'page_btn': page_btn,
        'current_sorted_column': current_sorted_column,
    })


@check_permission
@login_required
def chang_data(request, app_name, model_name, row_id):
    admin_class = site.init_admin_dict[app_name][model_name]
    model_from = create_model_form(admin_class)
    qs_obj = admin_class.model.objects.get(id=row_id)
    if request.method == 'GET':
        model_obj = model_from(instance=qs_obj)
    else:
        model_obj = model_from(instance=qs_obj, data=request.POST)
        if model_obj.is_valid():
            model_obj.save()
            return redirect('/kingadmin/%s/%s/' % (app_name, model_name))
    return render(request, 'kingadmin/change_data.html', {
        'model_obj': model_obj,
        'admin_class': admin_class,
        'app_name': app_name,
        'model_name': model_name,
    })


@check_permission
def add_data(request, app_name, model_name):
    admin_class = site.init_admin_dict[app_name][model_name]
    model_from = create_model_form(admin_class, form_add=True)
    if request.method == 'GET':
        model_obj = model_from()
    else:
        model_obj = model_from(data=request.POST)
        if model_obj.is_valid():
            model_obj.save()
            return redirect('/kingadmin/%s/%s/' % (app_name, model_name))
    return render(request, 'kingadmin/add_data.html', {
        'model_obj': model_obj,
        'admin_class': admin_class,
    })


@check_permission
@login_required
def delete_data(request, app_name, model_name, obj_id):
    admin_class = site.init_admin_dict[app_name][model_name]
    obj_id_list = list(obj_id)
    objs = admin_class.model.objects.filter(id__in=obj_id_list)
    if request.method == 'POST':
        objs.delete()
        return redirect('/kingadmin/{0}/{1}/'.format(app_name, model_name))
    return render(request, 'kingadmin/delete_data.html', {
        'objs': objs,
    })
