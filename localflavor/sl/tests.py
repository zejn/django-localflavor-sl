import unittest
from localflavor.sl import forms
from django.forms import ValidationError

class TestSITaxNumber(unittest.TestCase):

	def test_is_valid(self):
		f = forms.SITaxNumber()
		
		valid_taxnum = '15012557'
		self.assertEqual(f.clean(valid_taxnum), valid_taxnum)
	
	def test_modulo_is_1(self):
		f = forms.SITaxNumber()
		
		valid_taxnum = '22111310'
		self.assertEqual(f.clean(valid_taxnum), valid_taxnum)
	
	def test_modulo_is_0(self):
		f = forms.SITaxNumber()
		
		fail_taxnum = '22241310'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)
	
	def test_not_valid(self):
		f = forms.SITaxNumber()
		
		fail_taxnum = '15012558'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)
	
	def test_wrong_length(self):
		f = forms.SITaxNumber()
		
		fail_taxnum = '1501'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)
		
		fail_taxnum = '1501123123123'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)
	
	def test_not_integers(self):
		f = forms.SITaxNumber()
		
		fail_taxnum = 'abcdabcd'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)
	
	def test_starts_with_zero(self):
		f = forms.SITaxNumber()
		
		fail_taxnum = '01234579'
		self.failUnlessRaises(ValidationError, f.clean, fail_taxnum)

class TestEMSOField(unittest.TestCase):

    def test_is_valid(self):
        f = forms.EMSOField()
        
        valid_emso = '0205951500462'
        self.assertEqual(f.clean(valid_emso), valid_emso)
    
    def test_not_valid(self):
        f = forms.EMSOField()
        
        fail_emso = '0205951500463'
        self.failUnlessRaises(ValidationError, f.clean, fail_emso)
    
    def test_wrong_length(self):
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


class TestSLPhoneNumberField(unittest.TestCase):
    valid_numbers = {
        '+38640999999': '40999999',
        '+3861999999': '1999999',
        '0038640999999': '40999999',
        '040999999': '40999999',
        '01999999': '1999999',
        '059099999': '59099999',
    }
    invalid_numbers = [
        '03861999999',
        '3861999999',
    ]

    def test_valid_numbers(self):
        f = forms.SLPhoneNumberField()
        
        for key, value in self.valid_numbers.iteritems():
            output = f.clean(key)
            self.assertEqual(output, value)

    def test_invalid_numbers(self):
        f = forms.SLPhoneNumberField()
        
        for value in self.invalid_numbers:
            self.assertRaises(ValidationError, f.clean, value)
