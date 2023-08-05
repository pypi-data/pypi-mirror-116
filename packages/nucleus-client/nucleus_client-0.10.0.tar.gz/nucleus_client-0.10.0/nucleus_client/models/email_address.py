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


class EmailAddress(object):
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
        'email_address': 'str',
        'name': 'str',
        'to_type': 'str'
    }

    attribute_map = {
        'email_address': 'email_address',
        'name': 'name',
        'to_type': 'to_type'
    }

    def __init__(self, email_address=None, name=None, to_type=None):  # noqa: E501
        """EmailAddress - a model defined in OpenAPI"""  # noqa: E501

        self._email_address = None
        self._name = None
        self._to_type = None
        self.discriminator = None

        self.email_address = email_address
        self.name = name
        if to_type is not None:
            self.to_type = to_type

    @property
    def email_address(self):
        """Gets the email_address of this EmailAddress.  # noqa: E501


        :return: The email_address of this EmailAddress.  # noqa: E501
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """Sets the email_address of this EmailAddress.


        :param email_address: The email_address of this EmailAddress.  # noqa: E501
        :type: str
        """
        if email_address is None:
            raise ValueError("Invalid value for `email_address`, must not be `None`")  # noqa: E501

        self._email_address = email_address

    @property
    def name(self):
        """Gets the name of this EmailAddress.  # noqa: E501


        :return: The name of this EmailAddress.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EmailAddress.


        :param name: The name of this EmailAddress.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def to_type(self):
        """Gets the to_type of this EmailAddress.  # noqa: E501


        :return: The to_type of this EmailAddress.  # noqa: E501
        :rtype: str
        """
        return self._to_type

    @to_type.setter
    def to_type(self, to_type):
        """Sets the to_type of this EmailAddress.


        :param to_type: The to_type of this EmailAddress.  # noqa: E501
        :type: str
        """

        self._to_type = to_type

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
        if not isinstance(other, EmailAddress):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
