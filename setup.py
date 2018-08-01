#!/usr/bin/env python

from distutils.core import setup, Command



class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'test',
                'USER': 'test',
                'PASSWORD': 'test',
                'HOST': 'localhost'
            }},
            INSTALLED_APPS=('localized_text_field', 'django.contrib.contenttypes')
        )

        from django.core.management import call_command
        import django

        django.setup()
        call_command('test', 'localized_text_field')


setup(
    name="localized_text_field",
    version="0.1",
    description="Django based TextField class that supports localization",
    install_requires=[
        'django >= 1.8',
        'depocs == 1.0.0',
        'psycopg2',
    ],
    cmdclass={'test': TestCommand},
)

