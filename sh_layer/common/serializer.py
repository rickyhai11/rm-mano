import six

from oslo_messaging import Serializer

ATTR_NOT_SPECIFIED = object()


class Mapping(object):
    def __init__(self, mapping):
        self.direct_mapping = mapping
        self.reverse_mapping = {}
        for key, value in six.iteritems(mapping):
            self.reverse_mapping[value] = key

_SINGLETON_MAPPING = Mapping({
    ATTR_NOT_SPECIFIED: "@@**ATTR_NOT_SPECIFIED**@@",
})


class Playnetmano_rmSerializer(Serializer):
    def __init__(self, base=None):
        super(Playnetmano_rmSerializer, self).__init__()
        self._base = base

    def serialize_entity(self, context, entity):
        if isinstance(entity, dict):
            for key, value in six.iteritems(entity):
                entity[key] = self.serialize_entity(context, value)

        elif isinstance(entity, list):
            for i, item in enumerate(entity):
                entity[i] = self.serialize_entity(context, item)

        elif entity in _SINGLETON_MAPPING.direct_mapping:
            entity = _SINGLETON_MAPPING.direct_mapping[entity]

        if self._base is not None:
            entity = self._base.serialize_entity(context, entity)

        return entity

    def deserialize_entity(self, context, entity):
        if isinstance(entity, dict):
            for key, value in six.iteritems(entity):
                entity[key] = self.deserialize_entity(context, value)

        elif isinstance(entity, list):
            for i, item in enumerate(entity):
                entity[i] = self.deserialize_entity(context, item)

        elif entity in _SINGLETON_MAPPING.reverse_mapping:
            entity = _SINGLETON_MAPPING.reverse_mapping[entity]

        if self._base is not None:
            entity = self._base.deserialize_entity(context, entity)

        return entity

    def serialize_context(self, context):
        if self._base is not None:
            context = self._base.serialize_context(context)

        return context

    def deserialize_context(self, context):
        if self._base is not None:
            context = self._base.deserialize_context(context)

        return context
