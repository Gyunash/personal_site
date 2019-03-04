from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.forms.models import modelformset_factory
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import *
from .forms import *
import json


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, id, slug):
        post = get_object_or_404(Post, id=id, slug__iexact=slug)
        comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comment_form = CommentForm()

        return render(request, self.template, context={self.model.__name__.lower(): obj, "admin_object": obj, "detail": True, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, id, slug):
        post = get_object_or_404(Post, id=id, slug__iexact=slug)
        comments = Comment.objects.filter(post=post).order_by('-id')
        obj = get_object_or_404(self.model, slug__iexact=slug)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
                comment.save()
                #return HttpResponseRedirect(post.get_absolute_url())
                # return JsonResponse({"status": "comment_is_valid"})
        else:
            comment_form = CommentForm()

        context = {self.model.__name__.lower(): obj, 
                    "admin_object": obj, 
                    "detail": True, 
                    'comments': comments, 
                    'comment_form': comment_form}

        if request.is_ajax():
            html = render_to_string('blog/comments.html', context, request=request)
            return JsonResponse({'form': html})

        return render(request, self.template, context)

class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})



class ObjectUpdateMixin:
    model= None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})



class ObjectDeleteMixin:
    model= None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))