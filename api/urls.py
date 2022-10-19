from django.urls import path
from . import views

urlpatterns = [
    path('purchTransDet/',views.SavePurch.as_view()),
    path('purchTransSum/',views.RetTransSum.as_view()),
    path('purchTransDet/<int:pk>',views.MosRetrieveUpdate.as_view()),
    path('scriptSum/',views.RetriveAPISc2.as_view()),
    # path('transaction3/',views.RetInvSc1.as_view()),
    path('holdings/',views.RetHolding.as_view()),
    path('saveMember/',views.SaveMember.as_view()),
    path('retMember/',views.RetMember.as_view()),
    path('saveMember/<int:pk>',views.MemberUpdadeDelete.as_view()),
    path('saveCustomer/',views.SaveCustomer.as_view()),
    path('retCustomer/',views.RetCustomer.as_view()),
    path('saveCustomer/<int:pk>',views.CustomerUpdadeDelete.as_view())
  
    
    
]