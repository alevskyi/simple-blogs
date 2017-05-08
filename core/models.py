from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from django.db.models.fields.files import ImageField

def validate_text(value):
    pattern = re.compile("^[\w\s\d\,\.\!\-\~\?\+\'\"\:\/]{3,}$", flags=re.UNICODE)
    if not pattern.match(value):
        raise ValidationError("Some characters in text are not allowed. Or text is too short.")
    
    return value
 
#without tabs and new lines 
def validate_theme(value):
    pattern = re.compile("^[\w \d\,\.\!\-\~\?\+\'\":]{3,60}$", flags=re.UNICODE)
    if not pattern.match(value):
        raise ValidationError("Theme contains characters which are not allowed. Or text is too short.")
    try:
        Post.objects.get(theme=value)
        raise ValidationError("Theme '%s' already exists", value)
    except ObjectDoesNotExist:
        pass
    
    return value
    
def validate_user(value):
    pattern = re.compile("^[\w\d]{3,12}$", flags=re.UNICODE)
    if not pattern.match(value):
        raise ValidationError("Username is invalid. Only letters and digits, from 3 to 12 characters")
    
    return value
    
class Post(models.Model):
    text = models.CharField(max_length = 5000, validators=[validate_text])
    theme = models.CharField(max_length = 40, validators=[validate_theme])
    date = models.DateTimeField(auto_now = True)
    image = ImageField()
    user = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return unicode(self.theme)

    
class Comment(models.Model):
    text = models.CharField(max_length = 100, validators=[validate_text])
    user = models.CharField(max_length = 20, validators=[validate_user])
    date = models.DateTimeField(auto_now = True)
    post = models.ForeignKey(Post)
    
    def __unicode__(self):
        return unicode(self.text)
    
    
