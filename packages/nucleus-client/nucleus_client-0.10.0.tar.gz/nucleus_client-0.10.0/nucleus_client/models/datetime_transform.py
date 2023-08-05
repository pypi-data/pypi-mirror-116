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


class DatetimeTransform(object):
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
        'constant': 'DatetimeConstantTransform',
        'current_date': 'DatetimeCurrentDateTransform',
        'current_timestamp': 'DatetimeCurrentTimestampTransform',
        'diff': 'DatetimeDiffTransform',
        'diff_from_column_date': 'DatetimeDiffFromColumnDateTransform',
        'diff_from_now': 'DatetimeDiffFromNowTransform',
        'diff_from_static_date': 'DatetimeDiffFromStaticDateTransform',
        'format': 'DatetimeFormatTransform',
        'now': 'DatetimeCurrentTimestampTransform',
        'offset': 'DatetimeOffsetTransform',
        'offset_column_value': 'DatetimeOffsetColumnValueTransform',
        'offset_static_value': 'DatetimeOffsetStaticValueTransform',
        'range': 'DatetimeRangeTransform',
        'select': 'DatetimeSelectTransform',
        'today': 'DatetimeCurrentDateTransform'
    }

    attribute_map = {
        'constant': 'constant',
        'current_date': 'current_date',
        'current_timestamp': 'current_timestamp',
        'diff': 'diff',
        'diff_from_column_date': 'diff_from_column_date',
        'diff_from_now': 'diff_from_now',
        'diff_from_static_date': 'diff_from_static_date',
        'format': 'format',
        'now': 'now',
        'offset': 'offset',
        'offset_column_value': 'offset_column_value',
        'offset_static_value': 'offset_static_value',
        'range': 'range',
        'select': 'select',
        'today': 'today'
    }

    def __init__(self, constant=None, current_date=None, current_timestamp=None, diff=None, diff_from_column_date=None, diff_from_now=None, diff_from_static_date=None, format=None, now=None, offset=None, offset_column_value=None, offset_static_value=None, range=None, select=None, today=None):  # noqa: E501
        """DatetimeTransform - a model defined in OpenAPI"""  # noqa: E501

        self._constant = None
        self._current_date = None
        self._current_timestamp = None
        self._diff = None
        self._diff_from_column_date = None
        self._diff_from_now = None
        self._diff_from_static_date = None
        self._format = None
        self._now = None
        self._offset = None
        self._offset_column_value = None
        self._offset_static_value = None
        self._range = None
        self._select = None
        self._today = None
        self.discriminator = None

        if constant is not None:
            self.constant = constant
        if current_date is not None:
            self.current_date = current_date
        if current_timestamp is not None:
            self.current_timestamp = current_timestamp
        if diff is not None:
            self.diff = diff
        if diff_from_column_date is not None:
            self.diff_from_column_date = diff_from_column_date
        if diff_from_now is not None:
            self.diff_from_now = diff_from_now
        if diff_from_static_date is not None:
            self.diff_from_static_date = diff_from_static_date
        if format is not None:
            self.format = format
        if now is not None:
            self.now = now
        if offset is not None:
            self.offset = offset
        if offset_column_value is not None:
            self.offset_column_value = offset_column_value
        if offset_static_value is not None:
            self.offset_static_value = offset_static_value
        if range is not None:
            self.range = range
        if select is not None:
            self.select = select
        if today is not None:
            self.today = today

    @property
    def constant(self):
        """Gets the constant of this DatetimeTransform.  # noqa: E501


        :return: The constant of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeConstantTransform
        """
        return self._constant

    @constant.setter
    def constant(self, constant):
        """Sets the constant of this DatetimeTransform.


        :param constant: The constant of this DatetimeTransform.  # noqa: E501
        :type: DatetimeConstantTransform
        """

        self._constant = constant

    @property
    def current_date(self):
        """Gets the current_date of this DatetimeTransform.  # noqa: E501


        :return: The current_date of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeCurrentDateTransform
        """
        return self._current_date

    @current_date.setter
    def current_date(self, current_date):
        """Sets the current_date of this DatetimeTransform.


        :param current_date: The current_date of this DatetimeTransform.  # noqa: E501
        :type: DatetimeCurrentDateTransform
        """

        self._current_date = current_date

    @property
    def current_timestamp(self):
        """Gets the current_timestamp of this DatetimeTransform.  # noqa: E501


        :return: The current_timestamp of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeCurrentTimestampTransform
        """
        return self._current_timestamp

    @current_timestamp.setter
    def current_timestamp(self, current_timestamp):
        """Sets the current_timestamp of this DatetimeTransform.


        :param current_timestamp: The current_timestamp of this DatetimeTransform.  # noqa: E501
        :type: DatetimeCurrentTimestampTransform
        """

        self._current_timestamp = current_timestamp

    @property
    def diff(self):
        """Gets the diff of this DatetimeTransform.  # noqa: E501


        :return: The diff of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeDiffTransform
        """
        return self._diff

    @diff.setter
    def diff(self, diff):
        """Sets the diff of this DatetimeTransform.


        :param diff: The diff of this DatetimeTransform.  # noqa: E501
        :type: DatetimeDiffTransform
        """

        self._diff = diff

    @property
    def diff_from_column_date(self):
        """Gets the diff_from_column_date of this DatetimeTransform.  # noqa: E501


        :return: The diff_from_column_date of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeDiffFromColumnDateTransform
        """
        return self._diff_from_column_date

    @diff_from_column_date.setter
    def diff_from_column_date(self, diff_from_column_date):
        """Sets the diff_from_column_date of this DatetimeTransform.


        :param diff_from_column_date: The diff_from_column_date of this DatetimeTransform.  # noqa: E501
        :type: DatetimeDiffFromColumnDateTransform
        """

        self._diff_from_column_date = diff_from_column_date

    @property
    def diff_from_now(self):
        """Gets the diff_from_now of this DatetimeTransform.  # noqa: E501


        :return: The diff_from_now of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeDiffFromNowTransform
        """
        return self._diff_from_now

    @diff_from_now.setter
    def diff_from_now(self, diff_from_now):
        """Sets the diff_from_now of this DatetimeTransform.


        :param diff_from_now: The diff_from_now of this DatetimeTransform.  # noqa: E501
        :type: DatetimeDiffFromNowTransform
        """

        self._diff_from_now = diff_from_now

    @property
    def diff_from_static_date(self):
        """Gets the diff_from_static_date of this DatetimeTransform.  # noqa: E501


        :return: The diff_from_static_date of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeDiffFromStaticDateTransform
        """
        return self._diff_from_static_date

    @diff_from_static_date.setter
    def diff_from_static_date(self, diff_from_static_date):
        """Sets the diff_from_static_date of this DatetimeTransform.


        :param diff_from_static_date: The diff_from_static_date of this DatetimeTransform.  # noqa: E501
        :type: DatetimeDiffFromStaticDateTransform
        """

        self._diff_from_static_date = diff_from_static_date

    @property
    def format(self):
        """Gets the format of this DatetimeTransform.  # noqa: E501


        :return: The format of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeFormatTransform
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this DatetimeTransform.


        :param format: The format of this DatetimeTransform.  # noqa: E501
        :type: DatetimeFormatTransform
        """

        self._format = format

    @property
    def now(self):
        """Gets the now of this DatetimeTransform.  # noqa: E501


        :return: The now of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeCurrentTimestampTransform
        """
        return self._now

    @now.setter
    def now(self, now):
        """Sets the now of this DatetimeTransform.


        :param now: The now of this DatetimeTransform.  # noqa: E501
        :type: DatetimeCurrentTimestampTransform
        """

        self._now = now

    @property
    def offset(self):
        """Gets the offset of this DatetimeTransform.  # noqa: E501


        :return: The offset of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeOffsetTransform
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this DatetimeTransform.


        :param offset: The offset of this DatetimeTransform.  # noqa: E501
        :type: DatetimeOffsetTransform
        """

        self._offset = offset

    @property
    def offset_column_value(self):
        """Gets the offset_column_value of this DatetimeTransform.  # noqa: E501


        :return: The offset_column_value of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeOffsetColumnValueTransform
        """
        return self._offset_column_value

    @offset_column_value.setter
    def offset_column_value(self, offset_column_value):
        """Sets the offset_column_value of this DatetimeTransform.


        :param offset_column_value: The offset_column_value of this DatetimeTransform.  # noqa: E501
        :type: DatetimeOffsetColumnValueTransform
        """

        self._offset_column_value = offset_column_value

    @property
    def offset_static_value(self):
        """Gets the offset_static_value of this DatetimeTransform.  # noqa: E501


        :return: The offset_static_value of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeOffsetStaticValueTransform
        """
        return self._offset_static_value

    @offset_static_value.setter
    def offset_static_value(self, offset_static_value):
        """Sets the offset_static_value of this DatetimeTransform.


        :param offset_static_value: The offset_static_value of this DatetimeTransform.  # noqa: E501
        :type: DatetimeOffsetStaticValueTransform
        """

        self._offset_static_value = offset_static_value

    @property
    def range(self):
        """Gets the range of this DatetimeTransform.  # noqa: E501


        :return: The range of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeRangeTransform
        """
        return self._range

    @range.setter
    def range(self, range):
        """Sets the range of this DatetimeTransform.


        :param range: The range of this DatetimeTransform.  # noqa: E501
        :type: DatetimeRangeTransform
        """

        self._range = range

    @property
    def select(self):
        """Gets the select of this DatetimeTransform.  # noqa: E501


        :return: The select of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeSelectTransform
        """
        return self._select

    @select.setter
    def select(self, select):
        """Sets the select of this DatetimeTransform.


        :param select: The select of this DatetimeTransform.  # noqa: E501
        :type: DatetimeSelectTransform
        """

        self._select = select

    @property
    def today(self):
        """Gets the today of this DatetimeTransform.  # noqa: E501


        :return: The today of this DatetimeTransform.  # noqa: E501
        :rtype: DatetimeCurrentDateTransform
        """
        return self._today

    @today.setter
    def today(self, today):
        """Sets the today of this DatetimeTransform.


        :param today: The today of this DatetimeTransform.  # noqa: E501
        :type: DatetimeCurrentDateTransform
        """

        self._today = today

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
        if not isinstance(other, DatetimeTransform):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
