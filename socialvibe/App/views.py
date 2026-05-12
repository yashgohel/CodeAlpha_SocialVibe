from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Post, Like, Comment, Follower, Message, Notification, Story
from django.db.models import Q

def create_notification(user, sender, n_type, post=None, message=None):
    if user != sender:
        Notification.objects.create(
            user=user,
            sender=sender,
            notification_type=n_type,
            post=post,
            message=message
        )

# Create your views here.
def index(request):
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "signup":
            fullname = request.POST['fullname']
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with that email already exists.")
                return redirect('index')
            
            user = User.objects.create(fullname=fullname, email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('home')

        elif action == "login":
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = User.objects.filter(email=email, password=password).first()
            if user is not None:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials.")
                return redirect('index')
        
        elif action == "forgot_password":
            email = request.POST.get('email')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            
            user = User.objects.filter(email=email).first()
            if user:
                if new_password == confirm_new_password:
                    user.password = new_password
                    user.save()
                    messages.success(request, "Password reset successfully! You can now log in.")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "No account found with that email address.")
            return redirect('index')
                
    return render(request, 'login.html')



def home(request):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    
    if request.method == "POST":
        content = request.POST.get('content')
        attachment = request.FILES.get('attachment')
        feeling = request.POST.get('feeling')
        
        if content or attachment or feeling:
            Post.objects.create(
                user=user,
                content=content,
                attachment=attachment,
                feeling=feeling
            )
            return redirect('home')

    # Get search query
    search_query = request.GET.get('search', '')
    search_results = []
    if search_query:
        if search_query.startswith('@'):
            q = search_query[1:]
            search_results = User.objects.filter(Q(fullname__icontains=q) | Q(email__icontains=q)).exclude(id=user.id)
        else:
            search_results = User.objects.filter(fullname__icontains=search_query).exclude(id=user.id)

    # Get posts from following and self
    following_ids = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
    posts = Post.objects.filter(Q(user_id__in=following_ids) | Q(user=user)).order_by('-created_at')
    
    # Check follow status for search results
    for result in search_results:
        result.is_following = Follower.objects.filter(follower=user, following=result).exists()

    # Who to follow suggestions (users not followed yet, excluding self)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=user.id).order_by('?')[:3]

    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    # Get stories from following and self
    friend_ids = list(following_ids) + [user.id]
    stories = Story.objects.filter(user_id__in=friend_ids).order_by('-created_at')

    return render(request, 'index.html', {
        'current_user': user, 
        'posts': posts, 
        'stories': stories,
        'search_results': search_results,
        'search_query': search_query,
        'suggestions': suggestions,
        'unread_notifications': unread_notifications
    })

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect('index')

def notifications_view(request):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    
    # Mark as read
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    
    return render(request, 'notifications.html', {'current_user': user, 'notifications': notifications})

def delete_notification(request, notification_id):
    if 'user_id' not in request.session:
        return redirect('index')
    notification = Notification.objects.get(id=notification_id)
    if notification.user.id == request.session['user_id']:
        notification.delete()
    return redirect('notifications')

def messages_view(request, chat_user_id=None):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    
    # Get people the user has interacted with (followers/following)
    following_ids = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
    follower_ids = Follower.objects.filter(following=user).values_list('follower_id', flat=True)
    friend_ids = list(set(list(following_ids) + list(follower_ids)))
    friends = User.objects.filter(id__in=friend_ids)
    
    chat_messages = []
    active_chat_user = None
    recent_media = []
    
    if chat_user_id:
        active_chat_user = User.objects.get(id=chat_user_id)
        chat_messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=active_chat_user)) |
            (Q(sender=active_chat_user) & Q(receiver=user))
        ).order_by('created_at')
        
        # Mark as read
        Message.objects.filter(sender=active_chat_user, receiver=user, is_read=False).update(is_read=True)

        # Get recent media (images/videos shared in this chat)
        recent_media = Message.objects.filter(
            ((Q(sender=user) & Q(receiver=active_chat_user)) | (Q(sender=active_chat_user) & Q(receiver=user))),
            attachment__isnull=False
        ).exclude(attachment='').order_by('-created_at')[:6]

    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    return render(request, 'messages.html', {
        'current_user': user, 
        'friends': friends,
        'chat_messages': chat_messages,
        'active_chat_user': active_chat_user,
        'unread_notifications': unread_notifications,
        'recent_media': recent_media
    })

def send_message(request, receiver_id):
    if 'user_id' not in request.session:
        return redirect('index')
    if request.method == "POST":
        sender = User.objects.get(id=request.session['user_id'])
        receiver = User.objects.get(id=receiver_id)
        content = request.POST.get('content')
        attachment = request.FILES.get('attachment')
        if content or attachment:
            Message.objects.create(sender=sender, receiver=receiver, content=content, attachment=attachment)
            msg_content = content if content else "Sent an attachment"
            create_notification(receiver, sender, 'message', message=msg_content)
            
    return redirect('chat_with_user', chat_user_id=receiver_id)

