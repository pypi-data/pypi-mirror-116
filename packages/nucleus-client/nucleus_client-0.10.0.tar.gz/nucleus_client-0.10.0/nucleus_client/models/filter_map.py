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


class FilterMap(object):
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
        'data_key': 'str',
        'filter_key': 'str'
    }

    attribute_map = {
        'data_key': 'data_key',
        'filter_key': 'filter_key'
    }

    def __init__(self, data_key=None, filter_key=None):  # noqa: E501
        """FilterMap - a model defined in OpenAPI"""  # noqa: E501

        self._data_key = None
        self._filter_key = None
        self.discriminator = None

        if data_key is not None:
            self.data_key = data_key
        self.filter_key = filter_key

    @property
    def data_key(self):
        """Gets the data_key of this FilterMap.  # noqa: E501


        :return: The data_key of this FilterMap.  # noqa: E501
        :rtype: str
        """
        return self._data_key

    @data_key.setter
    def data_key(self, data_key):
        """Sets the data_key of this FilterMap.


        :param data_key: The data_key of this FilterMap.  # noqa: E501
        :type: str
        """

        self._data_key = data_key

    @property
    def filter_key(self):
        """Gets the filter_key of this FilterMap.  # noqa: E501


        :return: The filter_key of this FilterMap.  # noqa: E501
        :rtype: str
        """
        return self._filter_key

    @filter_key.setter
    def filter_key(self, filter_key):
        """Sets the filter_key of this FilterMap.


        :param filter_key: The filter_key of this FilterMap.  # noqa: E501
        :type: str
        """
        if filter_key is None:
            raise ValueError("Invalid value for `filter_key`, must not be `None`")  # noqa: E501

        self._filter_key = filter_key

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
        if not isinstance(other, FilterMap):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
