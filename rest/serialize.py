from collections import Iterable

from rest.models import RestModel
from rest.managers import RestQuerySet
from rest.helpers import merge_dicts


def serialize_object(obj, parent=None, forced=None):

    return_obj = {}

    forced = forced or {}

    # 1. Iterate over regular fields

    for field, value in obj.__dict__.items():

        # Do not serialize field if starts with "_" (even django model has _state object for example) OR
        # manually excluded by QuerySet's .defer() method OR
        # specified in Model's PRIVY_FIELDS

        if field not in forced.keys() and (
           field.startswith('_') or
           field in obj.get_deferred_fields() or
           field in getattr(obj, 'PRIVY_FIELDS', [])
        ):
            continue

        return_obj[field] = serialize(value)

    # 2. Iterate over .select_related() objects

    for field, related in obj._state.fields_cache.items():

        # Since fields_cache contains object not only when .select_related() used,
        # but also all children populated with parent when .prefetch_related() used -> skip that second case

        if parent and parent is related:
            pass
        else:
            child_forced = forced.get(field, None)
            return_obj[field] = serialize(related, parent=obj, forced=child_forced)

    # 3. Iterate over .prefetch_related() objects

    for field, objects in getattr(obj, '_prefetched_objects_cache', {}).items():
        child_forced = forced.get(field, None)
        return_obj[field] = serialize(objects, parent=obj, forced=child_forced)

    return return_obj


def serialize(content, parent=None, forced=None):

    # If iterable (including RestQuerySet) (but not str)
    if isinstance(content, Iterable) and not isinstance(content, (str, bytes, dict)):
        array = []
        for obj in content:
            forced = merge_dicts(forced, content._forced if isinstance(content, RestQuerySet) else None)
            array.append(serialize(obj, parent=parent, forced=forced))
        return array

    # If RestModel itself
    elif isinstance(content, RestModel):
        return serialize_object(content, parent=parent, forced=merge_dicts(forced, content._forced))

    # If some sort of dict (dict or object, including base models.Model)
    elif isinstance(content, dict) or hasattr(content, '__dict__'):
        content = content if isinstance(content, dict) else content.__dict__
        obj = {}
        for field, value in content.items():
            if not field.startswith('_'):
                obj[field] = serialize(value)
        return obj

    # Primitive
    else:
        return content