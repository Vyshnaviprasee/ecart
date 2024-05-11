from django import template

register = template.Library()

@register.filter(name='chunks')
def chunks(iterable, n):
    chunk = []
    i = 0
    for item in iterable:
        chunk.append(item)
        i += 1
        if i == n:
            yield chunk
            chunk = []
    yield chunk
