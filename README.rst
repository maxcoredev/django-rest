Django-rest
=====

Simple response serializer.

Quick start
-----------

1. Installation::

    git clone https://github.com/maxcoredev/django-rest.git
    cd django-rest
    pip install dist/django-rest-0.1.tar.gz

2. Add "rest" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest',
    ]

3. Add "rest" middleware::

    MIDDLEWARE = [
        ...
        'rest.middleware.DebugMiddleware',
    ]

4. Define models::

    from rest.models import RestModel, models

    class Article(RestModel):
        title = models.CharField(max_length=255)
        text = models.TextField()
        views_count = models.IntegerField()
        PRIVY_FIELDS = ['views_count']

5. Use it in views::

    from rest.response import Response
    from .models import Article

    def article_list(request):
        articles = Article.objects.all()
        return Response(articles)
