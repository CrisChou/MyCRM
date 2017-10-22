perm_dict = {
    'crm_table_list': [
        'show_model_table',
        'GET',
        [],
        {},
    ],  # 可以查看每张表里所有的数据
    'crm_table_list_view': [
        'table_obj_change',
        'GET',
        [],
        {},
    ],  # 可以访问表里每条数据的修改页
    'crm_table_list_change': [
        'table_obj_change',
        'POST',
        [],
        {},
    ],  # 可以对表里的每条数据进行修改
    'crm_table_obj_add_view': [
        'table_obj_add',
        'GET',
        [],
        {},
    ],  # 可以访问数据增加页
    'crm_table_obj_add': [
        'table_obj_add',
        'POST',
        [],
        {},
    ],  # 可以创建表里的数据
}