def edit_message(request, message_id):
    if 'user_id' not in request.session:
        return redirect('index')
    message = Message.objects.get(id=message_id)
    if message.sender.id == request.session['user_id']:
        if request.method == "POST":
            content = request.POST.get('content')
            if content:
                message.content = content
                message.is_edited = True
                message.save()
    return redirect('chat_with_user', chat_user_id=message.receiver.id)

def profile_view(request, user_id=None):
    if 'user_id' not in request.session:
        return redirect('index')
    
    current_user = User.objects.get(id=request.session['user_id'])
    
    if user_id:
        viewed_user = User.objects.get(id=user_id)
    else:
        viewed_user = current_user
    
    if request.method == "POST" and viewed_user == current_user:
        # Profile update logic
        fullname = request.POST.get('fullname')
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile_picture')
        cover_img = request.FILES.get('cover_image')
        
        if fullname or bio or profile_pic or cover_img:
            if fullname:
                viewed_user.fullname = fullname
            if bio:
                viewed_user.bio = bio
            if profile_pic:
                viewed_user.profile_picture = profile_pic
            if cover_img:
                viewed_user.cover_image = cover_img
            
            viewed_user.save()
            return redirect('profile')

        # Post creation logic
        content = request.POST.get('content')
        attachment = request.FILES.get('attachment')
        feeling = request.POST.get('feeling')
        
        if content or attachment or feeling:
            Post.objects.create(
                user=viewed_user,
                content=content,
                attachment=attachment,
                feeling=feeling
            )
            return redirect('profile')
            
    user_posts = Post.objects.filter(user=viewed_user).order_by('-created_at')
    # Filter posts that have an attachment for the media section
    media_posts = user_posts.exclude(attachment='')
    
    # Who to follow suggestions
    following_ids = Follower.objects.filter(follower=current_user).values_list('following_id', flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=current_user.id).order_by('?')[:3]
    
    # Follower/Following counts
    follower_count = Follower.objects.filter(following=viewed_user).count()
    following_count = Follower.objects.filter(follower=viewed_user).count()
    is_following = Follower.objects.filter(follower=current_user, following=viewed_user).exists()
    
    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=current_user, is_read=False).count()
    
    return render(request, 'profile.html', {
        'current_user': current_user,
        'viewed_user': viewed_user,
        'posts': user_posts,
        'media_posts': media_posts,
        'suggestions': suggestions,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
        'unread_notifications': unread_notifications
    })

def stories_view(request):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    
    # Get stories from people you follow and yourself
    following_ids = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
    friend_ids = list(following_ids) + [user.id]
    
    stories = Story.objects.filter(user_id__in=friend_ids).order_by('-created_at')
    
    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    return render(request, 'stories.html', {
        'current_user': user,
        'stories': stories,
        'unread_notifications': unread_notifications
    })

def add_story(request):
    if 'user_id' not in request.session:
        return redirect('index')
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        attachment = request.FILES.get('attachment')
        if attachment:
            Story.objects.create(user=user, attachment=attachment)
            messages.success(request, "Story posted successfully!")
    return redirect('home')

def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "update_profile":
            fullname = request.POST.get('fullname')
            bio = request.POST.get('bio')
            profile_pic = request.FILES.get('profile_picture')
            cover_img = request.FILES.get('cover_image')
            
            if fullname:
                user.fullname = fullname
            if bio:
                user.bio = bio
            if profile_pic:
                user.profile_picture = profile_pic
            if cover_img:
                user.cover_image = cover_img
                
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('settings')
            
        elif action == "change_password":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if user.password == old_password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    messages.success(request, "Password changed successfully!")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Incorrect old password.")
            return redirect('settings')

    # Who to follow suggestions
    following_ids = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=user.id).order_by('?')[:3]

    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    return render(request, 'settings.html', {
        'current_user': user, 
        'suggestions': suggestions,
        'unread_notifications': unread_notifications
    })

def like_post(request, post_id):
    if 'user_id' not in request.session:
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=post_id)
    
    like_filter = Like.objects.filter(user=user, post=post)
    if like_filter.exists():
        like_filter.delete()
    else:
        Like.objects.create(user=user, post=post)
        create_notification(post.user, user, 'like', post=post)
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def follow_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('index')
    follower = User.objects.get(id=request.session['user_id'])
    following = User.objects.get(id=user_id)
    Follower.objects.get_or_create(follower=follower, following=following)
    create_notification(following, follower, 'follow')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def unfollow_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('index')
    follower = User.objects.get(id=request.session['user_id'])
    following = User.objects.get(id=user_id)
    Follower.objects.filter(follower=follower, following=following).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def add_comment(request, post_id):
    if 'user_id' not in request.session:
        return redirect('index')
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, post=post, content=content)
            create_notification(post.user, user, 'comment', post=post, message=content)
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def delete_comment(request, comment_id):
    if 'user_id' not in request.session:
        return redirect('index')
    comment = Comment.objects.get(id=comment_id)
    if comment.user.id == request.session['user_id']:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

