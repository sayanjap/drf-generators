__all__ = ['API_VIEW', 'API_URL']

API_URL = """from django.conf.urls import include, url
from {{ app }} import views


urlpatterns = [
{% for model in models %}
  url(r'^{{ model|lower }}/(?P<id>[0-9]+)/$', views.{{ model }}APIRetrieveView.as_view()),
  url(r'^{{ model|lower }}/(?P<id>[0-9]+)/update/$', views.{{ model }}APIUpdateView.as_view()),
  url(r'^{{ model|lower }}/(?P<id>[0-9]+)/delete/$', views.{{ model }}APIDeleteView.as_view()),
  url(r'^{{ model|lower }}/list/$', views.{{ model }}APIListView.as_view()),
  url(r'^{{ model|lower }}/$', views.{{ model }}APICreateView.as_view()),
{% endfor %}
]
"""

API_VIEW = """from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from {{ app }}.serializers import {{ serializers|join:', ' }}
from {{ app }}.models import {{ models|join:', ' }}
{% for model in models %}

class {{ model }}APIListView(generics.ListAPIView):
    serializer_class = {{ model }}Serializer
    queryset = NotImplemented
    
    def list(self, request, *args, **kwargs):
        items = {{ model }}.objects.all()
        ser = self.get_serializer(items, many=True).data
        return Response(ser, status=status.HTTP_200_OK)
        
        
class {{ model }}APIRetrieveView(generics.RetrieveAPIView):
    serializer_class = {{ model }}Serializer
    queryset = NotImplemented   
    
    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            item = {{ model }}.objects.get(pk=id)
            serializer = {{ model }}Serializer(item)
            return Response(serializer.data)
        except {{ model }}.DoesNotExist:
            return Response(status=404)
            
            
class {{ model }}APIUpdateView(generics.UpdateAPIView):
    serializer_class = {{ model }}Serializer
    queryset = NotImplemented  
    
    def update(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            item = {{ model }}.objects.get(pk=id)
        except {{ model }}.DoesNotExist:
            return Response(status=404)
        serializer = {{ model }}Serializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
        
class {{ model }}APIDeleteView(generics.DestroyAPIView):
    serializer_class = {{ model }}Serializer
    queryset = NotImplemented          
    
    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            item = {{ model }}.objects.get(pk=id)
        except {{ model }}.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
        

class {{ model }}APICreateView(generics.CreateAPIView):
    serializer_class = {{ model }}Serializer
    queryset = NotImplemented

    def create(self, request, *args, **kwargs):
        serializer = {{ model }}Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
{% endfor %}"""
