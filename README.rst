Django-rest
=====

Simple response serializer, automatically serizlizing all specified relations and fields, except listed in model's ``PRIVY_FIELDS = []``

Quick start
-----------

1. Installation::

    $ git clone https://github.com/maxcoredev/django-rest.git
    $ cd django-rest
    $ pip install dist/django-rest-0.1.tar.gz

2. Add "rest" to your INSTALLED_APPS setting like this:: python

    INSTALLED_APPS = [
        ...
        'rest',
    ]

3. To get pretty view in browser and make it compatible with Django-debug-toolbar add ``DebugMiddleware``:: python

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

Examples
-----------

Returns all fields, except PRIVY_FIELDS
Related objects (O2O, M2O) are just pks (default)
Related collections (O2M, M2M) are omitted::

    articles = Article.objects.all()

Same as .all(), but omitting listed fields::

    articles = Article.objects.defer('title')

Same as .all(), but only listed fields, even if they are in PRIVY_FIELDS::

    articles = Article.objects.only('title')

Add full-fledged related objects (O2O, M2O)::

    articles = Article.objects.all().select_related('category')

Add related collections (O2M, M2M) (full-fledged)::

    articles = Article.objects.all().prefetch_related('tags')
