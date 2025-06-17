import os
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
from .models import ResearchResult
from .serializers import ResearchRequestSerializer, ResearchResultSerializer
from .agent import ResearchAgent
from .utils import export_to_pdf, export_to_csv

PDF_DIR = os.path.join(settings.MEDIA_ROOT, "pdfs")
CSV_DIR = os.path.join(settings.MEDIA_ROOT, "csvs")

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

class ResearchGenerateAPIView(APIView):
    def post(self, request):
        serializer = ResearchRequestSerializer(data=request.data)
        if serializer.is_valid():
            keyword = serializer.validated_data["keyword"]
            try:
                agent = ResearchAgent()
                data = agent.research(keyword)
                result = ResearchResult.objects.create(**data)
                return Response(ResearchResultSerializer(result).data, status=201)
            except Exception as e:
                return Response({"detail": str(e)}, status=500)
        return Response(serializer.errors, status=400)


class ResearchListCreateAPIView(generics.ListAPIView):
    queryset = ResearchResult.objects.all().order_by("-created_at")
    serializer_class = ResearchResultSerializer


class ResearchRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ResearchResult.objects.all()
    serializer_class = ResearchResultSerializer


class ResearchPDFDownloadAPIView(APIView):
    def get(self, request, pk):
        try:
            result = ResearchResult.objects.get(pk=pk)
        except ResearchResult.DoesNotExist:
            raise Http404("Research not found.")

        filename = os.path.join(PDF_DIR, f"{pk}_{result.keyword.replace(' ', '_')}.pdf")
        export_to_pdf(result, filename)

        if not os.path.exists(filename):
            raise Http404("PDF could not be generated.")
        return FileResponse(open(filename, 'rb'), as_attachment=True, filename=os.path.basename(filename))


class ResearchCSVDownloadAPIView(APIView):
    def get(self, request):
        results = ResearchResult.objects.all()
        filename = os.path.join(CSV_DIR, f"research_{len(results)}.csv")
        export_to_csv(results, filename)

        if not os.path.exists(filename):
            raise Http404("CSV could not be generated.")
        return FileResponse(open(filename, 'rb'), as_attachment=True, filename=os.path.basename(filename))
