from django.urls import path

from dashboard.views import StockListView, BillingReportView

urlpatterns = [
    path("stock/", StockListView.as_view()),
    path("reports/", BillingReportView.as_view()),
]
