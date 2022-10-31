from decimal import Decimal
from .models import TranSum,MemberMaster,CustomerMaster
from django.db.models import Sum
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.views import APIView
from .serializers import (SavePurchSerializer,RetTransSumSerializer,
SaveMemberSerializer,RetMemberSerializer,SavecustomerSerializer)
import copy

# -------------------- SavePurch API
class SavePurch(APIView):   
    def post(self, request, format=None):
        dic = copy.deepcopy(request.data)
        dic["balQty"] = request.data["qty"]
        serializer = SavePurchSerializer(data=dic)
        if serializer.is_valid():
            serializer.save() 
            return Response({'status':True,'Message': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------- RetTransSum API
class RetTransSum(generics.ListAPIView):
    queryset=TranSum.objects.all()
    serializer_class=RetTransSumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group','code','againstType','part']

    # -------------------- Overriding Queryset
    def get_queryset(self):
        option = self.request.query_params.get('option')
        dfy = self.request.query_params.get('dfy')
        try:
            start_fy=dfy[:4]+"-04-01"
            end_fy=dfy[5:]+"-03-31"
        except:
            raise Http404

        if option == 'O':

            return self.queryset.filter(trDate__lt=start_fy)
            
        elif option=='A':
            
            return self.queryset.filter(trDate__range=(start_fy,end_fy))
             
             
#   ------------------------- Update and Retrive API
class RetTransSumUpdate(generics.RetrieveUpdateAPIView):
    queryset=TranSum.objects.all()
    serializer_class=RetTransSumSerializer
    def update(self, request, *args, **kwargs):
       oldqty = self.request.query_params.get('oldqty')
       balqty = self.request.query_params.get('balqty')
    #    transid = self.request.query_params.get('transid')
 
    #    print(oldqty,balqty,transid)
       
       dict =  copy.deepcopy(request.data)
       dict["balQty"] = float(balqty) - float(oldqty) + float(dict["qty"])

    #    print(dict)

       partial = kwargs.pop('partial', False)
       instance = self.get_object()
       serializer = self.get_serializer(instance, data=dict, partial=partial)
       serializer.is_valid(raise_exception=True)
       self.perform_update(serializer)

       result = {
        "status": True,
        "msg": "Data successfully updated",
        "data":dict
        
       }
       return Response(result)

 # Retrive API Screen No Two
 
class RetScriptSum(APIView):
    def get(self, request, format=None):
        # ------------ fetching parameter in  Url
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        part = self.request.query_params.get('part')
        dfy = self.request.query_params.get('dfy')
        try:
            start_fy=dfy[:4]+"-04-01"
            end_fy=dfy[5:]+"-03-31"
        except:
            raise Http404
        # --------------------- Opening
        opening = TranSum.objects.filter(trDate__lt=start_fy,group=group,code=code,againstType=againstType,part=part).values_list('qty','sVal','isinCode','fmr')
        open=list(opening)
        varop=0
        varopval=0
        for i in open:
            op=int(i[0])
            opval=int(i[1])
            varop=varop+op
            varopval=varopval+opval 
        # print(varop) 
        # print(varopval)  
        # --------------------- Additions
        addition = TranSum.objects.filter(trDate__range=(start_fy,end_fy),group=group,code=code,againstType=againstType,part=part).values_list('qty','sVal','marketRate','marketValue','isinCode','fmr','avgRate')
        # print("Daaaa",addition)
        b=list(addition)
        # print("Daaaa",b)
        varadd=0
        varaddval=0
        for i in b:
            ad=int(i[0])
            addval=int(i[1])
            mktRate=float(i[2])
            if i[3] == None:
                i3=0
            else:
                i3=i[3]
            mktvalue=float(i3)
            
            global isinCode
            isinCode=i[4]
           
            fmr=i[5]

        
            varadd=varadd+ad
            varaddval=varaddval+addval
        # print(varadd)
        # print(varaddval)  
        # ------------------------- Closing
        closing=varadd+varop
        #-------------------------- opening and addition all values Sum
        InvValue=varaddval+varopval
       
        InvValue=float(InvValue)
        # InvValue1=round(InvValue,2)

        # print("InvValue",InvValue1,type(InvValue1))

        # -------------------------- Average Rate(total values / total qty)(InvValue/closing)
        try:
            avgRate=InvValue / closing
            avgRate=round(avgRate,2)
        except ZeroDivisionError:
            avgRate=0
        # print('Avg',avgRate,type(avgRate))
       

        # print("avgRate----->",avgRate)
           
        context={
            'isinCode':isinCode,
            'fmr':fmr,
            'opening':varop,
            'addition':varadd,
            'sales':0,
            'closing':closing,
            'invValue':InvValue,
            'avgRate':avgRate,
            'marketRate':mktRate,
            'mktvalue':mktvalue
        }
       
        return Response({'status':True,'msg':'done','data':context})

class RetHolding(APIView):

    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        # dfy = self.request.query_params.get('dfy')
        againstType = self.request.query_params.get('againstType')
       
        # try:
        #     start_fy=dfy[:4]+"-04-01"
        #     end_fy=dfy[5:]+"-03-31"
        # except:
        #     raise Http404

        all_data = TranSum.objects.filter(group=group,code=code,againstType=againstType).values_list('rate','balQty','marketRate','part')
        data_ls = []
        # print("Daaaaa",all_data)
        for data in all_data:

            dic = {}
            dic['part']=data[3]
            dic["holdQty"] =int(data[1])
            
    
            if data[1] == None:
                data_1 = 0
            else:
                data_1 = data[1]

            if data[2]==None:
                data_2=0
            else:
                data_2=data[2]

            
            dic["InvValue"] = (data[0])* (data_1)
            dic["mktvalue"] = data_1 * (data_2)
            # print("Dataaaa--->",dic)
            
            data_ls.append(dic)
        # print("dataaaaa---->",dic)
        return Response({'status':True,'msg':'done','data':data_ls})



# -------------------------- SaveMember api
class SaveMember(APIView):
    def post(self, request, format=None):
        serializer = SaveMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'Message': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # -------------------------- RetMember API
class RetMember(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        member=MemberMaster.objects.filter(group=group)
        serializer=RetMemberSerializer(member,many=True)
        return Response({'status':True,'msg':'done','data':serializer.data})

# ---------------------------- updated delete api mrmber
class MemberUpdadeDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=MemberMaster.objects.all()
    serializer_class=SaveMemberSerializer


# -------------------------- SaveCutomer api
class SaveCustomer(APIView):
    def post(self, request, format=None):
        serializer = SavecustomerSerializer(data=request.data)
       
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # -------------------------- RetCustomer API
class RetCustomer(generics.ListAPIView):
    queryset=CustomerMaster.objects.all()
    serializer_class=SavecustomerSerializer
    
# ---------------------------- updated delete api Customer
class CustomerUpdadeDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomerMaster.objects.all()
    serializer_class=SavecustomerSerializer
