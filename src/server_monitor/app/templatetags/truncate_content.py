from django import template

register = template.Library()


@register.filter(name='truncate_content')
def truncate_content(string, number, dots='...'):
    """ 
    truncate the {string} to {number} characters
    print {dots} on the end if truncated

    usage: {{ "some text to be truncated"|trunc:6 }}
    results: some te...
    """
    if not isinstance(string, str):
        string = str(string)

    if len(string) > number:
        string = string[0:number].replace('\n', ' ') + dots

    return string
