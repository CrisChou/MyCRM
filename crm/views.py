from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models
# Create your views here.


@login_required
def index(request):
    '''
    主页
    '''
    if request.method == 'GET':
        return render(request, 'crm/index.html')


@login_required
def enrollment(request):
    '''
    报名页
    '''
    enrollment_url = ''
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        class_id = request.POST.get('class_id')
        enrollment_url = '/crm/%s/%s/student_enrollment.html' % (customer_id,
                                                                 class_id, )
    customer_obj = models.CustomerInfo.objects.filter(status=0).values(
        'id', 'name')
    class_list_obj = models.ClassList.objects.all()
    print(customer_obj)
    return render(request, 'crm/enrollment.html', {
        'customer_obj': customer_obj,
        'class_list_obj': class_list_obj,
        'enrollment_url': enrollment_url
    })


def student_enrollment(request, customer_id, class_id):
    pass
