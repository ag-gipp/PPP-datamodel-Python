"""Contains operators that work on lists."""

from .abstractnode import register, AbstractNode
from .list import List

def to_abstract_node(x):
    return x if isinstance(x, AbstractNode) else AbstractNode.from_dict(x)

class ListOperator(AbstractNode):
    """Base class for list operators.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#union-intersection-and-or-first-and-last
    """
    __slots__ = ()
    _possible_attributes = ('list',)

    def _check_attributes(self, attributes):
        super(ListOperator, self)._check_attributes(attributes)
        if not isinstance(attributes['list'], list):
            raise TypeError('The “list” argument of the %s constructor '
                            'should be a list, not %r' %
                            (self.__class__.__name__, attributes['list']))

    def _parse_attributes(self, attributes):
        L = attributes['list']
        assert hasattr(L, '__iter__') and not isinstance(L, AbstractNode)
        if all(isinstance(x, dict) for x in L):
            L = [{'type': 'list', 'list': [x]} if x['type'] != 'list' else x
                 for x in L]
        else:
            assert not any(isinstance(x, dict) for x in L)
        L = tuple(to_abstract_node(l) for l in L)
        attributes['list'] = L
        super(ListOperator, self)._parse_attributes(attributes)

    def as_dict(self):
        return {'type': self.type, 'list': [x.as_dict() for x in self.list]}

class PredicateListOperator(ListOperator):
    __slots__ = ()
    _possible_attributes = ('list', 'predicate')

    def as_dict(self):
        d = super().as_dict()
        d['predicate'] = self.predicate.as_dict()
        return d



@register
class Union(ListOperator):
    __slots__ = ()
    _type = 'union'
@register
class Intersection(ListOperator):
    __slots__ = ()
    _type = 'intersection'
@register
class And(ListOperator):
    __slots__ = ()
    _type = 'and'
@register
class Or(ListOperator):
    __slots__ = ()
    _type = 'or'
@register
class First(ListOperator):
    __slots__ = ()
    _type = 'first'
@register
class Last(ListOperator):
    __slots__ = ()
    _type = 'last'

@register
class Sort(PredicateListOperator):
    __slots__ = ()
    _type = 'sort'