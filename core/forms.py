from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from core.models import Post, Comment
from django.forms.widgets import Textarea, TextInput
from django.forms.fields import ImageField, CharField


class PostForm(ModelForm):
    
    image = ImageField(required=False)
    user = CharField(required=False) 
    
    class Meta:
        model = Post
        fields = ('theme', 'text', 'image')
        exclude = ('user',)
        widgets = {
            'theme': TextInput(attrs={'size': '70'}),
            'text': Textarea(attrs={'style':'width:700px;height:400px;resize:none;'}),
        }
        
class CommentForm(ModelForm):
           
    class Meta:
        model = Comment
        fields = ('user', 'text')
        exclude = ('post',)
        widgets = {
            'user': TextInput(attrs={'size': '20'}),
            'text': Textarea(attrs={'style':'width:700px;height:80px;resize:none;'}),
        }
       
        
class RegistrationForm(FormView):
    
    form_class = UserCreationForm 
        
    success_url = '/login'
 
    template_name = 'core/register.html'
    
    def form_valid(self, form):
        
        form.save()
      
        return super(RegistrationForm, self).form_valid(form)


class LoginForm(FormView):
    form_class = AuthenticationForm
    
    success_url = '/profile'
    
    template_name = 'core/login.html'

    def form_valid(self, form):
        
        self.user = form.get_user()
        
        login(self.request, self.user)
        
        return super(LoginForm, self).form_valid(form)
    
