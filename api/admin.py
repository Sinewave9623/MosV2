from django.contrib import admin
from .models import TranSum,CustomerMaster,MemberMaster
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
# admin.site.register(TranSum)

class UserAdmin(BaseUserAdmin):
    list_display = ('userId','username','group','firstName','lastName','emailId','contactNo','dob','address','active','companyCode','sw_CustomerId','registration_Date','valid_Date')
    list_filter =('username','group','firstName','lastName','emailId','contactNo','dob','address')
    fieldsets = (
        ('User Credentials', {'fields': ('username','password')}),
        ('Personal info', {'fields': ('firstName','lastName','emailId','contactNo','dob',)}),
        ('Permissions', {'fields': ('is_active','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'firstName','lastName','emailId','contactNo','dob', 'password1', 'password2'),
        }),
    )
    search_fields = ('emailId',)
    ordering = ('emailId',)
    filter_horizontal = ()

admin.site.register(CustomerMaster, UserAdmin)
admin.site.unregister(Group)

# @admin.register(CustomerMaster)
# class CustomerMaster(admin.ModelAdmin):
#     list_display=['userId','userName','group','firstName','lastName','email','phoneNumber','dob','address','companyCode','swCustomerId','registrationDate','valid_date'] 

@admin.register(MemberMaster)
class MemberMasterAdmin(admin.ModelAdmin):
    list_display=['memberId','group','code','name','emailId','contactNo']



@admin.register(TranSum)
class TranSumAdmin(admin.ModelAdmin):
    list_display=('trId','group','code','fy','againstType','sp','part','fmr','isinCode','trDate','qty','balQty','rate','sVal','sttCharges','otherCharges','noteAdd')
