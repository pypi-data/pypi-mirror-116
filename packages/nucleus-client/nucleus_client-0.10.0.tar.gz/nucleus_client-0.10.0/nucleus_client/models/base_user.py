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


class BaseUser(object):
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
        'id': 'str',
        'activation_key': 'str',
        'client_ids': 'list[str]',
        'dt_last_access': 'datetime',
        'dt_u': 'datetime',
        'email': 'str',
        'name': 'str',
        'reset_key': 'str',
        'roles': 'list[str]'
    }

    attribute_map = {
        'id': '_id',
        'activation_key': 'activation_key',
        'client_ids': 'client_ids',
        'dt_last_access': 'dt_last_access',
        'dt_u': 'dt_u',
        'email': 'email',
        'name': 'name',
        'reset_key': 'reset_key',
        'roles': 'roles'
    }

    def __init__(self, id=None, activation_key=None, client_ids=None, dt_last_access=None, dt_u=None, email=None, name=None, reset_key=None, roles=None):  # noqa: E501
        """BaseUser - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._activation_key = None
        self._client_ids = None
        self._dt_last_access = None
        self._dt_u = None
        self._email = None
        self._name = None
        self._reset_key = None
        self._roles = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if activation_key is not None:
            self.activation_key = activation_key
        if client_ids is not None:
            self.client_ids = client_ids
        if dt_last_access is not None:
            self.dt_last_access = dt_last_access
        if dt_u is not None:
            self.dt_u = dt_u
        self.email = email
        self.name = name
        if reset_key is not None:
            self.reset_key = reset_key
        if roles is not None:
            self.roles = roles

    @property
    def id(self):
        """Gets the id of this BaseUser.  # noqa: E501


        :return: The id of this BaseUser.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BaseUser.


        :param id: The id of this BaseUser.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def activation_key(self):
        """Gets the activation_key of this BaseUser.  # noqa: E501


        :return: The activation_key of this BaseUser.  # noqa: E501
        :rtype: str
        """
        return self._activation_key

    @activation_key.setter
    def activation_key(self, activation_key):
        """Sets the activation_key of this BaseUser.


        :param activation_key: The activation_key of this BaseUser.  # noqa: E501
        :type: str
        """

        self._activation_key = activation_key

    @property
    def client_ids(self):
        """Gets the client_ids of this BaseUser.  # noqa: E501


        :return: The client_ids of this BaseUser.  # noqa: E501
        :rtype: list[str]
        """
        return self._client_ids

    @client_ids.setter
    def client_ids(self, client_ids):
        """Sets the client_ids of this BaseUser.


        :param client_ids: The client_ids of this BaseUser.  # noqa: E501
        :type: list[str]
        """

        self._client_ids = client_ids

    @property
    def dt_last_access(self):
        """Gets the dt_last_access of this BaseUser.  # noqa: E501


        :return: The dt_last_access of this BaseUser.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_last_access

    @dt_last_access.setter
    def dt_last_access(self, dt_last_access):
        """Sets the dt_last_access of this BaseUser.


        :param dt_last_access: The dt_last_access of this BaseUser.  # noqa: E501
        :type: datetime
        """

        self._dt_last_access = dt_last_access

    @property
    def dt_u(self):
        """Gets the dt_u of this BaseUser.  # noqa: E501


        :return: The dt_u of this BaseUser.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this BaseUser.


        :param dt_u: The dt_u of this BaseUser.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def email(self):
        """Gets the email of this BaseUser.  # noqa: E501


        :return: The email of this BaseUser.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this BaseUser.


        :param email: The email of this BaseUser.  # noqa: E501
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def name(self):
        """Gets the name of this BaseUser.  # noqa: E501


        :return: The name of this BaseUser.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BaseUser.


        :param name: The name of this BaseUser.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def reset_key(self):
        """Gets the reset_key of this BaseUser.  # noqa: E501


        :return: The reset_key of this BaseUser.  # noqa: E501
        :rtype: str
        """
        return self._reset_key

    @reset_key.setter
    def reset_key(self, reset_key):
        """Sets the reset_key of this BaseUser.


        :param reset_key: The reset_key of this BaseUser.  # noqa: E501
        :type: str
        """

        self._reset_key = reset_key

    @property
    def roles(self):
        """Gets the roles of this BaseUser.  # noqa: E501


        :return: The roles of this BaseUser.  # noqa: E501
        :rtype: list[str]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this BaseUser.


        :param roles: The roles of this BaseUser.  # noqa: E501
        :type: list[str]
        """

        self._roles = roles

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
        if not isinstance(other, BaseUser):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
