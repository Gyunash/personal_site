from django import template

register = template.Library()

@register.inclusion_tag('chat.html')
def render_message(message):
    context_for_rendering_inclusion_tag = {'message': message}
    return context_for_rendering_inclusion_tag