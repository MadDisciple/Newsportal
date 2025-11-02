import re
from django import template

register = template.Library()

BAD_WORDS = [
    'редиска',
    'нехороший',
    'дурак',
    'идиот',
    'болван',
    'глупец',
    'мерзавец',
    'негодяй',
    'подлец',
    'зараза',
    'сволочь',
    'урод',
    'гад',
    'дрянь'
]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError(f"Фильтр 'censor' применяется только к строкам, а не к {type(value)}")

    pattern = r'\b(' + '|'.join(BAD_WORDS) + r')\b'

    def replace_match(match):
        word = match.group(0)
        return word[0] + '*' * (len(word) - 1)

    censored_value = re.sub(pattern, replace_match, value, flags=re.IGNORECASE)

    return censored_value

@register.filter(name='addclass')
def addclass(field, css_class):
    if hasattr(field, 'field') and hasattr(field.field, 'widget'):
        if field.field.widget.__class__.__name__ == 'HiddenInput':
            return field
        return field.as_widget(attrs={'class': css_class})
    return field