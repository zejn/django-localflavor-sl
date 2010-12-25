import datetime
import re

from django.forms.fields import CharField, Select, ChoiceField
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from sl_postalcodes import SL_POSTALCODES


sorted_sl_postalcodes = sorted(SL_POSTALCODES, key=lambda k: k[1])

class EMSOField(CharField):
    """A form for validating Slovenian personal identification number.

    Additionally stores gender and birthday to self.info dictionary.
    """

    default_error_messages = {
        'invalid': _(u'Enter a valid personal identification number.'),
    }
    emso_regex = re.compile('^([0-3][0-9])([01][0-9])(\d{3})(\d{2})(\d{3})(\d)$')

    def clean(self, value):
        value = value.strip()
        if len(value) != 13:
            raise ValidationError(self.default_error_messages['invalid'])
        
        m  = self.emso_regex.match(value)
        if m is None:
            raise ValidationError(self.default_error_messages['invalid'])

        # validation
        s = 0
        int_values = [int(i) for i in value]
        for a, b in zip(int_values, range(7, 1, -1) * 2):
            s += a * b
        chk = s % 11
        if chk == 10:
            raise ValidationError(self.default_error_messages['invalid'])
        if int_values[-1] != 11 - chk:
            raise ValidationError(self.default_error_messages['invalid'])

        # extract info
        d = [int(i) for i in m.groups()]
        year = d[2] + 1000
        if year < 1700:
            year += 1000
        birthdate = datetime.date(year, d[1], d[0])
        gender = d[4] < 500 and 'male' or 'female'

        self.info = {'gender': gender, 'birthdate': birthdate}
        return value

class SLTaxNumber(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid tax number in form SIXXXXXXXX'),
    }
    sitax_regex = re.compile('^[1-9]\d{6}\d$')
    
    def clean(self, value):
        value = value.strip()
        if len(value) != 8:
            raise ValidationError(self.default_error_messages['invalid'])
        
        s = 0
        try:
            int_values = [int(i) for i in value]
        except ValueError:
            raise ValidationError(self.default_error_messages['invalid'])
        for a,b in zip(int_values, range(8,1,-1)):
            s += a*b
        chk = 11 - (s % 11)
        if chk == 11:
            raise ValidationError(self.default_error_messages['invalid'])
        if chk == 10:
            chk = 0

        if int_values[-1] != chk:
            raise ValidationError(self.default_error_messages['invalid'])

        return value


class SLPostalCodeField(ChoiceField):
    """Slovenian post codes field.
    
    Provides a sorted choice field of major post codes.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', sorted_sl_postalcodes)
        super(SLPostalCodeField, self).__init__(*args, **kwargs)


class SLPhoneNumberField(CharField):
    """Slovenian phone number field.

    Must have atleast local area code.
    Country code can be present.

    Examples:

    * +38640XXXXXX
    * 0038640XXXXXX
    * 040XXXXXX
    * 01XXXXXX
    * 0590XXXXX

    """

    default_error_messages = {
        'invalid': _(u'Enter phone number in form +386XXXXXXXX or 0XXXXXXXX.'),
    }
    phone_regex = re.compile('^(?:(?:00|\+)386|0)(\d{7,8})$')

    def clean(self, value):
        m = self.phone_regex.match(value.strip())
        if m is None:
            raise ValidationError(self.default_error_messages['invalid'])
        
        
        return value

class SLPostalCodeSelectWidget(Select):
    """Slovenian post codes select widget.
    
    Provides a sorted choice field of major post codes.
    """
    def __init__(self, attrs=None):
        super(SLPostalCodeSelectWidget, self).__init__(attrs,
            choices=sorted_sl_postalcodes)
