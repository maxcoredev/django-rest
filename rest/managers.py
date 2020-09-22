from django.db.models.query import QuerySet
from django.db.models.manager import Manager

from rest.helpers import merge_dicts


class RestQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None, forced=None):
        """Just QuerySet's __init__ copied with "forced" param added"""
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._forced = forced or {}

    def force(self, *fields):
        """Explicitly force add fields to queryset bypassing PRIVY_FIELDS"""

        def set_forced(string):
            splitted = string.split('__', 1)
            parent, child = splitted if len(splitted) == 2 else splitted + [{}]
            return { parent: set_forced(child) if type(child) is str else child }

        for field in fields:
            self._forced = merge_dicts(self._forced, set_forced(field))

        return self

    def only(self, *fields):
        """Force add fields to queryset bypassing PRIVY_FIELDS also while using .only()"""
        self.force(*fields)
        return super().only(*fields)

    def _set_forced(self, obj):
        """
        Universal method to be used both on the object and on the QuerySet

        For example, when single object selected after manipulations on QuerySet,
        have to set _forced to that object also, since it is not QuerySet anymore.
        That's relevant for .get(), .first(), last() methods.

        Also, there are cases, when its needed to be applied on newly created QuerySets
        Described below (._clone())

        """
        obj._forced = self._forced
        return obj

    def get(self, *args, **kwargs):
        return self._set_forced(super().get(*args, **kwargs))

    def first(self):
        return self._set_forced(super().first())

    def last(self):
        return self._set_forced(super().last())

    def _clone(self):
        """
        Since _clone() uses in lots of internal QuerySet's methods,
        it overrides queryset with new results and empty self._forced.
        To avoid that, have to explicitly set self._forced to new QuerySet via each _clone call.
        For example, now, .force() can be used before .prefetch_related() (which uses _clone())
        """
        return self._set_forced(super()._clone())


class RestManager(Manager.from_queryset(RestQuerySet)):
    pass
