from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

import unittest2 as unittest
from netfields import rest_framework as fields


class FieldsTestCase(unittest.TestCase):
    def test_validation_inet_field(self):

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField()

        address = '10.0.0.'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['ip'],
                         ["Invalid IP address: %r does not appear to be an IPv4 or IPv6 interface" % address])


    def test_validation_cidr_field(self):

        class TestSerializer(serializers.Serializer):
            cidr = fields.CidrAddressField()

        address = '10.0.0.'
        serializer = TestSerializer(data={'cidr': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['cidr'],
                         ["Invalid CIDR address: %r does not appear to be an IPv4 or IPv6 network" % address])

    def test_validation_mac_field(self):

        class TestSerializer(serializers.Serializer):
            mac = fields.MACAddressField()

        address = 'de:'
        serializer = TestSerializer(data={'mac': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(e.exception.detail['mac'], ["Invalid MAC address: failed to detect EUI version: %r" % address])

    def test_validation_additional_validators(self):
        def validate(value):
            raise serializers.ValidationError('Invalid.')

        class TestSerializer(serializers.Serializer):
            ip = fields.InetAddressField(validators=[validate])

        address = 'de:'
        serializer = TestSerializer(data={'ip': address})
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)
        self.assertItemsEqual(e.exception.detail['ip'],
                              ["Invalid IP address: %r does not appear to be an IPv4 or IPv6 interface" % address,
                               'Invalid.'])
