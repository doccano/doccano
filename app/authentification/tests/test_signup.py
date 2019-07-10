from django.test import TestCase
from ..forms import SignupForm
from ..tokens import account_activation_token


class TestSignUp(TestCase):
    form_class = SignupForm

    def test_signup(self):

        form = self.form_class({
            'username': 'i_am_a_test_username',
            'email': 'i_am_a_test@email.com',
            'password1': 'fdsfdsfdssd232323&',
            'password2': 'fdsfdsfdssd232323&'
        })
        self.assertTrue(form.is_valid())
        user_saved = form.save()
        self.assertEqual(user_saved.username, 'i_am_a_test_username')
        self.assertEqual(user_saved.email, 'i_am_a_test@email.com')

        # I guess this is impossible to test password because it gets removed
        # after the form.save() execution
        # self.assertEqual(user_saved.password1, "fdsfdsfdssd232323&")
        # self.assertEqual(user_saved.password2, "fdsfdsfdssd232323&")

    def test_blank_signup(self):
        form = self.form_class({})
        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'email': ['This field is required.'],
            'password1': ['This field is required.'],
            'password2': ['This field is required.']
        })


class TestToken(TestCase):
    """test for token"""

    def test_valid_token(self):
        request_POST = {'username': 'username5645',
                        'email': 'email@example.com',
                        'password1': 'pwd000000',
                        'password2': 'pwd000000'}
        user = SignupForm(request_POST).save(commit=False)
        token = account_activation_token.make_token(user)
        self.assertTrue(isinstance(token, str))
