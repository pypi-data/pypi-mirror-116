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


class DataQuery(object):
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
        'context': 'DataQueryContext',
        'header': 'bool',
        'query': 'str',
        'result_format': 'str'
    }

    attribute_map = {
        'context': 'context',
        'header': 'header',
        'query': 'query',
        'result_format': 'result_format'
    }

    def __init__(self, context=None, header=None, query=None, result_format=None):  # noqa: E501
        """DataQuery - a model defined in OpenAPI"""  # noqa: E501

        self._context = None
        self._header = None
        self._query = None
        self._result_format = None
        self.discriminator = None

        if context is not None:
            self.context = context
        if header is not None:
            self.header = header
        self.query = query
        if result_format is not None:
            self.result_format = result_format

    @property
    def context(self):
        """Gets the context of this DataQuery.  # noqa: E501


        :return: The context of this DataQuery.  # noqa: E501
        :rtype: DataQueryContext
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this DataQuery.


        :param context: The context of this DataQuery.  # noqa: E501
        :type: DataQueryContext
        """

        self._context = context

    @property
    def header(self):
        """Gets the header of this DataQuery.  # noqa: E501


        :return: The header of this DataQuery.  # noqa: E501
        :rtype: bool
        """
        return self._header

    @header.setter
    def header(self, header):
        """Sets the header of this DataQuery.


        :param header: The header of this DataQuery.  # noqa: E501
        :type: bool
        """

        self._header = header

    @property
    def query(self):
        """Gets the query of this DataQuery.  # noqa: E501


        :return: The query of this DataQuery.  # noqa: E501
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this DataQuery.


        :param query: The query of this DataQuery.  # noqa: E501
        :type: str
        """
        if query is None:
            raise ValueError("Invalid value for `query`, must not be `None`")  # noqa: E501

        self._query = query

    @property
    def result_format(self):
        """Gets the result_format of this DataQuery.  # noqa: E501


        :return: The result_format of this DataQuery.  # noqa: E501
        :rtype: str
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this DataQuery.


        :param result_format: The result_format of this DataQuery.  # noqa: E501
        :type: str
        """

        self._result_format = result_format

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
        if not isinstance(other, DataQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
