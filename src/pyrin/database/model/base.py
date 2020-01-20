# -*- coding: utf-8 -*-
"""
model base module.
"""

import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

import pyrin.database.services as database_services
import pyrin.database.sequence.services as sequence_services

from pyrin.core.context import CoreObject, DTO
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.model.exceptions import SequenceHasNotSetError, ColumnNotExistedError


class CoreDeclarative(CoreObject):
    """
    core declarative class.
    it will be used to create a declarative base for all models.
    """

    # holds the table name in database.
    __tablename__ = None

    # holds the extra arguments for table.
    # for example:
    # __table_args__ = {'schema': 'database_name.schema_name',
    #                   'extend_existing': True}
    __table_args__ = None

    # holds the name of the sequence used for table's primary key column.
    __sequence_name__ = None

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreDeclarative.
        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        :raises ColumnNotExistedError: column not existed error.
        """

        CoreObject.__init__(self)

        self._set_name(self.__class__.__name__)
        self.from_dict(False, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self._get_root_base_class()):
            return self.primary_key() == other.primary_key()

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('{base_type}{pk}'.format(base_type=self._get_root_base_class(),
                                             pk=self.primary_key()))

    def __repr__(self):
        return '<{module}.{class_} [{pk}]>'.format(module=self.__module__,
                                                   class_=self.__class__.__name__,
                                                   pk=str(self.primary_key()))

    def __str__(self):
        return str(self.primary_key())

    def _get_root_base_class(self):
        """
        gets root base class of this entity and caches it.
        root base class is the class which is direct subclass
        of CoreEntity in inheritance hierarchy.
        for example: {Base -> CoreEntity, A -> Base, B -> A}
        root base class of A, B and Base is Base class.

        :rtype: CoreEntity
        """

        if getattr(self, '_root_base_class', None) is None:
            bases = inspect.getmro(type(self))
            base_entity_index = bases.index(CoreEntity) - 1
            self.__class__._root_base_class = bases[base_entity_index]

        return self.__class__._root_base_class

    def _set_all_columns(self, columns):
        """
        sets all column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_all_columns', None) is None:
            self.__class__._all_columns = DTO()

        self.__class__._all_columns[type(self)] = columns

    def _set_exposed_columns(self, columns):
        """
        sets exposed column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_exposed_columns', None) is None:
            self.__class__._exposed_columns = DTO()

        self.__class__._exposed_columns[type(self)] = columns

    def save(self):
        """
        saves the current entity.
        """

        database_services.get_current_store().add(self)
        return self

    def update(self, **kwargs):
        """
        updates the current entity with given values.
        """

        self.from_dict(**kwargs)
        return self.save()

    def delete(self):
        """
        deletes the current entity.
        """

        database_services.get_current_store().delete(self)

    def next_sequence_value(self):
        """
        gets the next sequence value of this entity
        using `__sequence_name__` value.

        :raises SequenceHasNotSetError: sequence has not set error.

        :rtype: int
        """

        if self.__sequence_name__ in (None, ''):
            raise SequenceHasNotSetError('No primary key sequence has been set '
                                         'for entity [{name}].'
                                         .format(name=self.get_name()))

        return sequence_services.get_next_value(self.__sequence_name__)

    def primary_key(self):
        """
        gets the primary key value of this table.

        note that the returning value of this method will be used
        as a way to compare two different entities of the same type.
        so if your table does not have a primary key, you could either
        not implement this method and do not compare instances of this type
        or you could implement another logic in this method to make comparisons
        possible and correct. the returning value of this method must be hashable.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    def all_columns(self):
        """
        gets all column names of entity.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = self._get_all_columns()
        if columns is None:
            all_columns = tuple(prop.key for prop in class_mapper(type(self)).iterate_properties
                                if isinstance(prop, ColumnProperty))
            self._set_all_columns(all_columns)

        return self._get_all_columns()

    def exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `exposed=True`.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = self._get_exposed_columns()
        if columns is None:
            exposed_columns = tuple(prop.key for prop in class_mapper(type(self)).
                                    iterate_properties if isinstance(prop, ColumnProperty)
                                    and prop.columns[0].exposed is True)
            self._set_exposed_columns(exposed_columns)

        return self._get_exposed_columns()

    def _get_all_columns(self):
        """
        gets all column names of entity.
        returns None if not found.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = getattr(self, '_all_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `exposed=True`.
        returns None if not found.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = getattr(self, '_exposed_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def to_dict(self):
        """
        converts the entity into a dict and returns it.
        the result dict only contains the exposed columns of
        the entity which are those that their `exposed` attribute
        is set to True.

        :rtype: dict
        """

        result = DTO()
        for col in self.exposed_columns():
            result[col] = getattr(self, col)

        return result

    def from_dict(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of the entity from those
        values that are available in input keyword arguments.

        :keyword bool silent_on_invalid_column: specifies that if a key is not available
                                                in entity columns, do not raise an error.
                                                defaults to True if not provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        all_columns = self.all_columns()
        for key, value in kwargs.items():
            if key in all_columns:
                setattr(self, key, value)
            else:
                if silent_on_invalid_column is False:
                    raise ColumnNotExistedError('Entity [{entity}] does not have '
                                                'a column named [{column}].'
                                                .format(entity=self.get_name(),
                                                        column=key))

    @classmethod
    def table_name(cls):
        """
        gets the table name that this entity represents in database.

        :rtype: str
        """

        return cls.__tablename__


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative, name='CoreEntity', constructor=None)
