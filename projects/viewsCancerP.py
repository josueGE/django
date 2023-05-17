from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CancerPulmonarSerializer
from .models import CancerPulmonar
from rest_framework.response import Response
from rest_framework import status

class CancerPulmonarViewSet(viewsets.ViewSet):
    serializer_class = CancerPulmonarSerializer
    queryset = CancerPulmonar.objects.all()
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            cancer_pulmonar = CancerPulmonar.objects.get(pk=pk)
        except CancerPulmonar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cancer_pulmonar)
        return Response(serializer.data)
    def update(self, request, pk=None):
        try:
            cancer_pulmonar = CancerPulmonar.objects.get(pk=pk)
        except CancerPulmonar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cancer_pulmonar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        try:
            cancer_pulmonar = CancerPulmonar.objects.get(pk=pk)
        except CancerPulmonar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cancer_pulmonar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def list(self, request):
        anemias = CancerPulmonar.objects.all()
        serializer = self.serializer_class(anemias, many=True)
        return Response(serializer.data)