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


class CreateCustomDatasetTask(object):
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
        'dataset': 'IntegrationDataset',
        'external_key_column': 'str',
        'filters': 'Filter',
        'joins': 'Join',
        'output_activity_type': 'str',
        'select': 'list[str]',
        'transforms': 'Transform',
        'write': 'WriteConfig'
    }

    attribute_map = {
        'dataset': 'dataset',
        'external_key_column': 'external_key_column',
        'filters': 'filters',
        'joins': 'joins',
        'output_activity_type': 'output_activity_type',
        'select': 'select',
        'transforms': 'transforms',
        'write': 'write'
    }

    def __init__(self, dataset=None, external_key_column=None, filters=None, joins=None, output_activity_type=None, select=None, transforms=None, write=None):  # noqa: E501
        """CreateCustomDatasetTask - a model defined in OpenAPI"""  # noqa: E501

        self._dataset = None
        self._external_key_column = None
        self._filters = None
        self._joins = None
        self._output_activity_type = None
        self._select = None
        self._transforms = None
        self._write = None
        self.discriminator = None

        self.dataset = dataset
        if external_key_column is not None:
            self.external_key_column = external_key_column
        if filters is not None:
            self.filters = filters
        if joins is not None:
            self.joins = joins
        self.output_activity_type = output_activity_type
        if select is not None:
            self.select = select
        if transforms is not None:
            self.transforms = transforms
        if write is not None:
            self.write = write

    @property
    def dataset(self):
        """Gets the dataset of this CreateCustomDatasetTask.  # noqa: E501


        :return: The dataset of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: IntegrationDataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this CreateCustomDatasetTask.


        :param dataset: The dataset of this CreateCustomDatasetTask.  # noqa: E501
        :type: IntegrationDataset
        """
        if dataset is None:
            raise ValueError("Invalid value for `dataset`, must not be `None`")  # noqa: E501

        self._dataset = dataset

    @property
    def external_key_column(self):
        """Gets the external_key_column of this CreateCustomDatasetTask.  # noqa: E501


        :return: The external_key_column of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: str
        """
        return self._external_key_column

    @external_key_column.setter
    def external_key_column(self, external_key_column):
        """Sets the external_key_column of this CreateCustomDatasetTask.


        :param external_key_column: The external_key_column of this CreateCustomDatasetTask.  # noqa: E501
        :type: str
        """

        self._external_key_column = external_key_column

    @property
    def filters(self):
        """Gets the filters of this CreateCustomDatasetTask.  # noqa: E501


        :return: The filters of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: Filter
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this CreateCustomDatasetTask.


        :param filters: The filters of this CreateCustomDatasetTask.  # noqa: E501
        :type: Filter
        """

        self._filters = filters

    @property
    def joins(self):
        """Gets the joins of this CreateCustomDatasetTask.  # noqa: E501


        :return: The joins of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: Join
        """
        return self._joins

    @joins.setter
    def joins(self, joins):
        """Sets the joins of this CreateCustomDatasetTask.


        :param joins: The joins of this CreateCustomDatasetTask.  # noqa: E501
        :type: Join
        """

        self._joins = joins

    @property
    def output_activity_type(self):
        """Gets the output_activity_type of this CreateCustomDatasetTask.  # noqa: E501


        :return: The output_activity_type of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: str
        """
        return self._output_activity_type

    @output_activity_type.setter
    def output_activity_type(self, output_activity_type):
        """Sets the output_activity_type of this CreateCustomDatasetTask.


        :param output_activity_type: The output_activity_type of this CreateCustomDatasetTask.  # noqa: E501
        :type: str
        """
        if output_activity_type is None:
            raise ValueError("Invalid value for `output_activity_type`, must not be `None`")  # noqa: E501

        self._output_activity_type = output_activity_type

    @property
    def select(self):
        """Gets the select of this CreateCustomDatasetTask.  # noqa: E501


        :return: The select of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: list[str]
        """
        return self._select

    @select.setter
    def select(self, select):
        """Sets the select of this CreateCustomDatasetTask.


        :param select: The select of this CreateCustomDatasetTask.  # noqa: E501
        :type: list[str]
        """

        self._select = select

    @property
    def transforms(self):
        """Gets the transforms of this CreateCustomDatasetTask.  # noqa: E501


        :return: The transforms of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: Transform
        """
        return self._transforms

    @transforms.setter
    def transforms(self, transforms):
        """Sets the transforms of this CreateCustomDatasetTask.


        :param transforms: The transforms of this CreateCustomDatasetTask.  # noqa: E501
        :type: Transform
        """

        self._transforms = transforms

    @property
    def write(self):
        """Gets the write of this CreateCustomDatasetTask.  # noqa: E501


        :return: The write of this CreateCustomDatasetTask.  # noqa: E501
        :rtype: WriteConfig
        """
        return self._write

    @write.setter
    def write(self, write):
        """Sets the write of this CreateCustomDatasetTask.


        :param write: The write of this CreateCustomDatasetTask.  # noqa: E501
        :type: WriteConfig
        """

        self._write = write

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
        if not isinstance(other, CreateCustomDatasetTask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
