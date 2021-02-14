from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Post
from posts.serializers import PostSerializer

@api_view(['GET', 'POST'])
def post_list(request):
  if request.method == 'GET':
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({ "data": serializer.data })
  
  if request.method == 'POST':
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({ "message": "create successfully", "data": serializer.data }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
def post_detail(request, post_id):
  try:
    post = Post.objects.get(pk=post_id)
  except Post.DoesNotExist:
    return Response({ "message": "requested post not found" }, status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = PostSerializer(post)
    return Response({ "data": serializer.data })

  if request.method == 'DELETE':
    post.delete()
    return Response({ "message": "Post has been deleted !" }, status=status.HTTP_204_NO_CONTENT)
  
  if request.method == 'PUT':
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({ "message": "update post successfully", "data": serializer.data })
    return Response({ "message": "update post failed" }, status=status.HTTP_400_BAD_REQUEST)

