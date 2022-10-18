from django.urls import path
from . import views

urlpatterns = [
    path('purchTransDet/',views.SavePurch.as_view()),
    path('purchTransSum/',views.RetTransSum.as_view()),
    path('purchTransDet/<int:pk>',views.MosRetrieveUpdate.as_view()),
    path('scriptSum/',views.RetriveAPISc2.as_view()),
    # path('transaction3/',views.RetInvSc1.as_view()),
    path('holdings/',views.RetHolding.as_view()),
    path('SaveMember/',views.SaveMember.as_view()),
    path('RetMember/',views.RetMember.as_view()),
    path('SaveCustomer/',views.SaveCustomer.as_view())
  
    
    
]