import datetime
import re

from django.forms.fields import CharField, Select
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

class EMSOField(CharField):
	"""
	A form for validating Slovenian personal identification number.
	"""
	
	default_error_messages = {
		'invalid': _(u'Enter a valid personal identification number.'),
	}
	emso_regex = re.compile('^([0-3][0-9])([01][0-9])(\d{3})(\d{2})(\d{3})(\d)$')
	
	def clean(self, value):
		value = value.strip()
		print value
		if len(value) != 13:
			raise ValidationError(self.default_error_messages['invalid'])
		
		s = 0
		try:
			int_values = [int(i) for i in value]
		except ValueError:
			raise ValidationError(self.default_error_messages['invalid'])
		for a,b in zip(int_values, range(7,1,-1)*2):
			s += a*b
		chk = s % 11
		if chk == 10:
			raise ValidationError(self.default_error_messages['invalid'])
		if int_values[-1] != 11 - chk:
			raise ValidationError(self.default_error_messages['invalid'])
		
		m = self.emso_regex.match(value)
		if m is None:
			raise ValidationError(self.default_error_messages['invalid'])
		d = [int(i) for i in m.groups()]
		year = d[2] + 1000
		if year < 1700:
			year += 1000
		birthdate = datetime.date(year, d[1], d[0])
		
		gender = d[4] < 500 and 'male' or 'female'
		
		self.info = {'gender': gender, 'birthdate': birthdate}

