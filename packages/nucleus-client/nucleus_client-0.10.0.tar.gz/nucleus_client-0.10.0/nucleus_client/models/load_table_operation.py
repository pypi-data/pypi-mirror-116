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


class LoadTableOperation(object):
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
        'activity_type': 'str',
        'alias': 'str',
        'client_id': 'str',
        'integration_id': 'str',
        'partner_id': 'str',
        'schema': 'JobOperationSchema',
        'schema_id': 'str'
    }

    attribute_map = {
        'activity_type': 'activity_type',
        'alias': 'alias',
        'client_id': 'client_id',
        'integration_id': 'integration_id',
        'partner_id': 'partner_id',
        'schema': 'schema',
        'schema_id': 'schema_id'
    }

    def __init__(self, activity_type=None, alias=None, client_id=None, integration_id=None, partner_id=None, schema=None, schema_id=None):  # noqa: E501
        """LoadTableOperation - a model defined in OpenAPI"""  # noqa: E501

        self._activity_type = None
        self._alias = None
        self._client_id = None
        self._integration_id = None
        self._partner_id = None
        self._schema = None
        self._schema_id = None
        self.discriminator = None

        if activity_type is not None:
            self.activity_type = activity_type
        if alias is not None:
            self.alias = alias
        if client_id is not None:
            self.client_id = client_id
        if integration_id is not None:
            self.integration_id = integration_id
        if partner_id is not None:
            self.partner_id = partner_id
        if schema is not None:
            self.schema = schema
        if schema_id is not None:
            self.schema_id = schema_id

    @property
    def activity_type(self):
        """Gets the activity_type of this LoadTableOperation.  # noqa: E501


        :return: The activity_type of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this LoadTableOperation.


        :param activity_type: The activity_type of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._activity_type = activity_type

    @property
    def alias(self):
        """Gets the alias of this LoadTableOperation.  # noqa: E501


        :return: The alias of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this LoadTableOperation.


        :param alias: The alias of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._alias = alias

    @property
    def client_id(self):
        """Gets the client_id of this LoadTableOperation.  # noqa: E501


        :return: The client_id of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this LoadTableOperation.


        :param client_id: The client_id of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def integration_id(self):
        """Gets the integration_id of this LoadTableOperation.  # noqa: E501


        :return: The integration_id of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this LoadTableOperation.


        :param integration_id: The integration_id of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._integration_id = integration_id

    @property
    def partner_id(self):
        """Gets the partner_id of this LoadTableOperation.  # noqa: E501


        :return: The partner_id of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._partner_id

    @partner_id.setter
    def partner_id(self, partner_id):
        """Sets the partner_id of this LoadTableOperation.


        :param partner_id: The partner_id of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._partner_id = partner_id

    @property
    def schema(self):
        """Gets the schema of this LoadTableOperation.  # noqa: E501


        :return: The schema of this LoadTableOperation.  # noqa: E501
        :rtype: JobOperationSchema
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """Sets the schema of this LoadTableOperation.


        :param schema: The schema of this LoadTableOperation.  # noqa: E501
        :type: JobOperationSchema
        """

        self._schema = schema

    @property
    def schema_id(self):
        """Gets the schema_id of this LoadTableOperation.  # noqa: E501


        :return: The schema_id of this LoadTableOperation.  # noqa: E501
        :rtype: str
        """
        return self._schema_id

    @schema_id.setter
    def schema_id(self, schema_id):
        """Sets the schema_id of this LoadTableOperation.


        :param schema_id: The schema_id of this LoadTableOperation.  # noqa: E501
        :type: str
        """

        self._schema_id = schema_id

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
        if not isinstance(other, LoadTableOperation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
