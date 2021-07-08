from network.models import Post


def check_logged_in_user_following (model, user):
    ''''utility function to compare if user is followed by logged in user
    model: list of queryset of followers of the selected user
    user: the logged in user

    returns: boolean, true if user in model list else false
    '''
    #convert model to list
    model_to_list = list(model)
    list_of_usernames = [str(each_user) for each_user in model_to_list]
    return user in list_of_usernames

def get_followings_post(username, followDB, postDB):
    '''utility function to get posts of everyone a particular user follows
    
    @params username: the username 
    @params follow: followings Database
    @param post: the database containing all posts

    returns: List of all post the user follows
    '''

    #get the people the user follows
    people_user_follows = followDB.objects.filter(following = username)

    #get their post from the post db
    all_followed_posts = []
    for user in people_user_follows:
        #get current username to index db
        current_user = user.follower
        current_user_post = postDB.objects.filter(user = current_user)
         



def format_user_followings_post(post):
    '''utiltiy function to flatten the list of post a user follows
    
    @params post: list of post by followings

    returns: list of post destructured
    '''

def flatten_array(querySet, arr):
    if type(querySet) == "list":
        flatten_array(arr)
    arr.append(querySet)
    


    
