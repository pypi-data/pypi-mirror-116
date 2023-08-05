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


class IntegrationBatchHistoryReceipt(object):
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
        'batch_id': 'str',
        'dt_completed': 'datetime'
    }

    attribute_map = {
        'activity_type': 'activity_type',
        'batch_id': 'batch_id',
        'dt_completed': 'dt_completed'
    }

    def __init__(self, activity_type=None, batch_id=None, dt_completed=None):  # noqa: E501
        """IntegrationBatchHistoryReceipt - a model defined in OpenAPI"""  # noqa: E501

        self._activity_type = None
        self._batch_id = None
        self._dt_completed = None
        self.discriminator = None

        if activity_type is not None:
            self.activity_type = activity_type
        if batch_id is not None:
            self.batch_id = batch_id
        if dt_completed is not None:
            self.dt_completed = dt_completed

    @property
    def activity_type(self):
        """Gets the activity_type of this IntegrationBatchHistoryReceipt.  # noqa: E501


        :return: The activity_type of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this IntegrationBatchHistoryReceipt.


        :param activity_type: The activity_type of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :type: str
        """

        self._activity_type = activity_type

    @property
    def batch_id(self):
        """Gets the batch_id of this IntegrationBatchHistoryReceipt.  # noqa: E501


        :return: The batch_id of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :rtype: str
        """
        return self._batch_id

    @batch_id.setter
    def batch_id(self, batch_id):
        """Sets the batch_id of this IntegrationBatchHistoryReceipt.


        :param batch_id: The batch_id of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :type: str
        """

        self._batch_id = batch_id

    @property
    def dt_completed(self):
        """Gets the dt_completed of this IntegrationBatchHistoryReceipt.  # noqa: E501


        :return: The dt_completed of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_completed

    @dt_completed.setter
    def dt_completed(self, dt_completed):
        """Sets the dt_completed of this IntegrationBatchHistoryReceipt.


        :param dt_completed: The dt_completed of this IntegrationBatchHistoryReceipt.  # noqa: E501
        :type: datetime
        """

        self._dt_completed = dt_completed

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
        if not isinstance(other, IntegrationBatchHistoryReceipt):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
