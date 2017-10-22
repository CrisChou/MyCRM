from kingadmin.admin_base import BaseKingAdmin


class AdminSite(object):
    def __init__(self, *args, **kwargs):
        self.init_admin_dict = {}

    def register(self, model_class, admin_class=None):
        """注册admin表"""
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()
        
        admin_class.model = model_class

        if app_name not in self.init_admin_dict:
            self.init_admin_dict[app_name] = {}
        
        self.init_admin_dict[app_name][model_name] = admin_class



site = AdminSite()