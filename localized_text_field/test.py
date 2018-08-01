from django.db import models
from django.test import TestCase

from localized_text_field import LocalizedTextField, LocaleContext

class LocalizationTestClass(models.Model):
    hello = LocalizedTextField()

    class Meta(object):
        app_label='localized_text_field'

class LocalizedTextFieldTests(TestCase):

    def setUp(self):
        self.model = LocalizationTestClass.objects.create()

    def test_edit_text_without_locale(self):
        default_text = "Hello World!"
        self.model.hello = default_text
        self.assertEqual(self.model.hello, default_text)

        self.model.save()
        model = LocalizationTestClass.objects.get(id=self.model.id)
        self.assertEqual(model.hello, default_text)

    def test_edit_text_in_locale(self):
        english_text = "Hello World!"
        french_text = "Bonjour tout les monde"

        with LocaleContext('en-ca'):
            self.model.hello = english_text

        with LocaleContext('fr-ca'):
            self.model.hello = french_text

        self.model.save()
        model = LocalizationTestClass.objects.get(id=self.model.id)
        with LocaleContext('en-ca'):
            self.assertEqual(model.hello, english_text)
        with LocaleContext('fr-ca'):
            self.assertEqual(model.hello, french_text)

