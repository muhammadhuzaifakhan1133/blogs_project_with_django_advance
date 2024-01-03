from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import BlogModel
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.pagination import PageNumberPagination

class BlogSearchFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="contains")
    description = CharFilter(field_name="description", lookup_expr="contains")

    class Meta:
        model = BlogModel
        fields = ['title', 'description']

class BlogsAPIView(APIView, PageNumberPagination):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogSearchFilter
    

    def post(self, request: Request):
        if not request.user.is_authenticated:
            return Response({
                "error": "User unauthenticated"
            })
        serialized = BlogSerializer(data = {
            "title": request.data.get("title"),
            "description": request.data.get("description"),
            "file_url": request.data.get("file_url"),
            "author_id": request.user.id,
        })
        if serialized.is_valid():
            serialized.save()
            return Response({"message": "blog saved successfully"})
        return Response(serialized.errors)

    def get(self, request: Request):
        if not request.user.is_authenticated:
            return Response({
                "error": "User unauthenticated"
            })
        query = BlogModel.objects.filter(author_id=request.user.id).select_related("author")
        # for apply backends (filter and etc) in your custom query
        for backend in self.filter_backends:
            query = backend().filter_queryset(request, query, self)
        blogs = self.paginate_queryset(query, request, self)
        serialized = BlogSerializer(blogs, many=True)
        return Response(serialized.data)
    
class BlogAPIView(APIView):

    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response({
                "error": "User unauthenticated"
            })
        blog = BlogModel.objects.filter(id=id, author_id=request.user.id).select_related("author").first()
        if blog is None:
            return Response({
                "error": "blog not found"
            })
        serialized = BlogSerializer(blog)
        return Response(serialized.data)

    def put(self, request, id):
        return self.put_or_patch(request, id)

    def patch(self, request, id):
        return self.put_or_patch(request, id)

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response({
                "error": "User unauthenticated"
            })
        blog = BlogModel.objects.filter(id=id, author_id=request.user.id).select_related("author").first()
        if blog is None:
            return Response({
                "error": "blog not found"
            })
        blog.delete()
        return Response({
            "message": "blog deleted successfully"
        })
    def put_or_patch(self, request: Request, id):
        if not request.user.is_authenticated:
            return Response({
                "error": "User unauthenticated"
            })
        if "author_id" in request.data:
            request.data.pop("author_id")
        blog = BlogModel.objects.filter(id=id, author_id=request.user.id).select_related("author").first()
        if blog is None:
            return Response({
                "error": "blog not found"
            })
        serialized = BlogSerializer(blog, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors)