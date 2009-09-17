import unittest
from localflavor.sl import forms
from django.forms import ValidationError

class TestEMSOField(unittest.TestCase):

	def test_is_valid(self):
		f = forms.EMSOField()
		
		valid_emso = '0205951500462'
		self.assertEqual(f.clean(valid_emso), valid_emso)
	
	def test_not_valid(self):
		f = forms.EMSOField()
		
		fail_emso = '0205951500463'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
	
	def test_too_wrong_length(self):
		f = forms.EMSOField()
		
		fail_emso = '020'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
		
		fail_emso = '020020595150046020595150046'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
	
	def test_not_integers(self):
		f = forms.EMSOField()
		
		fail_emso = 'aaaabbbbccccd'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
	
	def test_modulo_is_10(self):
		f = forms.EMSOField()
		
		fail_emso = '1010095500072'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
	
	def test_after_2000(self):
		f = forms.EMSOField()
		
		valid_emso = '2309002500068'
		self.assertEqual(f.clean(valid_emso), valid_emso)
	
	def test_is_valid_date_range(self):
		f = forms.EMSOField()
		
		fail_emso = '2020095500070'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
		fail_emso = '5050095500078'
		self.failUnlessRaises(ValidationError, f.clean, fail_emso)
