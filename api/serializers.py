from attr import field, fields
from rest_framework import serializers
from .models import TranSum,CustomerMaster,MemberMaster


 # ---------------------- Saving API
class SavePurchSerializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=('trId','group','code','fy','againstType','sp','part','fmr','isinCode','trDate','qty','balQty','rate','sVal','sttCharges','otherCharges','noteAdd')
# ------------------------ Retriveing API
class RetTransSumSerializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=['trId','trDate','qty','rate','sVal','sttCharges','otherCharges','noteAdd']

# ------------------------ Retrivng API Screen No2 (opening, addition, closing)
class TranSumRetrivesc2Serializer(serializers.ModelSerializer):
    data1= serializers.SerializerMethodField()


    def get_data1(self, obj):
        
        return None
    class Meta:
        model=TranSum
        fields=['trId','fmr','isinCode','data1']


class RetInvSc1serializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=['trId','sp','part','fmr','isinCode','marketValue']

# ---------------------- Member saving API
class SaveMemberSerializer(serializers.ModelSerializer):
    # member=serializers.StringRelatedField()

    class Meta:
        model=MemberMaster
        fields=['code','name','email','phoneNumber']

# # -----------------------RetMember api
class RetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberMaster
        fields=['memberId','name','email','phoneNumber']

class SavecustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerMaster
        fields=['user_id','first_name','last_name','email','phoneNumber','username']







        
    