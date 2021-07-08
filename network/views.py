from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.core import serializers
from helper_functions import check_logged_in_user_following
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Follow, User



# View functions



def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def compose(request):
    # Get content of post
    data = json.loads(request.body)
    post = data.get('post', "")
    user = request.user

        # save them into the Post model
    send = Post(
            post = post,
            user = user
        )
    send.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

@login_required
@require_http_methods(["GET"])
def profile(request, user_id):
    # get all post by user
    user_posts = Post.objects.filter(user=user_id).order_by('post')
    # get all user likes
    totalLikes = []
    for post in user_posts:
        totalLikes.append(post.likes)
    likes = sum(totalLikes)
    # get user info from User model
    userdata = User.objects.get(pk=user_id)
    logged_in_user = str(request.user)
    logged_in_user_obj = User.objects.get(username=request.user)
    date_joined = userdata.date_joined
    dateJoined = str(date_joined)[:10]
    # get following/followers info
    following = Follow.objects.filter(following_id=user_id)
    followers = Follow.objects.filter(follower_id=user_id)
    # django paginator
    paginator = Paginator(user_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_following = check_logged_in_user_following(followers, logged_in_user)

    # logic to display follow button dynamically
    if is_following:
        is_followed = True
        return render(request, "network/profile.html", {
            'posts': page_obj, 'userdata': userdata, 'current_user': logged_in_user, 'date':dateJoined,
            'following': following.count(), 'followers': followers.count(),
             'current_user_id': logged_in_user_obj.id, 'followers_item': followers, 'messages': is_followed,
             'likes': likes
            })
    else:
        return render(request, "network/profile.html", {
                'posts': page_obj, 'userdata': userdata, 'current_user': logged_in_user, 'date':dateJoined,
                'following': following.count(), 'followers': followers.count(),
                'current_user_id': logged_in_user_obj.id, 'followers_item': followers,
                'likes': likes
                })


@require_http_methods(["GET"])
def post_view(request, posts):
    if posts:
        # get all posts from everyone using model manager function called get_username
        all_data_serial = Post.custom.get_username()
        user = str(request.user)
        paginator = Paginator(all_data_serial, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # serialize data to send (didn't use it because data from model manager is already serialized)
        # data = serializers.serialize('json', Post.objects.order_by('post').all())
        return JsonResponse({"data":all_data_serial, "loggedInUser":user}, safe=False)

@login_required
@require_http_methods(["GET"])
def following_view(request):
    # get people logged in user follows 
    get_following = Follow.objects.filter(following=request.user)
    # create empty list
    search_posts = []

    ''' for each loop, get the user followed by logged in user and save in a variable
    use the variable to search the post model to get posts by that user
    if the user has more than one post, convert to a list and append to empty list, 
    else, remove the first and only post from user and add to search list.
    The idea is to flatten the querySet result which returns nested lists and turn them into one list
    '''
    for user in list(get_following):
        result = Post.objects.filter(user=user.follower)
        if len(list(result)) > 1:
            list_result = list(result)
            for each_result in list_result:
                search_posts.append(each_result)
        else:
            list_result = list(result)
            search_posts.append(result[0])
            
    # Paginate
    paginator = Paginator(search_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {'posts': page_obj})


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def like_view(request, post_id):
    if request.method == "PUT":
        # ensure there is a post id sent
        if not post_id:
            return JsonResponse({
                "error": "Not post_id sent."
            }, status=400)
        post = Post.objects.get(pk=post_id)
        user = request.user
        # retrieve data from AJAX and increment likes manually
        data = json.loads(request.body)
        # get the likers of the post
        likers = []
        likers.append(post.likers)
        

        if data.get("likes") == True:
            # ensure user can like a post only once
            if user in likers:
                return
            else:
                post.likes += 1
                post.likers = user
                post.save()
            return JsonResponse({"message": "Post liked successfully.", "likes": post.likes}, safe=False, status=201)
        else:
            return JsonResponse({
                "error": "PUT request required."
            }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def dislike_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    data = json.loads(request.body)
    print(post.likers)
    print(user)
    if data.get('likes') == False:
        
        if user == post.likers:
            post.likers = None
            post.likes = post.likes - 1
            print('Post disliked')
            post.save()
            return JsonResponse({"message": "Post disliked successfully."}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@login_required
@require_http_methods(["POST"])
def follow(request, user_id):
    user_to_follow = user_id
    user_object = User.objects.get(username=request.user)
    follow_object = User.objects.get(pk=user_to_follow)
 
    # You can only save User object into a foreignkey field 
    f = Follow.objects.create(
        following = user_object,
        follower = follow_object
    )
    f.save()
    return HttpResponseRedirect(f'/network/profile/{user_id}')

@login_required
@require_http_methods(["POST"])
def unfollow(request, user_id):
    user_to_unfollow = User.objects.get(pk=user_id)
    logged_in_user = User.objects.get(username=request.user)
    Follow.objects.get(following=logged_in_user,follower=user_to_unfollow).delete()
    return HttpResponseRedirect(f'/network/profile/{user_id}')

@login_required
@require_http_methods(["PUT"])
def edit_view(request, post_id):
    post_obj = Post.objects.get(pk=post_id)
    data = json.loads(request.body)
    print(data.get('post'))
    post_obj.post = data.get('post')
    post_obj.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)

