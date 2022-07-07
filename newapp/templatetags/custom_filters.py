from django import template

register = template.Library()

@register.filter()
def censor(text):
    Cens_word = ["Редиска"]
    low = text.lower()
    for i in Cens_word:
        if i.find(low):
            low = text.replace(i[1:], "*" * (len(i) -1))
    return f'{low}'
