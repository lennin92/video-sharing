
from django.http import HttpResponse


def category_view(request):
    return HttpResponse("""
    <h1>CATEGORY VIEW</h1>
    <p>
        User data
        %s
    </p>
    """%str(request)
    )

def video_view(request):
    return HttpResponse("""
    <h1>VIDEO VIEW</h1>
    <p>
        User data
        %s
    </p>
    """%str(request)
    )