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


class IntegrationDataset(object):
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
        'filters': 'Filter',
        'integration_id': 'str',
        'transforms': 'Transform',
        'unions': 'IntegrationDataset'
    }

    attribute_map = {
        'activity_type': 'activity_type',
        'alias': 'alias',
        'client_id': 'client_id',
        'filters': 'filters',
        'integration_id': 'integration_id',
        'transforms': 'transforms',
        'unions': 'unions'
    }

    def __init__(self, activity_type=None, alias=None, client_id=None, filters=None, integration_id=None, transforms=None, unions=None):  # noqa: E501
        """IntegrationDataset - a model defined in OpenAPI"""  # noqa: E501

        self._activity_type = None
        self._alias = None
        self._client_id = None
        self._filters = None
        self._integration_id = None
        self._transforms = None
        self._unions = None
        self.discriminator = None

        self.activity_type = activity_type
        if alias is not None:
            self.alias = alias
        if client_id is not None:
            self.client_id = client_id
        if filters is not None:
            self.filters = filters
        if integration_id is not None:
            self.integration_id = integration_id
        if transforms is not None:
            self.transforms = transforms
        if unions is not None:
            self.unions = unions

    @property
    def activity_type(self):
        """Gets the activity_type of this IntegrationDataset.  # noqa: E501


        :return: The activity_type of this IntegrationDataset.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this IntegrationDataset.


        :param activity_type: The activity_type of this IntegrationDataset.  # noqa: E501
        :type: str
        """
        if activity_type is None:
            raise ValueError("Invalid value for `activity_type`, must not be `None`")  # noqa: E501

        self._activity_type = activity_type

    @property
    def alias(self):
        """Gets the alias of this IntegrationDataset.  # noqa: E501


        :return: The alias of this IntegrationDataset.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this IntegrationDataset.


        :param alias: The alias of this IntegrationDataset.  # noqa: E501
        :type: str
        """

        self._alias = alias

    @property
    def client_id(self):
        """Gets the client_id of this IntegrationDataset.  # noqa: E501


        :return: The client_id of this IntegrationDataset.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this IntegrationDataset.


        :param client_id: The client_id of this IntegrationDataset.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def filters(self):
        """Gets the filters of this IntegrationDataset.  # noqa: E501


        :return: The filters of this IntegrationDataset.  # noqa: E501
        :rtype: Filter
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this IntegrationDataset.


        :param filters: The filters of this IntegrationDataset.  # noqa: E501
        :type: Filter
        """

        self._filters = filters

    @property
    def integration_id(self):
        """Gets the integration_id of this IntegrationDataset.  # noqa: E501


        :return: The integration_id of this IntegrationDataset.  # noqa: E501
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this IntegrationDataset.


        :param integration_id: The integration_id of this IntegrationDataset.  # noqa: E501
        :type: str
        """

        self._integration_id = integration_id

    @property
    def transforms(self):
        """Gets the transforms of this IntegrationDataset.  # noqa: E501


        :return: The transforms of this IntegrationDataset.  # noqa: E501
        :rtype: Transform
        """
        return self._transforms

    @transforms.setter
    def transforms(self, transforms):
        """Sets the transforms of this IntegrationDataset.


        :param transforms: The transforms of this IntegrationDataset.  # noqa: E501
        :type: Transform
        """

        self._transforms = transforms

    @property
    def unions(self):
        """Gets the unions of this IntegrationDataset.  # noqa: E501


        :return: The unions of this IntegrationDataset.  # noqa: E501
        :rtype: IntegrationDataset
        """
        return self._unions

    @unions.setter
    def unions(self, unions):
        """Sets the unions of this IntegrationDataset.


        :param unions: The unions of this IntegrationDataset.  # noqa: E501
        :type: IntegrationDataset
        """

        self._unions = unions

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
        if not isinstance(other, IntegrationDataset):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
