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


class Integration(object):
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
        'batch_history': 'list[IntegrationBatchHistoryReceipt]',
        'dt_u': 'datetime',
        'integration_type_id': 'str',
        'loader_settings': 'LoaderSettings',
        'name': 'str',
        'parent_integration_id': 'str',
        'settings': 'dict(str, object)',
        'status': 'str',
        'sync_history': 'list[IntegrationSyncHistoryReceipt]'
    }

    attribute_map = {
        'id': '_id',
        'batch_history': 'batch_history',
        'dt_u': 'dt_u',
        'integration_type_id': 'integration_type_id',
        'loader_settings': 'loader_settings',
        'name': 'name',
        'parent_integration_id': 'parent_integration_id',
        'settings': 'settings',
        'status': 'status',
        'sync_history': 'sync_history'
    }

    def __init__(self, id=None, batch_history=None, dt_u=None, integration_type_id=None, loader_settings=None, name=None, parent_integration_id=None, settings=None, status=None, sync_history=None):  # noqa: E501
        """Integration - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._batch_history = None
        self._dt_u = None
        self._integration_type_id = None
        self._loader_settings = None
        self._name = None
        self._parent_integration_id = None
        self._settings = None
        self._status = None
        self._sync_history = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if batch_history is not None:
            self.batch_history = batch_history
        if dt_u is not None:
            self.dt_u = dt_u
        self.integration_type_id = integration_type_id
        if loader_settings is not None:
            self.loader_settings = loader_settings
        self.name = name
        if parent_integration_id is not None:
            self.parent_integration_id = parent_integration_id
        self.settings = settings
        if status is not None:
            self.status = status
        if sync_history is not None:
            self.sync_history = sync_history

    @property
    def id(self):
        """Gets the id of this Integration.  # noqa: E501


        :return: The id of this Integration.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Integration.


        :param id: The id of this Integration.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def batch_history(self):
        """Gets the batch_history of this Integration.  # noqa: E501


        :return: The batch_history of this Integration.  # noqa: E501
        :rtype: list[IntegrationBatchHistoryReceipt]
        """
        return self._batch_history

    @batch_history.setter
    def batch_history(self, batch_history):
        """Sets the batch_history of this Integration.


        :param batch_history: The batch_history of this Integration.  # noqa: E501
        :type: list[IntegrationBatchHistoryReceipt]
        """

        self._batch_history = batch_history

    @property
    def dt_u(self):
        """Gets the dt_u of this Integration.  # noqa: E501


        :return: The dt_u of this Integration.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this Integration.


        :param dt_u: The dt_u of this Integration.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def integration_type_id(self):
        """Gets the integration_type_id of this Integration.  # noqa: E501


        :return: The integration_type_id of this Integration.  # noqa: E501
        :rtype: str
        """
        return self._integration_type_id

    @integration_type_id.setter
    def integration_type_id(self, integration_type_id):
        """Sets the integration_type_id of this Integration.


        :param integration_type_id: The integration_type_id of this Integration.  # noqa: E501
        :type: str
        """
        if integration_type_id is None:
            raise ValueError("Invalid value for `integration_type_id`, must not be `None`")  # noqa: E501

        self._integration_type_id = integration_type_id

    @property
    def loader_settings(self):
        """Gets the loader_settings of this Integration.  # noqa: E501


        :return: The loader_settings of this Integration.  # noqa: E501
        :rtype: LoaderSettings
        """
        return self._loader_settings

    @loader_settings.setter
    def loader_settings(self, loader_settings):
        """Sets the loader_settings of this Integration.


        :param loader_settings: The loader_settings of this Integration.  # noqa: E501
        :type: LoaderSettings
        """

        self._loader_settings = loader_settings

    @property
    def name(self):
        """Gets the name of this Integration.  # noqa: E501


        :return: The name of this Integration.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Integration.


        :param name: The name of this Integration.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parent_integration_id(self):
        """Gets the parent_integration_id of this Integration.  # noqa: E501


        :return: The parent_integration_id of this Integration.  # noqa: E501
        :rtype: str
        """
        return self._parent_integration_id

    @parent_integration_id.setter
    def parent_integration_id(self, parent_integration_id):
        """Sets the parent_integration_id of this Integration.


        :param parent_integration_id: The parent_integration_id of this Integration.  # noqa: E501
        :type: str
        """

        self._parent_integration_id = parent_integration_id

    @property
    def settings(self):
        """Gets the settings of this Integration.  # noqa: E501


        :return: The settings of this Integration.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this Integration.


        :param settings: The settings of this Integration.  # noqa: E501
        :type: dict(str, object)
        """
        if settings is None:
            raise ValueError("Invalid value for `settings`, must not be `None`")  # noqa: E501

        self._settings = settings

    @property
    def status(self):
        """Gets the status of this Integration.  # noqa: E501


        :return: The status of this Integration.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Integration.


        :param status: The status of this Integration.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def sync_history(self):
        """Gets the sync_history of this Integration.  # noqa: E501


        :return: The sync_history of this Integration.  # noqa: E501
        :rtype: list[IntegrationSyncHistoryReceipt]
        """
        return self._sync_history

    @sync_history.setter
    def sync_history(self, sync_history):
        """Sets the sync_history of this Integration.


        :param sync_history: The sync_history of this Integration.  # noqa: E501
        :type: list[IntegrationSyncHistoryReceipt]
        """

        self._sync_history = sync_history

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
        if not isinstance(other, Integration):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
