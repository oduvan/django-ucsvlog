
def userid(request):
    return (request.user.id or '0')

def language_code(request):
    from django.utils import translation
    return ranslation.get_language()

def language_bidi(request):
    from django.utils import translation
    return translation.get_language_bidi()