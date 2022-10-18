from django.contrib import admin
from .models import TranSum,CustomerMaster,MemberMaster
# Register your models here.
# admin.site.register(TranSum)



@admin.register(CustomerMaster)
class CustomerMaster(admin.ModelAdmin):
    list_display=['user_id','username','group','first_name','last_name','email','phoneNumber','dob','address','company_code','sw_customer_id','registration_date','valid_date'] 

@admin.register(MemberMaster)
class MemberMasterAdmin(admin.ModelAdmin):
    list_display=['memberId','group','code','name','email','phoneNumber']



@admin.register(TranSum)
class TranSumAdmin(admin.ModelAdmin):
    list_display=('trId','group','code','fy','againstType','sp','part','fmr','isinCode','trDate','qty','balQty','rate','sVal','sttCharges','otherCharges','noteAdd')
