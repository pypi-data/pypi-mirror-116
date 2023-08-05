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


class DatasetMetadata(object):
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
        'activity_types': 'list[str]',
        'client_id': 'str'
    }

    attribute_map = {
        'activity_types': 'activity_types',
        'client_id': 'client_id'
    }

    def __init__(self, activity_types=None, client_id=None):  # noqa: E501
        """DatasetMetadata - a model defined in OpenAPI"""  # noqa: E501

        self._activity_types = None
        self._client_id = None
        self.discriminator = None

        self.activity_types = activity_types
        self.client_id = client_id

    @property
    def activity_types(self):
        """Gets the activity_types of this DatasetMetadata.  # noqa: E501


        :return: The activity_types of this DatasetMetadata.  # noqa: E501
        :rtype: list[str]
        """
        return self._activity_types

    @activity_types.setter
    def activity_types(self, activity_types):
        """Sets the activity_types of this DatasetMetadata.


        :param activity_types: The activity_types of this DatasetMetadata.  # noqa: E501
        :type: list[str]
        """
        if activity_types is None:
            raise ValueError("Invalid value for `activity_types`, must not be `None`")  # noqa: E501

        self._activity_types = activity_types

    @property
    def client_id(self):
        """Gets the client_id of this DatasetMetadata.  # noqa: E501


        :return: The client_id of this DatasetMetadata.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this DatasetMetadata.


        :param client_id: The client_id of this DatasetMetadata.  # noqa: E501
        :type: str
        """
        if client_id is None:
            raise ValueError("Invalid value for `client_id`, must not be `None`")  # noqa: E501

        self._client_id = client_id

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
        if not isinstance(other, DatasetMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
