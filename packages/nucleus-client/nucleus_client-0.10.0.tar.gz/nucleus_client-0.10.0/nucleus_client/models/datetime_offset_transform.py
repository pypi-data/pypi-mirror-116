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


class DatetimeOffsetTransform(object):
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
        'column2': 'str',
        'granularity': 'str',
        'operator': 'str',
        'output_column': 'str',
        'value': 'float'
    }

    attribute_map = {
        'column': 'column',
        'column2': 'column2',
        'granularity': 'granularity',
        'operator': 'operator',
        'output_column': 'output_column',
        'value': 'value'
    }

    def __init__(self, column=None, column2=None, granularity=None, operator=None, output_column=None, value=None):  # noqa: E501
        """DatetimeOffsetTransform - a model defined in OpenAPI"""  # noqa: E501

        self._column = None
        self._column2 = None
        self._granularity = None
        self._operator = None
        self._output_column = None
        self._value = None
        self.discriminator = None

        self.column = column
        if column2 is not None:
            self.column2 = column2
        self.granularity = granularity
        self.operator = operator
        self.output_column = output_column
        if value is not None:
            self.value = value

    @property
    def column(self):
        """Gets the column of this DatetimeOffsetTransform.  # noqa: E501


        :return: The column of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: str
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this DatetimeOffsetTransform.


        :param column: The column of this DatetimeOffsetTransform.  # noqa: E501
        :type: str
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def column2(self):
        """Gets the column2 of this DatetimeOffsetTransform.  # noqa: E501


        :return: The column2 of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: str
        """
        return self._column2

    @column2.setter
    def column2(self, column2):
        """Sets the column2 of this DatetimeOffsetTransform.


        :param column2: The column2 of this DatetimeOffsetTransform.  # noqa: E501
        :type: str
        """

        self._column2 = column2

    @property
    def granularity(self):
        """Gets the granularity of this DatetimeOffsetTransform.  # noqa: E501


        :return: The granularity of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: str
        """
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """Sets the granularity of this DatetimeOffsetTransform.


        :param granularity: The granularity of this DatetimeOffsetTransform.  # noqa: E501
        :type: str
        """
        if granularity is None:
            raise ValueError("Invalid value for `granularity`, must not be `None`")  # noqa: E501

        self._granularity = granularity

    @property
    def operator(self):
        """Gets the operator of this DatetimeOffsetTransform.  # noqa: E501


        :return: The operator of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """Sets the operator of this DatetimeOffsetTransform.


        :param operator: The operator of this DatetimeOffsetTransform.  # noqa: E501
        :type: str
        """
        if operator is None:
            raise ValueError("Invalid value for `operator`, must not be `None`")  # noqa: E501

        self._operator = operator

    @property
    def output_column(self):
        """Gets the output_column of this DatetimeOffsetTransform.  # noqa: E501


        :return: The output_column of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: str
        """
        return self._output_column

    @output_column.setter
    def output_column(self, output_column):
        """Sets the output_column of this DatetimeOffsetTransform.


        :param output_column: The output_column of this DatetimeOffsetTransform.  # noqa: E501
        :type: str
        """
        if output_column is None:
            raise ValueError("Invalid value for `output_column`, must not be `None`")  # noqa: E501

        self._output_column = output_column

    @property
    def value(self):
        """Gets the value of this DatetimeOffsetTransform.  # noqa: E501


        :return: The value of this DatetimeOffsetTransform.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this DatetimeOffsetTransform.


        :param value: The value of this DatetimeOffsetTransform.  # noqa: E501
        :type: float
        """

        self._value = value

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
        if not isinstance(other, DatetimeOffsetTransform):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
