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


class PartnerPostData(object):
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
        'client_xref_id': 'str',
        'data': 'dict(str, object)',
        'dt_activity': 'datetime',
        'dt_u': 'datetime',
        'existing_entity_external_key': 'list[str]',
        'existing_entity_type': 'str',
        'external_key': 'list[str]'
    }

    attribute_map = {
        'client_xref_id': 'client_xref_id',
        'data': 'data',
        'dt_activity': 'dt_activity',
        'dt_u': 'dt_u',
        'existing_entity_external_key': 'existing_entity_external_key',
        'existing_entity_type': 'existing_entity_type',
        'external_key': 'external_key'
    }

    def __init__(self, client_xref_id=None, data=None, dt_activity=None, dt_u=None, existing_entity_external_key=None, existing_entity_type=None, external_key=None):  # noqa: E501
        """PartnerPostData - a model defined in OpenAPI"""  # noqa: E501

        self._client_xref_id = None
        self._data = None
        self._dt_activity = None
        self._dt_u = None
        self._existing_entity_external_key = None
        self._existing_entity_type = None
        self._external_key = None
        self.discriminator = None

        if client_xref_id is not None:
            self.client_xref_id = client_xref_id
        self.data = data
        self.dt_activity = dt_activity
        if dt_u is not None:
            self.dt_u = dt_u
        if existing_entity_external_key is not None:
            self.existing_entity_external_key = existing_entity_external_key
        if existing_entity_type is not None:
            self.existing_entity_type = existing_entity_type
        self.external_key = external_key

    @property
    def client_xref_id(self):
        """Gets the client_xref_id of this PartnerPostData.  # noqa: E501


        :return: The client_xref_id of this PartnerPostData.  # noqa: E501
        :rtype: str
        """
        return self._client_xref_id

    @client_xref_id.setter
    def client_xref_id(self, client_xref_id):
        """Sets the client_xref_id of this PartnerPostData.


        :param client_xref_id: The client_xref_id of this PartnerPostData.  # noqa: E501
        :type: str
        """

        self._client_xref_id = client_xref_id

    @property
    def data(self):
        """Gets the data of this PartnerPostData.  # noqa: E501


        :return: The data of this PartnerPostData.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this PartnerPostData.


        :param data: The data of this PartnerPostData.  # noqa: E501
        :type: dict(str, object)
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data

    @property
    def dt_activity(self):
        """Gets the dt_activity of this PartnerPostData.  # noqa: E501


        :return: The dt_activity of this PartnerPostData.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_activity

    @dt_activity.setter
    def dt_activity(self, dt_activity):
        """Sets the dt_activity of this PartnerPostData.


        :param dt_activity: The dt_activity of this PartnerPostData.  # noqa: E501
        :type: datetime
        """
        if dt_activity is None:
            raise ValueError("Invalid value for `dt_activity`, must not be `None`")  # noqa: E501

        self._dt_activity = dt_activity

    @property
    def dt_u(self):
        """Gets the dt_u of this PartnerPostData.  # noqa: E501


        :return: The dt_u of this PartnerPostData.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this PartnerPostData.


        :param dt_u: The dt_u of this PartnerPostData.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def existing_entity_external_key(self):
        """Gets the existing_entity_external_key of this PartnerPostData.  # noqa: E501


        :return: The existing_entity_external_key of this PartnerPostData.  # noqa: E501
        :rtype: list[str]
        """
        return self._existing_entity_external_key

    @existing_entity_external_key.setter
    def existing_entity_external_key(self, existing_entity_external_key):
        """Sets the existing_entity_external_key of this PartnerPostData.


        :param existing_entity_external_key: The existing_entity_external_key of this PartnerPostData.  # noqa: E501
        :type: list[str]
        """

        self._existing_entity_external_key = existing_entity_external_key

    @property
    def existing_entity_type(self):
        """Gets the existing_entity_type of this PartnerPostData.  # noqa: E501


        :return: The existing_entity_type of this PartnerPostData.  # noqa: E501
        :rtype: str
        """
        return self._existing_entity_type

    @existing_entity_type.setter
    def existing_entity_type(self, existing_entity_type):
        """Sets the existing_entity_type of this PartnerPostData.


        :param existing_entity_type: The existing_entity_type of this PartnerPostData.  # noqa: E501
        :type: str
        """

        self._existing_entity_type = existing_entity_type

    @property
    def external_key(self):
        """Gets the external_key of this PartnerPostData.  # noqa: E501


        :return: The external_key of this PartnerPostData.  # noqa: E501
        :rtype: list[str]
        """
        return self._external_key

    @external_key.setter
    def external_key(self, external_key):
        """Sets the external_key of this PartnerPostData.


        :param external_key: The external_key of this PartnerPostData.  # noqa: E501
        :type: list[str]
        """
        if external_key is None:
            raise ValueError("Invalid value for `external_key`, must not be `None`")  # noqa: E501

        self._external_key = external_key

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
        if not isinstance(other, PartnerPostData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
