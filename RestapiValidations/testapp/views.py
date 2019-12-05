from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.parsers import JSONParser
from testapp.serializers import EmployeeSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from testapp.models import EmployeeModel


@method_decorator(csrf_exempt,name = "dispatch")
class EmployeeAPICURD(View):
    def post(self,request):
        stream = io.BytesIO(request.body)
        p_data = JSONParser().parse(stream)
        es = EmployeeSerializer(data=p_data)
        if es.is_valid():
            es.save()
            message = {"msg":"Employee record is Saved"}
        else:
            message = {"msg":es.errors}
        json_data = JSONRenderer().render(message)
        return HttpResponse(json_data,content_type="application/json")

    def put(self,request):
        stream = io.BytesIO(request.body)
        p_data = JSONParser().parse(stream)
        emp = EmployeeModel.objects.get(idno=p_data['idno'])
        es = EmployeeSerializer(emp,data=p_data,partial=True)
        if es.is_valid():
            es.save()
            message = {"msg":"Employee Record is Updated Successfully"}
        else:
            message = {"msg":es.errors}
        json_data = JSONRenderer().render(message)
        return HttpResponse(json_data,content_type="application/json")
