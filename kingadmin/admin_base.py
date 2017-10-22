from django.shortcuts import redirect


class BaseKingAdmin(object):
    # def __init__(self, *args, **kwargs):
    #     self.actions.extend(self.default_actions)

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []

    default_actions = ['delete_selected_objs']
    actions = []

    def delete_selected_objs(self, request, querysets):
        qs_id_list = []
        for i in querysets:
            qs_id_list.append(i.id)
        id_str = ''
        for i in qs_id_list:
            id_str += str(i)

        return redirect('/kingadmin/%s/%s/%s/delete_data.html' %
                        (querysets[0]._meta.app_label,
                         querysets[0]._meta.model_name, id_str))
