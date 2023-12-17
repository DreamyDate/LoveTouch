from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from django.template.loader import render_to_string


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('news/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                                total_comments=Count('comments')
                                ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def render_header():
    return render_to_string('pages/header.html')

@register.simple_tag
def render_footer():
    return render_to_string('pages/footer.html')
