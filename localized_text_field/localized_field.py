from django.contrib.postgres.fields import JSONField

from depocs import Scoped

class LocaleContext(Scoped):
    """
    Context object for setting a locale. When used as a Context manager, any
    access of a LocalizedTextField within will return and modify the value
    indicated by the value set by the locale.
    """

    def __init__(self, locale):
        self.locale = locale

class LocalizedTextFieldDescriptor(object):
    """
    Descriptor for accessing the LocalizedTextField as if it was a TextField
    and not a JSON dict holding multiple text representations. It uses the
    current LocaleContext to determine what the correct locale is, and falls
    back to the default locale if no text exists for the request locale.
    """

    def __init__(self, name, default_locale):
        self.name = name
        self.default_locale = default_locale

    def get_text_for_locale(self, instance, locale):
        try:
            text_lookup = instance.__dict__[self.name]
        except KeyError:
            text_lookup = instance.__dict__[self.name] = {}
        value = text_lookup.get(locale, None)
        return value

    def set_text_for_locale(self, instance, locale, value):
        try:
            text_lookup = instance.__dict__[self.name]
        except KeyError:
            text_lookup = instance.__dict__[self.name] = {}
        text_lookup[locale] = value

    def get_locale(self):
        try:
            locale = LocaleContext.current.locale
        except LocaleContext.Missing:
            locale = self.default_locale
        return locale

    def __get__(self, instance, owner):
        if instance is None:
            return self

        locale = self.get_locale()
        value = self.get_text_for_locale(instance, locale)

        # If nothing exists for the given locale, fallback to the default locale
        if value is None:
            value = self.get_text_for_locale(instance, self.default_locale)

        return value

    def __set__(self, instance, value):
        # If we're loading from the DB, we're getting set with the full dict
        # directly
        if isinstance(value, dict):
            instance.__dict__[self.name] = value
        else:
            locale = self.get_locale()
            self.set_text_for_locale(instance, locale, value)


class LocalizedTextField(JSONField):
    """

    """

    def __init__(self, *args, **kwargs):
        """

        """

        self.default_locale = kwargs.pop('default_locale', 'en-us')
        default_value = kwargs.pop('default', None)
        if default_value:
            kwargs['default'] = {self.default_locale: default_value}
        super(LocalizedTextField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        """
        Adds a LocalizedTextFieldDescriptor to manage accessing text by locale
        """
        super(LocalizedTextField, self).contribute_to_class(cls, name)

        descriptor = LocalizedTextFieldDescriptor(self.name, self.default_locale)
        setattr(cls, self.name, descriptor)

    def pre_save(self, instance, add):
        """
        Override pre_save to sidestep the descriptor we added
        """
        return instance.__dict__[self.name]
