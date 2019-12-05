from rest_framework import serializers
from testapp.models import EmployeeModel

class EmployeeSerializer(serializers.Serializer):
    idno = serializers.IntegerField()
    name = serializers.CharField()
    desg = serializers.CharField()
    salary = serializers.FloatField()


    # one Field validation
    def validate_salary(self,salary):
        if salary>=10000:
            return salary
        else:
            raise serializers.ValidationError("salary must be greater than or equal to 10000")
    #one object validation(multifield validation)
    def validate(self,data):
        if data.get('desg')=="Manager":
            if data.get('salary')>=50000:
                return data
            else:
                raise serializers.ValidationError("Manage salary must be minimum of 50000.00")
        else:
            return data


    def create(self,validated_data):
        return EmployeeModel.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.idno = validated_data.get("idno",instance.idno)
        instance.name = validated_data.get("name",instance.name)
        instance.desg = validated_data.get("desg",instance.desg)
        instance.salary = validated_data.get("salary",instance.salary)

        instance.save()
        return instance
