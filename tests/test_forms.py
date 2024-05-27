import unittest

from base_test import BaseTestCase

from app.forms.default_form import DefaultForm
from app.forms.login_form import LoginForm
from app.forms.profile_form import ProfileForm
from app.forms.register_form import RegisterForm
from app.forms.user_form import UserForm

# ==============================================================================================================
class Test_Default_Form(BaseTestCase):

    def test_validate_success_form(self):
        '''
        Tests the input for the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': '2024-05-23',
            'message': 'This is a test message from the unit testing.'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_validate_invalid_date_format_form(self):
        '''
        Test for invlid date inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': '23-05-2024',
            'message': 'The invalid date is reversed.'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_validate_invalid_date_form(self):
        '''
        Test for invlid date inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'date': 'NOT A DATE',
            'message': 'The invalid date is not a date!'
        })
        self.assertFalse(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_validate_no_date_form(self):
        '''
        Test for no date inputs into the default form
        '''
        form = DefaultForm(data={
            'name': 'Test User',
            'message': 'There is no date!'
        })
        self.assertTrue(form.validate())

    #-----------------------------------------------------------------------------------------------------------
    def test_validate_no_name_form(self):
        '''
        Test for absent name input into the default form
        '''
        form = DefaultForm(data={
            'date': '2024-05-23',
            'message': 'There is no name!'
        })
        self.assertFalse(form.validate())
    
    #-----------------------------------------------------------------------------------------------------------
    def test_validate_long_message(self):
        '''
        Test for invlid message inputs into the default form
        '''
        long_message = 'A' * 1002

        form = DefaultForm(data={
            'name': 'Test User',
            'date': '2024-05-23',
            'message': long_message
        })
        self.assertFalse(form.validate())

# ==============================================================================================================

if __name__ == "__main__":
    unittest.main()