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


class AggregationTaskMetric(object):
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
        'add': 'AddMetric',
        'average': 'UnaryMetric',
        'avg': 'UnaryMetric',
        'collect': 'UnaryMetric',
        'collect_set': 'UnaryMetric',
        'count': 'CountMetric',
        'count_distinct': 'UnaryMetric',
        'count_distinct_approx': 'UnaryMetric',
        'cumulative': 'CumulativeMetric',
        'cumulative_count': 'UnaryMetric',
        'cumulative_sum': 'CumulativeSumMetric',
        'divide': 'DivideMetric',
        'implode': 'UnaryMetric',
        'kurtosis': 'UnaryMetric',
        'min': 'UnaryMetric',
        'multiply': 'MultiplyMetric',
        'percentage': 'PercentageMetric',
        'percentile_lookup': 'PercentileLookupMetric',
        'sample_standard_deviation': 'UnaryMetric',
        'sample_stddev': 'UnaryMetric',
        'skewness': 'UnaryMetric',
        'standard_deviation': 'UnaryMetric',
        'stddev': 'UnaryMetric',
        'subtract': 'SubtractMetric',
        'sum': 'UnaryMetric',
        'variance': 'UnaryMetric'
    }

    attribute_map = {
        'add': 'add',
        'average': 'average',
        'avg': 'avg',
        'collect': 'collect',
        'collect_set': 'collect_set',
        'count': 'count',
        'count_distinct': 'count_distinct',
        'count_distinct_approx': 'count_distinct_approx',
        'cumulative': 'cumulative',
        'cumulative_count': 'cumulative_count',
        'cumulative_sum': 'cumulative_sum',
        'divide': 'divide',
        'implode': 'implode',
        'kurtosis': 'kurtosis',
        'min': 'min',
        'multiply': 'multiply',
        'percentage': 'percentage',
        'percentile_lookup': 'percentile_lookup',
        'sample_standard_deviation': 'sample_standard_deviation',
        'sample_stddev': 'sample_stddev',
        'skewness': 'skewness',
        'standard_deviation': 'standard_deviation',
        'stddev': 'stddev',
        'subtract': 'subtract',
        'sum': 'sum',
        'variance': 'variance'
    }

    def __init__(self, add=None, average=None, avg=None, collect=None, collect_set=None, count=None, count_distinct=None, count_distinct_approx=None, cumulative=None, cumulative_count=None, cumulative_sum=None, divide=None, implode=None, kurtosis=None, min=None, multiply=None, percentage=None, percentile_lookup=None, sample_standard_deviation=None, sample_stddev=None, skewness=None, standard_deviation=None, stddev=None, subtract=None, sum=None, variance=None):  # noqa: E501
        """AggregationTaskMetric - a model defined in OpenAPI"""  # noqa: E501

        self._add = None
        self._average = None
        self._avg = None
        self._collect = None
        self._collect_set = None
        self._count = None
        self._count_distinct = None
        self._count_distinct_approx = None
        self._cumulative = None
        self._cumulative_count = None
        self._cumulative_sum = None
        self._divide = None
        self._implode = None
        self._kurtosis = None
        self._min = None
        self._multiply = None
        self._percentage = None
        self._percentile_lookup = None
        self._sample_standard_deviation = None
        self._sample_stddev = None
        self._skewness = None
        self._standard_deviation = None
        self._stddev = None
        self._subtract = None
        self._sum = None
        self._variance = None
        self.discriminator = None

        if add is not None:
            self.add = add
        if average is not None:
            self.average = average
        if avg is not None:
            self.avg = avg
        if collect is not None:
            self.collect = collect
        if collect_set is not None:
            self.collect_set = collect_set
        if count is not None:
            self.count = count
        if count_distinct is not None:
            self.count_distinct = count_distinct
        if count_distinct_approx is not None:
            self.count_distinct_approx = count_distinct_approx
        if cumulative is not None:
            self.cumulative = cumulative
        if cumulative_count is not None:
            self.cumulative_count = cumulative_count
        if cumulative_sum is not None:
            self.cumulative_sum = cumulative_sum
        if divide is not None:
            self.divide = divide
        if implode is not None:
            self.implode = implode
        if kurtosis is not None:
            self.kurtosis = kurtosis
        if min is not None:
            self.min = min
        if multiply is not None:
            self.multiply = multiply
        if percentage is not None:
            self.percentage = percentage
        if percentile_lookup is not None:
            self.percentile_lookup = percentile_lookup
        if sample_standard_deviation is not None:
            self.sample_standard_deviation = sample_standard_deviation
        if sample_stddev is not None:
            self.sample_stddev = sample_stddev
        if skewness is not None:
            self.skewness = skewness
        if standard_deviation is not None:
            self.standard_deviation = standard_deviation
        if stddev is not None:
            self.stddev = stddev
        if subtract is not None:
            self.subtract = subtract
        if sum is not None:
            self.sum = sum
        if variance is not None:
            self.variance = variance

    @property
    def add(self):
        """Gets the add of this AggregationTaskMetric.  # noqa: E501


        :return: The add of this AggregationTaskMetric.  # noqa: E501
        :rtype: AddMetric
        """
        return self._add

    @add.setter
    def add(self, add):
        """Sets the add of this AggregationTaskMetric.


        :param add: The add of this AggregationTaskMetric.  # noqa: E501
        :type: AddMetric
        """

        self._add = add

    @property
    def average(self):
        """Gets the average of this AggregationTaskMetric.  # noqa: E501


        :return: The average of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._average

    @average.setter
    def average(self, average):
        """Sets the average of this AggregationTaskMetric.


        :param average: The average of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._average = average

    @property
    def avg(self):
        """Gets the avg of this AggregationTaskMetric.  # noqa: E501


        :return: The avg of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._avg

    @avg.setter
    def avg(self, avg):
        """Sets the avg of this AggregationTaskMetric.


        :param avg: The avg of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._avg = avg

    @property
    def collect(self):
        """Gets the collect of this AggregationTaskMetric.  # noqa: E501


        :return: The collect of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._collect

    @collect.setter
    def collect(self, collect):
        """Sets the collect of this AggregationTaskMetric.


        :param collect: The collect of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._collect = collect

    @property
    def collect_set(self):
        """Gets the collect_set of this AggregationTaskMetric.  # noqa: E501


        :return: The collect_set of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._collect_set

    @collect_set.setter
    def collect_set(self, collect_set):
        """Sets the collect_set of this AggregationTaskMetric.


        :param collect_set: The collect_set of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._collect_set = collect_set

    @property
    def count(self):
        """Gets the count of this AggregationTaskMetric.  # noqa: E501


        :return: The count of this AggregationTaskMetric.  # noqa: E501
        :rtype: CountMetric
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this AggregationTaskMetric.


        :param count: The count of this AggregationTaskMetric.  # noqa: E501
        :type: CountMetric
        """

        self._count = count

    @property
    def count_distinct(self):
        """Gets the count_distinct of this AggregationTaskMetric.  # noqa: E501


        :return: The count_distinct of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._count_distinct

    @count_distinct.setter
    def count_distinct(self, count_distinct):
        """Sets the count_distinct of this AggregationTaskMetric.


        :param count_distinct: The count_distinct of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._count_distinct = count_distinct

    @property
    def count_distinct_approx(self):
        """Gets the count_distinct_approx of this AggregationTaskMetric.  # noqa: E501


        :return: The count_distinct_approx of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._count_distinct_approx

    @count_distinct_approx.setter
    def count_distinct_approx(self, count_distinct_approx):
        """Sets the count_distinct_approx of this AggregationTaskMetric.


        :param count_distinct_approx: The count_distinct_approx of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._count_distinct_approx = count_distinct_approx

    @property
    def cumulative(self):
        """Gets the cumulative of this AggregationTaskMetric.  # noqa: E501


        :return: The cumulative of this AggregationTaskMetric.  # noqa: E501
        :rtype: CumulativeMetric
        """
        return self._cumulative

    @cumulative.setter
    def cumulative(self, cumulative):
        """Sets the cumulative of this AggregationTaskMetric.


        :param cumulative: The cumulative of this AggregationTaskMetric.  # noqa: E501
        :type: CumulativeMetric
        """

        self._cumulative = cumulative

    @property
    def cumulative_count(self):
        """Gets the cumulative_count of this AggregationTaskMetric.  # noqa: E501


        :return: The cumulative_count of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._cumulative_count

    @cumulative_count.setter
    def cumulative_count(self, cumulative_count):
        """Sets the cumulative_count of this AggregationTaskMetric.


        :param cumulative_count: The cumulative_count of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._cumulative_count = cumulative_count

    @property
    def cumulative_sum(self):
        """Gets the cumulative_sum of this AggregationTaskMetric.  # noqa: E501


        :return: The cumulative_sum of this AggregationTaskMetric.  # noqa: E501
        :rtype: CumulativeSumMetric
        """
        return self._cumulative_sum

    @cumulative_sum.setter
    def cumulative_sum(self, cumulative_sum):
        """Sets the cumulative_sum of this AggregationTaskMetric.


        :param cumulative_sum: The cumulative_sum of this AggregationTaskMetric.  # noqa: E501
        :type: CumulativeSumMetric
        """

        self._cumulative_sum = cumulative_sum

    @property
    def divide(self):
        """Gets the divide of this AggregationTaskMetric.  # noqa: E501


        :return: The divide of this AggregationTaskMetric.  # noqa: E501
        :rtype: DivideMetric
        """
        return self._divide

    @divide.setter
    def divide(self, divide):
        """Sets the divide of this AggregationTaskMetric.


        :param divide: The divide of this AggregationTaskMetric.  # noqa: E501
        :type: DivideMetric
        """

        self._divide = divide

    @property
    def implode(self):
        """Gets the implode of this AggregationTaskMetric.  # noqa: E501


        :return: The implode of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._implode

    @implode.setter
    def implode(self, implode):
        """Sets the implode of this AggregationTaskMetric.


        :param implode: The implode of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._implode = implode

    @property
    def kurtosis(self):
        """Gets the kurtosis of this AggregationTaskMetric.  # noqa: E501


        :return: The kurtosis of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._kurtosis

    @kurtosis.setter
    def kurtosis(self, kurtosis):
        """Sets the kurtosis of this AggregationTaskMetric.


        :param kurtosis: The kurtosis of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._kurtosis = kurtosis

    @property
    def min(self):
        """Gets the min of this AggregationTaskMetric.  # noqa: E501


        :return: The min of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._min

    @min.setter
    def min(self, min):
        """Sets the min of this AggregationTaskMetric.


        :param min: The min of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._min = min

    @property
    def multiply(self):
        """Gets the multiply of this AggregationTaskMetric.  # noqa: E501


        :return: The multiply of this AggregationTaskMetric.  # noqa: E501
        :rtype: MultiplyMetric
        """
        return self._multiply

    @multiply.setter
    def multiply(self, multiply):
        """Sets the multiply of this AggregationTaskMetric.


        :param multiply: The multiply of this AggregationTaskMetric.  # noqa: E501
        :type: MultiplyMetric
        """

        self._multiply = multiply

    @property
    def percentage(self):
        """Gets the percentage of this AggregationTaskMetric.  # noqa: E501


        :return: The percentage of this AggregationTaskMetric.  # noqa: E501
        :rtype: PercentageMetric
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """Sets the percentage of this AggregationTaskMetric.


        :param percentage: The percentage of this AggregationTaskMetric.  # noqa: E501
        :type: PercentageMetric
        """

        self._percentage = percentage

    @property
    def percentile_lookup(self):
        """Gets the percentile_lookup of this AggregationTaskMetric.  # noqa: E501


        :return: The percentile_lookup of this AggregationTaskMetric.  # noqa: E501
        :rtype: PercentileLookupMetric
        """
        return self._percentile_lookup

    @percentile_lookup.setter
    def percentile_lookup(self, percentile_lookup):
        """Sets the percentile_lookup of this AggregationTaskMetric.


        :param percentile_lookup: The percentile_lookup of this AggregationTaskMetric.  # noqa: E501
        :type: PercentileLookupMetric
        """

        self._percentile_lookup = percentile_lookup

    @property
    def sample_standard_deviation(self):
        """Gets the sample_standard_deviation of this AggregationTaskMetric.  # noqa: E501


        :return: The sample_standard_deviation of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._sample_standard_deviation

    @sample_standard_deviation.setter
    def sample_standard_deviation(self, sample_standard_deviation):
        """Sets the sample_standard_deviation of this AggregationTaskMetric.


        :param sample_standard_deviation: The sample_standard_deviation of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._sample_standard_deviation = sample_standard_deviation

    @property
    def sample_stddev(self):
        """Gets the sample_stddev of this AggregationTaskMetric.  # noqa: E501


        :return: The sample_stddev of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._sample_stddev

    @sample_stddev.setter
    def sample_stddev(self, sample_stddev):
        """Sets the sample_stddev of this AggregationTaskMetric.


        :param sample_stddev: The sample_stddev of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._sample_stddev = sample_stddev

    @property
    def skewness(self):
        """Gets the skewness of this AggregationTaskMetric.  # noqa: E501


        :return: The skewness of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._skewness

    @skewness.setter
    def skewness(self, skewness):
        """Sets the skewness of this AggregationTaskMetric.


        :param skewness: The skewness of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._skewness = skewness

    @property
    def standard_deviation(self):
        """Gets the standard_deviation of this AggregationTaskMetric.  # noqa: E501


        :return: The standard_deviation of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._standard_deviation

    @standard_deviation.setter
    def standard_deviation(self, standard_deviation):
        """Sets the standard_deviation of this AggregationTaskMetric.


        :param standard_deviation: The standard_deviation of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._standard_deviation = standard_deviation

    @property
    def stddev(self):
        """Gets the stddev of this AggregationTaskMetric.  # noqa: E501


        :return: The stddev of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._stddev

    @stddev.setter
    def stddev(self, stddev):
        """Sets the stddev of this AggregationTaskMetric.


        :param stddev: The stddev of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._stddev = stddev

    @property
    def subtract(self):
        """Gets the subtract of this AggregationTaskMetric.  # noqa: E501


        :return: The subtract of this AggregationTaskMetric.  # noqa: E501
        :rtype: SubtractMetric
        """
        return self._subtract

    @subtract.setter
    def subtract(self, subtract):
        """Sets the subtract of this AggregationTaskMetric.


        :param subtract: The subtract of this AggregationTaskMetric.  # noqa: E501
        :type: SubtractMetric
        """

        self._subtract = subtract

    @property
    def sum(self):
        """Gets the sum of this AggregationTaskMetric.  # noqa: E501


        :return: The sum of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._sum

    @sum.setter
    def sum(self, sum):
        """Sets the sum of this AggregationTaskMetric.


        :param sum: The sum of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._sum = sum

    @property
    def variance(self):
        """Gets the variance of this AggregationTaskMetric.  # noqa: E501


        :return: The variance of this AggregationTaskMetric.  # noqa: E501
        :rtype: UnaryMetric
        """
        return self._variance

    @variance.setter
    def variance(self, variance):
        """Sets the variance of this AggregationTaskMetric.


        :param variance: The variance of this AggregationTaskMetric.  # noqa: E501
        :type: UnaryMetric
        """

        self._variance = variance

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
        if not isinstance(other, AggregationTaskMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
