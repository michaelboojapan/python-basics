from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse
from django.conf import settings

from .models import Tweet

from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={})


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    data = request.POST
    serializer = TweetSerializer(data=data)
    if serializer.is_valid():
        obj = serializer.save(user=request.user)

        next_url = request.POST.get('next') or None
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        return Response(serializer.data)
    return Response({}, status=400)


@api_view(['delete', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message': 'you can not delete this tweet'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet deleted'}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_like_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    msg = "user liked tweet"
    if request.user in obj.likes.all():
        obj.likes.remove(request.user)
    else:
        msg = "user unliked tweet"
        obj.likes.add(request.user)

    return Response({'message': msg}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')

        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()

        msg = "user liked tweet"
        if action == 'like':
            obj.likes.add(request.user)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            msg = "user unliked tweet"
        elif action == 'retweet':
            msg = "user retweet"
            pass


    return Response({'message': msg}, status=200)


#
#
# end here
#
#
def tweet_list_view_pure_django(request):
    queryset = Tweet.objects.all()
    tweets_list = [{'id': qs.id, 'content': qs.content} for qs in queryset]
    data = {
        'response': tweets_list
    }
    # return render(request, 'tweets/tweet_list.html', data)
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    status = 200
    data = {
        'id': tweet_id,
        # 'image_path': obj.image.url,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content

    except:
        data['message'] = 'Not Found',
        status = 404

    return JsonResponse(data, status=status)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user = None
        if request.is_agax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user or None
        obj.save()
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    context = {
        'form': form
    }

    return render(request, 'pages/tweet_create.html', context)

# def tweet_create_view(request, *args, **kwargs):
#     my_form = RawTweetForm()
#     if request.method == 'POST':
#         my_form = RawTweetForm(request.POST)
#         if my_form.is_valid():
#             print(my_form.cleaned_data)
#             Tweet.objects.create(**my_form.cleaned_data)
#
#     context = {
#         'form': my_form
#     }
#     return render(request, 'tweets/tweet_create.html', context)

# def tweet_create_view(request, *args, **kwargs):
#     print("#"*36)
#     if request.method == 'POST':
#         my_new_title = request.POST.get('title')
#         print(my_new_title)
#         # Tweet.objects.get(id=1)
#
#     context = {
#     }
#     return render(request, 'tweets/tweet_create.html', context)
