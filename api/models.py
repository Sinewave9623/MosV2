from django.db import models
from .manager import CustomerUserManager
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class CustomerMaster(AbstractUser):
    userId=models.BigAutoField(primary_key=True)
    username = models.CharField(
        ('username'),
        max_length=30,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': ("A user with that username already exists."),
        }, 
    )
    group=models.CharField(max_length=10)
    firstName = models.CharField('first name', max_length=30, blank=True)
    lastName = models.CharField('last name', max_length=30, blank=True)
    emailId = models.EmailField(
        verbose_name='emailId address',
        max_length=40,
        blank=True,

    )
    contactNo=models.CharField(max_length=30,null = True, blank = True)
    dob=models.DateField(blank=True,null=True)
    photo=models.ImageField(upload_to='customer_photo',blank=True,default='')
    address=models.TextField(blank=True,null=True)
    active = models.BooleanField(default=False)
    companyCode = models.CharField(max_length=30,blank=True,null=True)
    sw_CustomerId = models.IntegerField(null=True, blank=True)
    registration_Date= models.DateField(null=True, blank=True)
    valid_Date=models.DateField(null=True, blank=True) 

    objects = CustomerUserManager()

    EMAIL_FIELD = 'emailId'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['emailId']

    class Meta:
        verbose_name = ('CustomerMaster')
        verbose_name_plural = ('CustomerMasters')

    def __str__(self):
        return self.group 

# ------------------------Member Master
class MemberMaster(models.Model):
    memberId=models.BigAutoField(primary_key=True)
    group=models.CharField(max_length=10)
    code=models.CharField(max_length=10)
    name=models.CharField(max_length=30)
    emailId=models.EmailField(max_length=30)
    contactNo=models.CharField(max_length=30,null = True, blank = True)

    def __str__(self):
        return self.code


class TranSum(models.Model):
    TYPE=(
        ('Shares','Shares'),
        ('Mutual Funds','Mutual Funds'),
        ('Futures & Options','Futures & Options'),
        ('Day Trading','Day Trading'),
        ('Trading','Trading')
    )
    FY=(
        
        ('2021-2022','2021-2022'),
        ('2022-2023','2022-2023'),
        ('2023-2024','2023-2024'),
        ('2024-2025','2024-2025'),
        ('2025-2026','2025-2026'),
        ('2026-2027','2026-2027'),
        ('2027-2028','2027-2028'),
        ('2028-2029','2028-2029')
    )
    trId = models.BigAutoField(primary_key=True)
    group=models.CharField(max_length=10)
    code=models.CharField(max_length=10)
    fy=models.CharField(max_length=9,choices=FY)
    againstType=models.CharField(max_length=20,choices=TYPE)
    sp=models.CharField(max_length=2)
    part=models.CharField(max_length=30)
    sno=models.IntegerField(blank=True,null=True)
    fmr=models.FloatField(null=True, blank=True)
    isinCode=models.CharField(max_length=30,null=True, blank=True)
    trDate=models.DateField()
    qty=models.IntegerField()
    rate=models.DecimalField(max_digits=65, decimal_places=2)
    sVal=models.DecimalField(max_digits=65, decimal_places=2)
    sttCharges=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True)
    otherCharges=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True)
    noteAdd=models.CharField(max_length=200,blank=True)
    marketRate=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=Decimal('0.00'))
    def validate_decimals(value):
        try:
            return round(float(value), 2)
        except:
            raise ValidationError(
                ('%(value)s is not an integer or a float  number'),
                params={'value': value},
            )
    marketValue=models.FloatField(validators=[validate_decimals],blank=True,null=True)
    HoldingValue=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    avgRate=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    scriptSno=models.IntegerField(blank=True,null=True)
    empCode=models.CharField(max_length=10,blank=True,null=True)
    clDate=models.DateField(null=True,blank=True)
    clRate=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    clQTY=models.IntegerField(blank=True,null=True,default=0)
    clValue=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    clsttCharges=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    clOtherCharges=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    balQty=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    # balQty=models.IntegerField(blank=True,null=True,default=0)
    dayTrade=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True,default=0)
    strategyDate=models.DateField(null=True,blank=True)
    strategyTrigger=models.DecimalField(max_digits=65, decimal_places=2,blank=True,null=True)

    

    
  

     

