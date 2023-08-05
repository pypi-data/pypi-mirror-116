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


class PageTemplateUpdate(object):
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
        'dt_u': 'datetime',
        'name': 'str',
        'settings_spec': 'SettingsSpec',
        'template_body': 'str'
    }

    attribute_map = {
        'dt_u': 'dt_u',
        'name': 'name',
        'settings_spec': 'settings_spec',
        'template_body': 'template_body'
    }

    def __init__(self, dt_u=None, name=None, settings_spec=None, template_body=None):  # noqa: E501
        """PageTemplateUpdate - a model defined in OpenAPI"""  # noqa: E501

        self._dt_u = None
        self._name = None
        self._settings_spec = None
        self._template_body = None
        self.discriminator = None

        if dt_u is not None:
            self.dt_u = dt_u
        if name is not None:
            self.name = name
        self.settings_spec = settings_spec
        self.template_body = template_body

    @property
    def dt_u(self):
        """Gets the dt_u of this PageTemplateUpdate.  # noqa: E501


        :return: The dt_u of this PageTemplateUpdate.  # noqa: E501
        :rtype: datetime
        """
        return self._dt_u

    @dt_u.setter
    def dt_u(self, dt_u):
        """Sets the dt_u of this PageTemplateUpdate.


        :param dt_u: The dt_u of this PageTemplateUpdate.  # noqa: E501
        :type: datetime
        """

        self._dt_u = dt_u

    @property
    def name(self):
        """Gets the name of this PageTemplateUpdate.  # noqa: E501


        :return: The name of this PageTemplateUpdate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PageTemplateUpdate.


        :param name: The name of this PageTemplateUpdate.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def settings_spec(self):
        """Gets the settings_spec of this PageTemplateUpdate.  # noqa: E501


        :return: The settings_spec of this PageTemplateUpdate.  # noqa: E501
        :rtype: SettingsSpec
        """
        return self._settings_spec

    @settings_spec.setter
    def settings_spec(self, settings_spec):
        """Sets the settings_spec of this PageTemplateUpdate.


        :param settings_spec: The settings_spec of this PageTemplateUpdate.  # noqa: E501
        :type: SettingsSpec
        """
        if settings_spec is None:
            raise ValueError("Invalid value for `settings_spec`, must not be `None`")  # noqa: E501

        self._settings_spec = settings_spec

    @property
    def template_body(self):
        """Gets the template_body of this PageTemplateUpdate.  # noqa: E501


        :return: The template_body of this PageTemplateUpdate.  # noqa: E501
        :rtype: str
        """
        return self._template_body

    @template_body.setter
    def template_body(self, template_body):
        """Sets the template_body of this PageTemplateUpdate.


        :param template_body: The template_body of this PageTemplateUpdate.  # noqa: E501
        :type: str
        """
        if template_body is None:
            raise ValueError("Invalid value for `template_body`, must not be `None`")  # noqa: E501

        self._template_body = template_body

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
        if not isinstance(other, PageTemplateUpdate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
