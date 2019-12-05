from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from testapp.mixins import HttpResponseMixin,SerializeMixin
from testapp.utils import is_json
from testapp.forms import EmployeeForm
import json
from testapp.models import Employee

@method_decorator(csrf_exempt,name="dispatch")
class EmployeeAllCrud(HttpResponseMixin,SerializeMixin,View):
    def get_object_by_id(self,id):
        try:
            emp = Employee.objects.get(id=id)
            print(emp)
        except:
            emp = None
        print(emp)
        return emp

    def get(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"please send a valid json data only"})
            return self.http_response(json_data,status=400)
        pdata = json.loads(data)
        id = pdata.get("id",None)
        if id is not None:
            emp = self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps({"msg":"The requested Resource is not available with the Given id"})
                return self.http_response(json_data,status=400)
            json_data = self.serialize([emp,])
            return self.http_response(json_data)
        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return self.http_response(json_data)



    def post(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"please send a valid json data only"})
            return self.http_response(json_data,status=400)
        empdata = json.loads(data)
        form = EmployeeForm(empdata)
        if form.is_valid():
            form.save(commit = True)
            json_data = json.dumps({"msg":"Resource Created Successfully"})
            return self.http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.http_response(json_data,status=400)



    def put(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"Please Send Valid Json data Only"})
            return self.http_response(json_data,status=400)
        pdata = json.loads(data)
        id = pdata.get('id',None)
        if id is None:
            json_data = json.dumps({"msg":"To preform Update Id must be required"})
            return self.http_response(json_data,status=400)
        emp = self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({"msg":"The required resource is not available with the Matched ID" })
            return self.http_response(json_data,status=404)
        provided_data = json.loads(data)
        original_data = {'eno':emp.eno,'ename':emp.ename,'esal':emp.esal,'eaddr':emp.eaddr}
        original_data.update(provided_data)
        form = EmployeeForm(original_data,instance=emp)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"msg":"Resource Updated Successfully"})
            return self.http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.http_response(json_data,status=400)


    def delete(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({"msg":"Please send a valid json data"})
            return http_response(json_data,status=400)
        pdata = json.loads(data)
        id = pdata.get('id',None)
        if id is not None:
            emp = self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps({"msg":"The Requested resource not available with matched id"})
                return self.http_response(json_data,status=404)
            status,deleted_item = emp.delete()
            print(status)
            if status==1:
                json_data = json.dumps({"msg":"Resource Deleted Successfull"})
                return self.http_response(json_data)
            json_data = json.dumps({"msg":"unable to delete please try again"})
            return self.http_response(json_data)
        json_data = json.dumps({"msg":"To perform deletion id is mandatory,please provide "})
        return self.http_response(json_data,status=404)
