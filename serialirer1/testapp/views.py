from django.shortcuts import render

from testapp.forms import EmployeeForm
from testapp.models import Employee
from testapp.utils import is_json
from testapp.mixins import SerializeMixin,HttpResponseMixin
from django.views.generic import View
import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt,name="dispatch")
class EmployeeListCBV(HttpResponseMixin,SerializeMixin,View):
    def get(self,request,*args,**kwargs):
        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return HttpResponse(json_data,content_type="application/json")

    def post(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"please send Valid json only"})
            return self.http_response(json_data,status=400)
        empdata = json.loads(data)
        form = EmployeeForm(empdata)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"msg":"Resoure Created Successfully"})
            return self.http_response(json_data)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.http_response(json_data,status=404)
@method_decorator(csrf_exempt,name="dispatch")
class EmployeeDetailCBV(HttpResponseMixin,SerializeMixin,View):
    def get_object_by_id(self,id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp = None
        return emp


    def get(self,request,id,*args,**kwargs):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data = json.dumps({"msg":"The Requested Resource is not available"})
            return self.http_response(json_data,status=404)
        else:
            json_data = self.serialize([emp,])
            return self.http_response(json_data)


    def put(self,request,id,*args,**kwargs):
        emp = self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({"msg":"No Matched Resource is Found,Not Possible to perform Updation"})
            return self.http_response(json_data,status=404)
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data=json.dumps({"msg":"please send valid json data only"})
            return self.http_response(json_data,status=400)
        provided_data = json.loads(data)
        original_data = {
                            'eno':emp.eno,
                            'ename':emp.ename,
                            'esal':emp.esal,
                            'eaddr':emp.eaddr
                        }
        original_data.update(provided_data)
        form = EmployeeForm(original_data,instance=emp)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"msg":"Resource Updated Successfully"})
            return self.http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.http_response(json_data,status=404)
    def delete(self,request,id,*args,**kwargs):
        emp = self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({"msg":"No data is matching with the given Id so Deletion Can not be performed"})
            return self.http_response(json_data,status=404)
        status,deleted = emp.delete()
        if status == 1:
            json_data = json.dumps({"msg":"Resource Deleted Succesfully"})
            return self.http_response(json_data)
        json_data = json.dumps({"msg":"unable To delete Plz Try Again"})
