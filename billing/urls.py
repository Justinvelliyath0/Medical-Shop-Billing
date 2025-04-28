from django.urls import path

from billing.views import CreateBillView

urlpatterns = [path("", CreateBillView.as_view())]
