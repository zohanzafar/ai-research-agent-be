from django.urls import path
from . import views

urlpatterns = [
    path("research/", views.ResearchListCreateAPIView.as_view(), name="research-list"),
    path("research/generate/", views.ResearchGenerateAPIView.as_view(), name="research-generate"),
    path("research/<int:pk>/", views.ResearchRetrieveDestroyAPIView.as_view(), name="research-detail"),
    path("research/<int:pk>/download-pdf/", views.ResearchPDFDownloadAPIView.as_view(), name="research-download-pdf"),
    path("research/download-csv/", views.ResearchCSVDownloadAPIView.as_view(), name="research-download-csv"),
]
