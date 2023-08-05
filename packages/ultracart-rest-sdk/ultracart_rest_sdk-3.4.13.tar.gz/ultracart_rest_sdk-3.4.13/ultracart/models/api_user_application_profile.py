# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ApiUserApplicationProfile(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'api_application_logo_url': 'str',
        'application_description': 'str',
        'application_name': 'str',
        'developer_name': 'str',
        'developer_website': 'str'
    }

    attribute_map = {
        'api_application_logo_url': 'api_application_logo_url',
        'application_description': 'application_description',
        'application_name': 'application_name',
        'developer_name': 'developer_name',
        'developer_website': 'developer_website'
    }

    def __init__(self, api_application_logo_url=None, application_description=None, application_name=None, developer_name=None, developer_website=None):  # noqa: E501
        """ApiUserApplicationProfile - a model defined in Swagger"""  # noqa: E501

        self._api_application_logo_url = None
        self._application_description = None
        self._application_name = None
        self._developer_name = None
        self._developer_website = None
        self.discriminator = None

        if api_application_logo_url is not None:
            self.api_application_logo_url = api_application_logo_url
        if application_description is not None:
            self.application_description = application_description
        if application_name is not None:
            self.application_name = application_name
        if developer_name is not None:
            self.developer_name = developer_name
        if developer_website is not None:
            self.developer_website = developer_website

    @property
    def api_application_logo_url(self):
        """Gets the api_application_logo_url of this ApiUserApplicationProfile.  # noqa: E501

        Application logo URL  # noqa: E501

        :return: The api_application_logo_url of this ApiUserApplicationProfile.  # noqa: E501
        :rtype: str
        """
        return self._api_application_logo_url

    @api_application_logo_url.setter
    def api_application_logo_url(self, api_application_logo_url):
        """Sets the api_application_logo_url of this ApiUserApplicationProfile.

        Application logo URL  # noqa: E501

        :param api_application_logo_url: The api_application_logo_url of this ApiUserApplicationProfile.  # noqa: E501
        :type: str
        """

        self._api_application_logo_url = api_application_logo_url

    @property
    def application_description(self):
        """Gets the application_description of this ApiUserApplicationProfile.  # noqa: E501

        Application description  # noqa: E501

        :return: The application_description of this ApiUserApplicationProfile.  # noqa: E501
        :rtype: str
        """
        return self._application_description

    @application_description.setter
    def application_description(self, application_description):
        """Sets the application_description of this ApiUserApplicationProfile.

        Application description  # noqa: E501

        :param application_description: The application_description of this ApiUserApplicationProfile.  # noqa: E501
        :type: str
        """

        self._application_description = application_description

    @property
    def application_name(self):
        """Gets the application_name of this ApiUserApplicationProfile.  # noqa: E501

        Application name  # noqa: E501

        :return: The application_name of this ApiUserApplicationProfile.  # noqa: E501
        :rtype: str
        """
        return self._application_name

    @application_name.setter
    def application_name(self, application_name):
        """Sets the application_name of this ApiUserApplicationProfile.

        Application name  # noqa: E501

        :param application_name: The application_name of this ApiUserApplicationProfile.  # noqa: E501
        :type: str
        """

        self._application_name = application_name

    @property
    def developer_name(self):
        """Gets the developer_name of this ApiUserApplicationProfile.  # noqa: E501

        Developer name  # noqa: E501

        :return: The developer_name of this ApiUserApplicationProfile.  # noqa: E501
        :rtype: str
        """
        return self._developer_name

    @developer_name.setter
    def developer_name(self, developer_name):
        """Sets the developer_name of this ApiUserApplicationProfile.

        Developer name  # noqa: E501

        :param developer_name: The developer_name of this ApiUserApplicationProfile.  # noqa: E501
        :type: str
        """

        self._developer_name = developer_name

    @property
    def developer_website(self):
        """Gets the developer_website of this ApiUserApplicationProfile.  # noqa: E501

        Developer website  # noqa: E501

        :return: The developer_website of this ApiUserApplicationProfile.  # noqa: E501
        :rtype: str
        """
        return self._developer_website

    @developer_website.setter
    def developer_website(self, developer_website):
        """Sets the developer_website of this ApiUserApplicationProfile.

        Developer website  # noqa: E501

        :param developer_website: The developer_website of this ApiUserApplicationProfile.  # noqa: E501
        :type: str
        """

        self._developer_website = developer_website

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(ApiUserApplicationProfile, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiUserApplicationProfile):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
