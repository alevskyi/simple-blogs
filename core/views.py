from django.http import HttpResponseRedirect
from core.models import Post, Comment
from django.shortcuts import render, get_object_or_404

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from cryptography.exceptions import InvalidKey
from datetime import datetime

from core.helpers import break_on_pages, ReturningRedirect, sort
from django.contrib.auth.decorators import login_required
from core.forms import PostForm, CommentForm
from django.contrib.auth.models import User


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('core:main'))

@login_required    
def profile_redirect(request):
    return HttpResponseRedirect(reverse('core:profile', kwargs={'username': request.user.username}))
    
@login_required    
def profile(request, username):
    
    user = get_object_or_404(User, username=username)
    
    posts = Post.objects.filter(user=username) 
    
    if request.method == 'GET' and request.user.username == username:
        try:
           
            context = break_on_pages(posts, request)
               
        except ReturningRedirect, e:
            return e.redirect

        form = PostForm()
        context.update({'form':form})

        return render(request, 'core/profile.html', context)
   
 
@login_required    
def new_redirect(request):
    return HttpResponseRedirect(reverse('core:new_post', kwargs={'username': request.user.username}))
 
 
@login_required 
def new_post(request, username):
      
    if request.method == 'GET' and request.user.username == username:
        
        form = PostForm()
        context = {'form':form}
        return render(request, 'core/new.html', context)
    
    elif request.method == 'POST' and request.user.username == username:
       
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = username
            post.save()      
            return HttpResponseRedirect(reverse('core:profile', kwargs={'username': request.user.username}))
        
        else:
            context = {'form' : form}
            return render(request, 'core/new.html', context)


def search(request):
    
    if request.method == 'POST':                
        query_value = str(request.POST.get('query'))
        
        if not query_value:
            return HttpResponseRedirect(reverse('core:main'))
            
        match_value = str(request.POST.get('match'))
        from_value = str(request.POST.get('date_from'))
        to_value = str(request.POST.get('date_to'))
        sort_value = str(request.POST.get('sort'))
        
        param_tupple = (query_value, match_value, from_value, to_value, sort_value) 
        
        url = reverse('core:search') + '?query=%s&match=%s&date_from=%s&date_to=%s&sort=%s' % param_tupple
        
        return HttpResponseRedirect(url)
    
    elif request.method == 'GET':
        
        query_value = unicode(request.GET.get('query'))
        
        if not query_value:
            return HttpResponseRedirect(reverse('core:main'))
        
        match_value = unicode(request.GET.get('match'))
        from_value = unicode(request.GET.get('date_from'))
        to_value = unicode(request.GET.get('date_to'))
        sort_value = unicode(request.GET.get('sort'))
        
        if(match_value == 'theme'):
            posts = Post.objects.filter(theme__regex=query_value)
        
        elif(match_value == 'text'):
            posts = Post.objects.filter(text__regex=query_value)
    
        elif(match_value == 'user'):
            posts = Post.objects.filter(user__regex=query_value)
    
        else:
            raise InvalidKey(unicode('invalid parameter ') + match_value)
        
        if from_value:
            from_date = datetime.strptime(from_value, '%d.%m.%Y')
            posts = posts.filter(date__gte=from_date)
    
        if to_value:
            to_date = datetime.strptime(to_value, '%d.%m.%Y')
            posts = posts.filter(date__lte=to_date)
                  
        sorted_posts = sort(posts, sort_value)
        
        try:
                 
            context = break_on_pages(sorted_posts, request)            
            return render(request, 'core/main.html', context)
        
        except ReturningRedirect, e:
            return e.redirect    
    

def main(request):
    
    posts = Post.objects.all()
    try:
        context = break_on_pages(posts, request)
        return render(request, 'core/main.html', context)
       
    except ReturningRedirect, e:
        return e.redirect   
    
       
def detailed(request, post_id): 
    
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all()
    form = CommentForm()
    
    context = {'post' : post, 'form' : form, 'comments' : comments}
    
    if request.method == 'GET':                          
            
        return render(request, 'core/detailed.html', context)
    
    else:
                
        form = CommentForm(request.POST)      
        
        if form.is_valid():
  
            comment = form.save(commit=False)
    
            post = Post.objects.get(id=post_id)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('core:detailed', kwargs={'post_id': post_id}))
        
        else:
            context.update({'form' : form})  
            return render(request, 'core/detailed.html', context) 
            
    
