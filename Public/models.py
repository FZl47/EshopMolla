from django.db import models
from ckeditor.fields import RichTextField
from Config.Tools import RandomString

class SiteInfo(models.Model):
    our_mission = RichTextField()
    our_vision = RichTextField()
    who_we_are = RichTextField()
    contact_information = RichTextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address_office = models.CharField(max_length=500)
    token_blog = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return 'Eshop Molla'


def upload_src_image_out_stor(instance,path):
    frmt = str(path).split('.')[-1]
    return f"contactUs/outStor/{RandomString()}.{frmt}"

class OutStor(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    store_hour = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to=upload_src_image_out_stor)

    def __str__(self):return self.title


class CommentSupport(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    is_checked = models.BooleanField(default=False)
    dateTimeSubmit = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.subject[:30]}..."



class FaqCategory(models.Model):
    title = models.CharField(max_length=100)

    def getFaqs(self):
        return self.faq_set.all().filter(show=True)

    def __str__(self):
        return self.title

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    show = models.BooleanField()
    category = models.ForeignKey('Public.FaqCategory',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question[:20]}..."


