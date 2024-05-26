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
        form = DefaultForm(
            name='Test User',
            date='2024-05-23',
            message='This is a test message from the unit testing.'
        )
        self.assertTrue(form.validate())


if __name__ == "__main__":
    unittest.main()