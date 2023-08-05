# coding: utf-8

"""
    Nucleus API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Transform(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'array': 'ArrayTransform',
        'bool': 'BooleanTransform',
        'boolean': 'BooleanTransform',
        'coalesce': 'CoalesceTransform',
        'datetime': 'DatetimeTransform',
        'drop': 'DropTransform',
        'dt': 'DatetimeTransform',
        'map': 'MapTransform',
        'num': 'NumberTransform',
        'number': 'NumberTransform',
        'rename': 'RenameTransform',
        'rename2': 'RenameTransform2',
        'str': 'StringTransform',
        'string': 'StringTransform'
    }

    attribute_map = {
        'array': 'array',
        'bool': 'bool',
        'boolean': 'boolean',
        'coalesce': 'coalesce',
        'datetime': 'datetime',
        'drop': 'drop',
        'dt': 'dt',
        'map': 'map',
        'num': 'num',
        'number': 'number',
        'rename': 'rename',
        'rename2': 'rename2',
        'str': 'str',
        'string': 'string'
    }

    def __init__(self, array=None, bool=None, boolean=None, coalesce=None, datetime=None, drop=None, dt=None, map=None, num=None, number=None, rename=None, rename2=None, str=None, string=None):  # noqa: E501
        """Transform - a model defined in OpenAPI"""  # noqa: E501

        self._array = None
        self._bool = None
        self._boolean = None
        self._coalesce = None
        self._datetime = None
        self._drop = None
        self._dt = None
        self._map = None
        self._num = None
        self._number = None
        self._rename = None
        self._rename2 = None
        self._str = None
        self._string = None
        self.discriminator = None

        if array is not None:
            self.array = array
        if bool is not None:
            self.bool = bool
        if boolean is not None:
            self.boolean = boolean
        if coalesce is not None:
            self.coalesce = coalesce
        if datetime is not None:
            self.datetime = datetime
        if drop is not None:
            self.drop = drop
        if dt is not None:
            self.dt = dt
        if map is not None:
            self.map = map
        if num is not None:
            self.num = num
        if number is not None:
            self.number = number
        if rename is not None:
            self.rename = rename
        if rename2 is not None:
            self.rename2 = rename2
        if str is not None:
            self.str = str
        if string is not None:
            self.string = string

    @property
    def array(self):
        """Gets the array of this Transform.  # noqa: E501


        :return: The array of this Transform.  # noqa: E501
        :rtype: ArrayTransform
        """
        return self._array

    @array.setter
    def array(self, array):
        """Sets the array of this Transform.


        :param array: The array of this Transform.  # noqa: E501
        :type: ArrayTransform
        """

        self._array = array

    @property
    def bool(self):
        """Gets the bool of this Transform.  # noqa: E501


        :return: The bool of this Transform.  # noqa: E501
        :rtype: BooleanTransform
        """
        return self._bool

    @bool.setter
    def bool(self, bool):
        """Sets the bool of this Transform.


        :param bool: The bool of this Transform.  # noqa: E501
        :type: BooleanTransform
        """

        self._bool = bool

    @property
    def boolean(self):
        """Gets the boolean of this Transform.  # noqa: E501


        :return: The boolean of this Transform.  # noqa: E501
        :rtype: BooleanTransform
        """
        return self._boolean

    @boolean.setter
    def boolean(self, boolean):
        """Sets the boolean of this Transform.


        :param boolean: The boolean of this Transform.  # noqa: E501
        :type: BooleanTransform
        """

        self._boolean = boolean

    @property
    def coalesce(self):
        """Gets the coalesce of this Transform.  # noqa: E501


        :return: The coalesce of this Transform.  # noqa: E501
        :rtype: CoalesceTransform
        """
        return self._coalesce

    @coalesce.setter
    def coalesce(self, coalesce):
        """Sets the coalesce of this Transform.


        :param coalesce: The coalesce of this Transform.  # noqa: E501
        :type: CoalesceTransform
        """

        self._coalesce = coalesce

    @property
    def datetime(self):
        """Gets the datetime of this Transform.  # noqa: E501


        :return: The datetime of this Transform.  # noqa: E501
        :rtype: DatetimeTransform
        """
        return self._datetime

    @datetime.setter
    def datetime(self, datetime):
        """Sets the datetime of this Transform.


        :param datetime: The datetime of this Transform.  # noqa: E501
        :type: DatetimeTransform
        """

        self._datetime = datetime

    @property
    def drop(self):
        """Gets the drop of this Transform.  # noqa: E501


        :return: The drop of this Transform.  # noqa: E501
        :rtype: DropTransform
        """
        return self._drop

    @drop.setter
    def drop(self, drop):
        """Sets the drop of this Transform.


        :param drop: The drop of this Transform.  # noqa: E501
        :type: DropTransform
        """

        self._drop = drop

    @property
    def dt(self):
        """Gets the dt of this Transform.  # noqa: E501


        :return: The dt of this Transform.  # noqa: E501
        :rtype: DatetimeTransform
        """
        return self._dt

    @dt.setter
    def dt(self, dt):
        """Sets the dt of this Transform.


        :param dt: The dt of this Transform.  # noqa: E501
        :type: DatetimeTransform
        """

        self._dt = dt

    @property
    def map(self):
        """Gets the map of this Transform.  # noqa: E501


        :return: The map of this Transform.  # noqa: E501
        :rtype: MapTransform
        """
        return self._map

    @map.setter
    def map(self, map):
        """Sets the map of this Transform.


        :param map: The map of this Transform.  # noqa: E501
        :type: MapTransform
        """

        self._map = map

    @property
    def num(self):
        """Gets the num of this Transform.  # noqa: E501


        :return: The num of this Transform.  # noqa: E501
        :rtype: NumberTransform
        """
        return self._num

    @num.setter
    def num(self, num):
        """Sets the num of this Transform.


        :param num: The num of this Transform.  # noqa: E501
        :type: NumberTransform
        """

        self._num = num

    @property
    def number(self):
        """Gets the number of this Transform.  # noqa: E501


        :return: The number of this Transform.  # noqa: E501
        :rtype: NumberTransform
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this Transform.


        :param number: The number of this Transform.  # noqa: E501
        :type: NumberTransform
        """

        self._number = number

    @property
    def rename(self):
        """Gets the rename of this Transform.  # noqa: E501


        :return: The rename of this Transform.  # noqa: E501
        :rtype: RenameTransform
        """
        return self._rename

    @rename.setter
    def rename(self, rename):
        """Sets the rename of this Transform.


        :param rename: The rename of this Transform.  # noqa: E501
        :type: RenameTransform
        """

        self._rename = rename

    @property
    def rename2(self):
        """Gets the rename2 of this Transform.  # noqa: E501


        :return: The rename2 of this Transform.  # noqa: E501
        :rtype: RenameTransform2
        """
        return self._rename2

    @rename2.setter
    def rename2(self, rename2):
        """Sets the rename2 of this Transform.


        :param rename2: The rename2 of this Transform.  # noqa: E501
        :type: RenameTransform2
        """

        self._rename2 = rename2

    @property
    def str(self):
        """Gets the str of this Transform.  # noqa: E501


        :return: The str of this Transform.  # noqa: E501
        :rtype: StringTransform
        """
        return self._str

    @str.setter
    def str(self, str):
        """Sets the str of this Transform.


        :param str: The str of this Transform.  # noqa: E501
        :type: StringTransform
        """

        self._str = str

    @property
    def string(self):
        """Gets the string of this Transform.  # noqa: E501


        :return: The string of this Transform.  # noqa: E501
        :rtype: StringTransform
        """
        return self._string

    @string.setter
    def string(self, string):
        """Sets the string of this Transform.


        :param string: The string of this Transform.  # noqa: E501
        :type: StringTransform
        """

        self._string = string

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Transform):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
