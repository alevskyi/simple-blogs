import re
from urlparse import urlparse, urlunparse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponseRedirect

class ReturningRedirect(Exception):
    def __init__(self, redirect):
        self.redirect = redirect
        
    def __str__(self):
        return 'break_on_pages returning redirect instead of context'
 
    
def break_on_pages(posts, request):
    '''
    Return context of posts divided on pages and urls to pages. Raises ReturningRedirect exception if url is invalid
    '''
    paginator = Paginator(posts, 2)
    
    page = request.GET.get('page')
    
    url = request.get_full_path()
            
    if not page:
        #page should always be present in url
        raise ReturningRedirect(HttpResponseRedirect(add_page(url, 1)))
    
    else:
        page = int(page)
            
    try:
        posts = paginator.page(page)
        
    except PageNotAnInteger:
        
        raise ReturningRedirect(HttpResponseRedirect(replace_page(url, 1)))
    
    except EmptyPage:
                
        if(page > paginator.num_pages):
            raise ReturningRedirect(HttpResponseRedirect(replace_page(url, paginator.num_pages)))
        
        else:
            raise ReturningRedirect(HttpResponseRedirect(replace_page(url, 1)))
        
    first_page_url = replace_page(url, 1)
    last_page_url = replace_page(url, paginator.num_pages)
    
    if posts.has_previous():
        previous_page_url = replace_page(url, posts.number - 1)
    else:
        previous_page_url = ''
    
    if posts.has_next():
        next_page_url = replace_page(url, posts.number + 1)
    else:
        next_page_url = ''
                       
    context = {'posts': posts, 'first_page_url' : first_page_url, 'last_page_url' : last_page_url,
            'previous_page_url' : previous_page_url, 'next_page_url' : next_page_url}
    
    return context


def replace_page(url, page_nmbr):
    '''
    Replaces url parameter 'page=any_string' by 'page=page_nmbr'. Throws Exception if substring 'page=' not in url.
    '''
    regex = re.compile('.+[&?](page=[^&]*)')
    match = regex.search(url)
        
    if not match:
        raise Exception("replace_page match fail")
    else:
        start = match.start(1)
        end = match.end(1)
           
        return url[:start] + 'page=' + str(page_nmbr) + url[end:]
    


def add_page(url, page_nmbr):
    '''
    Adds 'page=page_nmbr' to url, with regard to '?' and '&' delimiters and empty page parameter: 'page=' 
    '''
    components = urlparse(url)
    scheme, netloc, path, params, query, fragment = [c for c in components]
    
    if query:
        #Check if query contains empty key 'page'
        if 'page=' in query:
            page_string = ''
        else:
            page_string = '&page='
    else:
        page_string = 'page='
        
    new_query = query + page_string + str(page_nmbr)
    return urlunparse( (scheme, netloc, path, params, new_query, fragment) )


def sort(posts, sort_type):
    '''
    Sorts query set by 'sort_type', accepted values: 'date', 'comments', 'nosort'
    '''
    if sort_type == 'date':
        #From new to old, - sign is reverse order
        return posts.order_by('-date')
    
    elif sort_type == 'comments':
        #From most commented to less, reverse=True
        posts_list = list(posts)
        return sorted(posts_list, key=sort_by_comments, reverse=True)
    
    elif sort_type == 'nosort':
        return posts
    
    else:
        raise Exception('Invalid sort type \'%s\', accepted values are:  date, comments, nosort' % sort_type)
    

def sort_by_comments(post):
    return post.comment_set.count()
    
