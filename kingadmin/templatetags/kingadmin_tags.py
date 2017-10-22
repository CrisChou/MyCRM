from django.template import Library
from django.utils.safestring import mark_safe
import datetime

register = Library()
# ###注意注意register千万千万不要写错


@register.simple_tag
def build_table_row(item, admin_class):
    '''用于生成表格行数据'''
    ele = ''
    for c in admin_class.list_display:
        if admin_class.model._meta.get_field(c).choices:
            column_data = getattr(item, 'get_%s_display' % c)()
        else:
            column_data = getattr(item, c)

        td_ele = '<td>%s</td>' % column_data
        ele += td_ele
    ele += '''<td><a href="%s/change_data.html" class="btn btn-primary">编辑
    </a></td>''' % (item.id, )
    return mark_safe(ele)


@register.simple_tag
def build_filter_ele(column, admin_class):
    column_choices = admin_class.model._meta.get_field(column)

    try:
        select_ele = "%s:<select name='%s' class='form-control'>" % (column,
                                                                     column)
        for choices in column_choices.get_choices():
            selected = ''
            if column in admin_class.filter_conditions:
                if str(choices[0]) == admin_class.filter_conditions.get(
                        column):
                    selected = 'selected'
            option = '<option value="%s" %s>%s</option>' % (choices[0],
                                                            selected,
                                                            choices[1], )
            select_ele += option

    except AttributeError:
        if column_choices.get_internal_type() in ('DateField',
                                                  'DateTimeField'):
            select_ele = "%s:<select name='%s__gte' class='form-control'>" % (
                column, column)
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '----------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                ['', 'ALL'],
            ]
            for i in time_list:
                selected = ''
                time_str = '' if not i[0] else "%s-%s-%s" % (i[0].year,
                                                             i[0].month,
                                                             i[0].day)
                if '%s__gte' % column in admin_class.filter_conditions:
                    if time_str == admin_class.filter_conditions.get(
                            '%s__gte' % column):
                        selected = 'selected'
                option = '<option value="%s" %s>%s</option>' % (time_str,
                                                                selected,
                                                                i[1], )
                select_ele += option
            select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def build_sorted_arrow(item, current_sorted_column):
    if item in current_sorted_column:
        arrow = ''
        if current_sorted_column[item].startswith('-'):
            arrow = '↑'

        else:
            arrow = '↓'

        return mark_safe(arrow)

    else:
        return ''


@register.simple_tag
def get_sorted_column(item, current_sorted_column, forloop):
    if item in current_sorted_column:
        sorted_index = current_sorted_column[item]
        if sorted_index.startswith('-'):
            sorted_index = sorted_index.strip('-')
        else:
            sorted_index = '-' + sorted_index

        return sorted_index

    else:
        return forloop


@register.simple_tag
def render_filter_args(admin_class):
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += '&%s=%s' % (k, v)
        return mark_safe(ele)

    else:
        return ''


@register.simple_tag
def get_field_value(model_obj, field, admin_class):
    try:
        choices = admin_class.model._meta.get_field(field)
        field_value = choices.get_choices()
        for i, j in field_value:
            if i == getattr(model_obj.instance, field):
                return j
    except AttributeError:
        return getattr(model_obj.instance, field)


@register.simple_tag
def get_m2m_value(model_obj, field_name, admin_class):
    field_obj = admin_class.model._meta.get_field(field_name)
    qs = getattr(model_obj.instance, field_name).all()
    qs = set(qs)
    field_obj = field_obj.related_model.objects.all()
    field_obj = set(field_obj)
    return field_obj - qs


@register.simple_tag
def get_qs_m2m_value(model_obj, field_name, admin_class):

    qs = getattr(model_obj.instance, field_name).all()
    return qs


@register.simple_tag
def get_add_m2m_value(obj_name, admin_class):
    field_obj = admin_class.model._meta.get_field(obj_name)
    field_obj = field_obj.related_model.objects.all()
    return field_obj


@register.simple_tag
def build_delete_msg(obj):
    """
    提示要被删除对象所有的关联对象
    """
    ele = "<ul>"
    for fk_obj in obj._meta.related_objects:
        table_name = fk_obj.name
        serach_str = "%s_set" % table_name
        related_objs = getattr(obj, serach_str).all()
        ele += "<li>%s<ul>" % table_name

        if fk_obj.get_internal_type() == "ManyToManyField":
            for i in related_objs:
                ele += '''<li><a href='/kingadmin/%s/%s/%s/change_data.html'>%s</a></li>''' % (
                    i._meta.app_label, i._meta.model_name, i.id, i)

        else:
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change_data.html'>%s</a></li>" % (
                    i._meta.app_label, i._meta.model_name, i.id, i)

                ele += build_delete_msg(i)
        ele += "</ul></li>"

    ele += "</ul>"
    return ele



@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name