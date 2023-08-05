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


class AggregationParameterizedTask(object):
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
        'date_dimension': 'DateDimension',
        'dimensions': 'Dimension',
        'filters': 'Filter',
        'granularity': 'str',
        'include_goals': 'bool',
        'joins': 'Join',
        'metrics': 'AggregationTaskMetric',
        'post_filters': 'Filter',
        'post_transforms': 'Transform',
        'segment': 'str',
        'sort': 'Sort',
        'transforms': 'Transform',
        'unique_limit': 'UniqueLimit'
    }

    attribute_map = {
        'dataset': 'dataset',
        'date_dimension': 'date_dimension',
        'dimensions': 'dimensions',
        'filters': 'filters',
        'granularity': 'granularity',
        'include_goals': 'include_goals',
        'joins': 'joins',
        'metrics': 'metrics',
        'post_filters': 'post_filters',
        'post_transforms': 'post_transforms',
        'segment': 'segment',
        'sort': 'sort',
        'transforms': 'transforms',
        'unique_limit': 'unique_limit'
    }

    def __init__(self, dataset=None, date_dimension=None, dimensions=None, filters=None, granularity=None, include_goals=None, joins=None, metrics=None, post_filters=None, post_transforms=None, segment=None, sort=None, transforms=None, unique_limit=None):  # noqa: E501
        """AggregationParameterizedTask - a model defined in OpenAPI"""  # noqa: E501

        self._dataset = None
        self._date_dimension = None
        self._dimensions = None
        self._filters = None
        self._granularity = None
        self._include_goals = None
        self._joins = None
        self._metrics = None
        self._post_filters = None
        self._post_transforms = None
        self._segment = None
        self._sort = None
        self._transforms = None
        self._unique_limit = None
        self.discriminator = None

        self.dataset = dataset
        if date_dimension is not None:
            self.date_dimension = date_dimension
        if dimensions is not None:
            self.dimensions = dimensions
        if filters is not None:
            self.filters = filters
        if granularity is not None:
            self.granularity = granularity
        if include_goals is not None:
            self.include_goals = include_goals
        if joins is not None:
            self.joins = joins
        self.metrics = metrics
        if post_filters is not None:
            self.post_filters = post_filters
        if post_transforms is not None:
            self.post_transforms = post_transforms
        self.segment = segment
        if sort is not None:
            self.sort = sort
        if transforms is not None:
            self.transforms = transforms
        if unique_limit is not None:
            self.unique_limit = unique_limit

    @property
    def dataset(self):
        """Gets the dataset of this AggregationParameterizedTask.  # noqa: E501


        :return: The dataset of this AggregationParameterizedTask.  # noqa: E501
        :rtype: IntegrationDataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this AggregationParameterizedTask.


        :param dataset: The dataset of this AggregationParameterizedTask.  # noqa: E501
        :type: IntegrationDataset
        """
        if dataset is None:
            raise ValueError("Invalid value for `dataset`, must not be `None`")  # noqa: E501

        self._dataset = dataset

    @property
    def date_dimension(self):
        """Gets the date_dimension of this AggregationParameterizedTask.  # noqa: E501


        :return: The date_dimension of this AggregationParameterizedTask.  # noqa: E501
        :rtype: DateDimension
        """
        return self._date_dimension

    @date_dimension.setter
    def date_dimension(self, date_dimension):
        """Sets the date_dimension of this AggregationParameterizedTask.


        :param date_dimension: The date_dimension of this AggregationParameterizedTask.  # noqa: E501
        :type: DateDimension
        """

        self._date_dimension = date_dimension

    @property
    def dimensions(self):
        """Gets the dimensions of this AggregationParameterizedTask.  # noqa: E501


        :return: The dimensions of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Dimension
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """Sets the dimensions of this AggregationParameterizedTask.


        :param dimensions: The dimensions of this AggregationParameterizedTask.  # noqa: E501
        :type: Dimension
        """

        self._dimensions = dimensions

    @property
    def filters(self):
        """Gets the filters of this AggregationParameterizedTask.  # noqa: E501


        :return: The filters of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Filter
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this AggregationParameterizedTask.


        :param filters: The filters of this AggregationParameterizedTask.  # noqa: E501
        :type: Filter
        """

        self._filters = filters

    @property
    def granularity(self):
        """Gets the granularity of this AggregationParameterizedTask.  # noqa: E501


        :return: The granularity of this AggregationParameterizedTask.  # noqa: E501
        :rtype: str
        """
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """Sets the granularity of this AggregationParameterizedTask.


        :param granularity: The granularity of this AggregationParameterizedTask.  # noqa: E501
        :type: str
        """

        self._granularity = granularity

    @property
    def include_goals(self):
        """Gets the include_goals of this AggregationParameterizedTask.  # noqa: E501


        :return: The include_goals of this AggregationParameterizedTask.  # noqa: E501
        :rtype: bool
        """
        return self._include_goals

    @include_goals.setter
    def include_goals(self, include_goals):
        """Sets the include_goals of this AggregationParameterizedTask.


        :param include_goals: The include_goals of this AggregationParameterizedTask.  # noqa: E501
        :type: bool
        """

        self._include_goals = include_goals

    @property
    def joins(self):
        """Gets the joins of this AggregationParameterizedTask.  # noqa: E501


        :return: The joins of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Join
        """
        return self._joins

    @joins.setter
    def joins(self, joins):
        """Sets the joins of this AggregationParameterizedTask.


        :param joins: The joins of this AggregationParameterizedTask.  # noqa: E501
        :type: Join
        """

        self._joins = joins

    @property
    def metrics(self):
        """Gets the metrics of this AggregationParameterizedTask.  # noqa: E501


        :return: The metrics of this AggregationParameterizedTask.  # noqa: E501
        :rtype: AggregationTaskMetric
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """Sets the metrics of this AggregationParameterizedTask.


        :param metrics: The metrics of this AggregationParameterizedTask.  # noqa: E501
        :type: AggregationTaskMetric
        """
        if metrics is None:
            raise ValueError("Invalid value for `metrics`, must not be `None`")  # noqa: E501

        self._metrics = metrics

    @property
    def post_filters(self):
        """Gets the post_filters of this AggregationParameterizedTask.  # noqa: E501


        :return: The post_filters of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Filter
        """
        return self._post_filters

    @post_filters.setter
    def post_filters(self, post_filters):
        """Sets the post_filters of this AggregationParameterizedTask.


        :param post_filters: The post_filters of this AggregationParameterizedTask.  # noqa: E501
        :type: Filter
        """

        self._post_filters = post_filters

    @property
    def post_transforms(self):
        """Gets the post_transforms of this AggregationParameterizedTask.  # noqa: E501


        :return: The post_transforms of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Transform
        """
        return self._post_transforms

    @post_transforms.setter
    def post_transforms(self, post_transforms):
        """Sets the post_transforms of this AggregationParameterizedTask.


        :param post_transforms: The post_transforms of this AggregationParameterizedTask.  # noqa: E501
        :type: Transform
        """

        self._post_transforms = post_transforms

    @property
    def segment(self):
        """Gets the segment of this AggregationParameterizedTask.  # noqa: E501


        :return: The segment of this AggregationParameterizedTask.  # noqa: E501
        :rtype: str
        """
        return self._segment

    @segment.setter
    def segment(self, segment):
        """Sets the segment of this AggregationParameterizedTask.


        :param segment: The segment of this AggregationParameterizedTask.  # noqa: E501
        :type: str
        """
        if segment is None:
            raise ValueError("Invalid value for `segment`, must not be `None`")  # noqa: E501

        self._segment = segment

    @property
    def sort(self):
        """Gets the sort of this AggregationParameterizedTask.  # noqa: E501


        :return: The sort of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Sort
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """Sets the sort of this AggregationParameterizedTask.


        :param sort: The sort of this AggregationParameterizedTask.  # noqa: E501
        :type: Sort
        """

        self._sort = sort

    @property
    def transforms(self):
        """Gets the transforms of this AggregationParameterizedTask.  # noqa: E501


        :return: The transforms of this AggregationParameterizedTask.  # noqa: E501
        :rtype: Transform
        """
        return self._transforms

    @transforms.setter
    def transforms(self, transforms):
        """Sets the transforms of this AggregationParameterizedTask.


        :param transforms: The transforms of this AggregationParameterizedTask.  # noqa: E501
        :type: Transform
        """

        self._transforms = transforms

    @property
    def unique_limit(self):
        """Gets the unique_limit of this AggregationParameterizedTask.  # noqa: E501


        :return: The unique_limit of this AggregationParameterizedTask.  # noqa: E501
        :rtype: UniqueLimit
        """
        return self._unique_limit

    @unique_limit.setter
    def unique_limit(self, unique_limit):
        """Sets the unique_limit of this AggregationParameterizedTask.


        :param unique_limit: The unique_limit of this AggregationParameterizedTask.  # noqa: E501
        :type: UniqueLimit
        """

        self._unique_limit = unique_limit

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
        if not isinstance(other, AggregationParameterizedTask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
