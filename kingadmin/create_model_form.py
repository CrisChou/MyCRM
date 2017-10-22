from django.forms import ModelForm


def create_model_form(admin_class, form_add=False):
    '''
    动态生成modelform
    from_add: False 默认是创建修改的表单，True时候为添加
    '''

    class Meta:
        model = admin_class.model
        if form_add:
            fields = "__all__"
        else:
            fields = "__all__"
            exclude = admin_class.readonly_fields

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})

        return ModelForm.__new__(cls)

    model_form = type('NewModelForm', (ModelForm, ),
                      {'Meta': Meta,
                       '__new__': __new__})
    return model_form
