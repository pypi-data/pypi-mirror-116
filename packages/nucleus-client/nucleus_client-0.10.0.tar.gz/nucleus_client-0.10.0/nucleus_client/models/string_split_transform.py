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


class StringSplitTransform(object):
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
        'column': 'str',
        'explode': 'bool',
        'output_column': 'str',
        'pattern': 'str'
    }

    attribute_map = {
        'column': 'column',
        'explode': 'explode',
        'output_column': 'output_column',
        'pattern': 'pattern'
    }

    def __init__(self, column=None, explode=None, output_column=None, pattern=None):  # noqa: E501
        """StringSplitTransform - a model defined in OpenAPI"""  # noqa: E501

        self._column = None
        self._explode = None
        self._output_column = None
        self._pattern = None
        self.discriminator = None

        self.column = column
        if explode is not None:
            self.explode = explode
        self.output_column = output_column
        self.pattern = pattern

    @property
    def column(self):
        """Gets the column of this StringSplitTransform.  # noqa: E501


        :return: The column of this StringSplitTransform.  # noqa: E501
        :rtype: str
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this StringSplitTransform.


        :param column: The column of this StringSplitTransform.  # noqa: E501
        :type: str
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def explode(self):
        """Gets the explode of this StringSplitTransform.  # noqa: E501


        :return: The explode of this StringSplitTransform.  # noqa: E501
        :rtype: bool
        """
        return self._explode

    @explode.setter
    def explode(self, explode):
        """Sets the explode of this StringSplitTransform.


        :param explode: The explode of this StringSplitTransform.  # noqa: E501
        :type: bool
        """

        self._explode = explode

    @property
    def output_column(self):
        """Gets the output_column of this StringSplitTransform.  # noqa: E501


        :return: The output_column of this StringSplitTransform.  # noqa: E501
        :rtype: str
        """
        return self._output_column

    @output_column.setter
    def output_column(self, output_column):
        """Sets the output_column of this StringSplitTransform.


        :param output_column: The output_column of this StringSplitTransform.  # noqa: E501
        :type: str
        """
        if output_column is None:
            raise ValueError("Invalid value for `output_column`, must not be `None`")  # noqa: E501

        self._output_column = output_column

    @property
    def pattern(self):
        """Gets the pattern of this StringSplitTransform.  # noqa: E501


        :return: The pattern of this StringSplitTransform.  # noqa: E501
        :rtype: str
        """
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        """Sets the pattern of this StringSplitTransform.


        :param pattern: The pattern of this StringSplitTransform.  # noqa: E501
        :type: str
        """
        if pattern is None:
            raise ValueError("Invalid value for `pattern`, must not be `None`")  # noqa: E501

        self._pattern = pattern

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
        if not isinstance(other, StringSplitTransform):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
