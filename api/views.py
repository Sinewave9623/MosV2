from .models import TranSum,MemberMaster,CustomerMaster
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q,Sum
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.views import APIView
import pandas as pd
import requests
from .serializers import (SavePurchSerializer,RetTransSumSerializer,
TranSumRetrivesc2Serializer,RetInvSc1serializer,SaveMemberSerializer,RetMemberSerializer,SavecustomerSerializer)



# -------------------- SavePurch API
class SavePurch(APIView):
    def post(self, request, format=None):
        serializer = SavePurchSerializer(data=request.data)
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
class MosRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset=TranSum.objects.all()
    serializer_class=RetTransSumSerializer
    def update(self, request, *args, **kwargs):
       partial = kwargs.pop('partial', False)
       instance = self.get_object()
       serializer = self.get_serializer(instance, data=request.data, partial=partial)
       serializer.is_valid(raise_exception=True)
       self.perform_update(serializer)
       result = {
        "status": True,
        "message": "Data successfully updated",
        "data": serializer.data,
       }
       return Response(result)
    # # ---------------  Overriding Destroy Method

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response({'status':True,'Message': 'You have successfully Deleted'})
 
 # Retrive API Screen No Two
 
class RetriveAPISc2(APIView):
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
        opening = TranSum.objects.filter(trDate__lt=start_fy,group=group,code=code,againstType=againstType,part=part).values_list('qty')
        open=list(opening)
        varop=0
        for i in open:
            w=int(i[0])
            varop=varop+w 
        print(varop)  
        # --------------------- Additions
        addition = TranSum.objects.filter(trDate__range=(start_fy,end_fy),group=group,code=code,againstType=againstType,part=part).values_list('qty')
        # print("Daaaa",addition)
        b=list(addition)
        varadd=0
        for i in b:
            w=int(i[0])
            varadd=varadd+w   
        # ------------------------- Closing
        closing=varadd+varop
        # serializer = TranSumRetrivesc2Serializer(addition, many=True,context={'request': request})
        return Response({'status':True,'msg':'done','opening':varop,'addition':varadd,'closing':closing})

class RetHolding(APIView):

    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        part = self.request.query_params.get('part')
        dfy = self.request.query_params.get('dfy')
        againstType = self.request.query_params.get('againstType')
       
        try:
            start_fy=dfy[:4]+"-04-01"
            end_fy=dfy[5:]+"-03-31"
        except:
            raise Http404

        all_data = TranSum.objects.filter(group=group,code=code,againstType=againstType).values_list('rate','balQty','marketRate','part')
        # print("Allll",all_data)
        # return all_data
        # return Response(all_data)
        data_ls = []
        for data in all_data:
            dic = {}
            dic['part']=data[3]
            dic["holdQty"] =data[1]
            dic["InvValue"] = (data[0]) * (data[1])
            dic["mktvalue"] = (data[1]) * (data[2])
            data_ls.append(dic)
        print("dataaaaa---->",dic)
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
class RetMember(generics.ListAPIView):
    queryset=MemberMaster.objects.all()
    serializer_class=RetMemberSerializer

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
            return Response({'status':True,'Message': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # -------------------------- RetCustomer API
class RetCustomer(generics.ListAPIView):
    queryset=CustomerMaster.objects.all()
    serializer_class=SavecustomerSerializer
    
# ---------------------------- updated delete api Customer
class CustomerUpdadeDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomerMaster.objects.all()
    serializer_class=SavecustomerSerializer