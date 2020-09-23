Django-rest
=====

Simple response serializer, automatically serizlizing all specified relations and fields, except listed in model's ``PRIVY_FIELDS = []``

Quick start
-----------

1. Installation:

.. code-block:: bash

    $ git clone https://github.com/maxcoredev/django-rest.git
    $ cd django-rest
    $ pip install dist/django-rest-0.1.tar.gz

2. Define models:

.. code-block:: python

    from rest.models import RestModel, models

    class Article(RestModel):
        title = models.CharField(max_length=255)
        text = models.TextField()
        views_count = models.IntegerField()

        # Feilds that must not be serialized if not forced with objects.only() and objects.force()
        PRIVY_FIELDS = ['views_count']

3. Use it in views:

.. code-block:: python

    from rest.response import Response
    from .models import Article

    def article_list(request):
        articles = Article.objects.all()
        return Response(articles)


4. To get pretty view in browser and make it compatible with Django-debug-toolbar add ``DebugMiddleware``:

.. code-block:: python

    MIDDLEWARE = [
        ...
        'rest.middleware.DebugMiddleware',
    ]

Examples
-----------

Return all fields, except ``PRIVY_FIELDS``

Related objects (O2O, M2O) are just pks (default)

Related collections (O2M, M2M) are omitted:

.. code-block:: python

    articles = Article.objects.all()

-----------

Omitting fields:

.. code-block:: python

    articles = Article.objects.defer('title')

-----------

Only listed fields, even if they are in ``PRIVY_FIELDS``:

.. code-block:: python

    articles = Article.objects.only('title')

-----------

The only non-standard method - force add ``PRIVY_FIELDS`` to be serialized:

.. code-block:: python

    articles = Article.objects.force('views_count')

-----------

Add full-fledged related objects (O2O, M2O):

.. code-block:: python

    articles = Article.objects.all().select_related('category')

-----------

Add related collections (O2M, M2M) (full-fledged):

.. code-block:: python

    articles = Article.objects.all().prefetch_related('tags')
