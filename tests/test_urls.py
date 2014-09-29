# -*- coding: utf-8 -*-
"""Tests for ``gen_url``."""
from fauxfactory import (
    gen_alpha,
    gen_alphanumeric,
    gen_cjk,
    gen_url,
)
from fauxfactory.constants import SCHEMES
import random
import sys
import unittest
# (too-many-public-methods) pylint:disable=R0904


class GenUrlTestCase(unittest.TestCase):
    """Call ``gen_url`` and provide a variety of arguments."""

    def test_unicode(self):
        """Check whether ``gen_url`` returns a unicode string."""
        url = gen_url()
        if sys.version_info[0] is 2:
            # (undefined-variable) pylint:disable=E0602
            self.assertIsInstance(url, unicode)  # flake8:noqa
        else:
            self.assertIsInstance(url, str)

    def test_no_arguments(self):
        """Provide no arguments.

        Assert that the generated URL's scheme is a value from ``SCHEMES``.

        """
        for _ in range(10):
            self.assertIn(gen_url().split(':')[0], SCHEMES)

    def test_valid_scheme(self):
        """Provide a value for the ``scheme`` argument.

        Assert that the generated URL contains the given scheme in the correct
        location.

        """
        for scheme in ('http', 'https', 'ftp', 'telnet', 'dummy'):
            self.assertEqual(gen_url(scheme=scheme).split(':')[0], scheme)

    def test_invalid_scheme(self):
        """Provide an invalid value for the ``scheme`` argument.

        Assert that a ``ValueError`` is raised.

        """
        for scheme in ('', ' ', gen_cjk()):
            with self.assertRaises(ValueError):
                gen_url(scheme=scheme)

    def test_valid_subdomain(self):
        """Provide a value for the ``subdomain`` argument.

        Assert that the generated URL contains the given scheme in the correct
        location.

        """
        for _ in range(10):
            subdomain = gen_alphanumeric()
            self.assertEqual(
                gen_url(subdomain=subdomain).split('//')[1].split('.')[0],
                subdomain
            )

    def test_invalid_subdomain(self):
        """Provide an invalid value for the ``subdomain`` argument.

        Assert that a ``ValueError`` is raised.

        """
        for subdomain in ('', ' ', gen_cjk()):
            with self.assertRaises(ValueError):
                gen_url(subdomain=subdomain)

    def test_valid_tld(self):
        """Provide a valid value for the ``tld`` argument.

        Assert that the generated URL contains the given scheme in the correct
        location. Provide the same value to both the ``tld`` and deprecated
        ``tlds`` argument.

        """
        for _ in range(10):
            tld = gen_alpha(length=random.randint(1, 10))
            self.assertEqual(gen_url(tld=tld).split('.')[-1], tld)
            self.assertEqual(gen_url(tlds=tld).split('.')[-1], tld)

    def test_invalid_tld(self):
        """Provide an invalid value for the ``tld`` argument.

        Assert that a ``ValueError`` is raised. Provide the same value to both
        the ``tld`` and deprecated ``tlds`` argument.

        """
        for tld in ('', ' ', gen_cjk()):
            with self.assertRaises(ValueError):
                gen_url(tld=tld)
            with self.assertRaises(ValueError):
                gen_url(tlds=tld)

    def test_tld_and_tlds(self):
        """Provide a value for both ``tld`` and ``tlds``.

        Assert that a ``ValueError`` is raised.

        """
        with self.assertRaises(ValueError):
            gen_url(tld='foo', tlds='bar')
