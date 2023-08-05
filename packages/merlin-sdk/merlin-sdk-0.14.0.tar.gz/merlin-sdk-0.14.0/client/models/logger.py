# coding: utf-8

"""
    Merlin

    API Guide for accessing Merlin's model management, deployment, and serving functionalities  # noqa: E501

    OpenAPI spec version: 0.14.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from client.configuration import Configuration


class Logger(object):
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
        'model': 'LoggerConfig',
        'transformer': 'LoggerConfig'
    }

    attribute_map = {
        'model': 'model',
        'transformer': 'transformer'
    }

    def __init__(self, model=None, transformer=None, _configuration=None):  # noqa: E501
        """Logger - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._model = None
        self._transformer = None
        self.discriminator = None

        if model is not None:
            self.model = model
        if transformer is not None:
            self.transformer = transformer

    @property
    def model(self):
        """Gets the model of this Logger.  # noqa: E501


        :return: The model of this Logger.  # noqa: E501
        :rtype: LoggerConfig
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this Logger.


        :param model: The model of this Logger.  # noqa: E501
        :type: LoggerConfig
        """

        self._model = model

    @property
    def transformer(self):
        """Gets the transformer of this Logger.  # noqa: E501


        :return: The transformer of this Logger.  # noqa: E501
        :rtype: LoggerConfig
        """
        return self._transformer

    @transformer.setter
    def transformer(self, transformer):
        """Sets the transformer of this Logger.


        :param transformer: The transformer of this Logger.  # noqa: E501
        :type: LoggerConfig
        """

        self._transformer = transformer

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
        if issubclass(Logger, dict):
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
        if not isinstance(other, Logger):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Logger):
            return True

        return self.to_dict() != other.to_dict()
