from django.test import SimpleTestCase, TestCase, RequestFactory, override_settings
from django.http import HttpRequest
from ..views import SignupView
from django.conf import settings
from api.tests.test_config import setenv

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AddCSSTemplateTagTest(SimpleTestCase):

    def test_rendered(self):
        with setenv('ALLOW_SIGNUP', 'True'):
            request = HttpRequest()
            request.method = 'GET'
            needle = '<input type="password" name="password1" class=" input" required id="id_password1">'
            self.assertInHTML(needle, str(SignupView.as_view()(request, as_string=True).content))


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ViewsTest(SimpleTestCase):
    """Class for testing views"""

    def test_mail_not_set_up(self):
        with setenv('ALLOW_SIGNUP', 'True'):
            if hasattr(settings, 'EMAIL_HOST'):
                has_EMAIL_HOST = True
                EMAIL_HOST = settings.EMAIL_HOST
                delattr(settings, 'EMAIL_HOST')
            else:
                has_EMAIL_HOST = False

            if hasattr(settings, 'EMAIL_BACKEND'):
                has_EMAIL_BACKEND = True
                EMAIL_BACKEND = settings.EMAIL_BACKEND
                delattr(settings, 'EMAIL_BACKEND')
            else:
                has_EMAIL_BACKEND = False

            request = HttpRequest()
            request.method = 'POST'
            response = SignupView.as_view()(request, as_string=True)

            if has_EMAIL_HOST:
                settings.EMAIL_HOST = EMAIL_HOST
            if has_EMAIL_BACKEND:
                settings.EMAIL_BACKEND = EMAIL_BACKEND
            needle = "<span>has not set up any emails</span>"
            self.assertInHTML(needle, str(response.content))

    def test_signup_not_allowed(self):
        with setenv('ALLOW_SIGNUP', 'True'):
            ALLOW_SIGNUP = settings.ALLOW_SIGNUP
            settings.ALLOW_SIGNUP = False
            request = HttpRequest()
            request.method = 'POST'
            response = SignupView.as_view()(request, as_string=True)
            settings.ALLOW_SIGNUP = ALLOW_SIGNUP
            self.assertEqual(response.status_code, 302)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ViewsDBTest(TestCase):
    """Class for testing views with DB queries"""

    def test_form_submission(self):
        with setenv('ALLOW_SIGNUP', 'True'):
            self.factory = RequestFactory()
            if hasattr(settings, 'EMAIL_BACKEND'):
                EMAIL_BACKEND = settings.EMAIL_BACKEND
            else:
                EMAIL_BACKEND = False

            settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
            request = self.factory.post('/signup')
            request.POST = {'username': 'username5648',
                            'email': 'email@example.com',
                            'password1': 'pwd0000Y00$$',
                            'password2': 'pwd0000Y00$$'
                            }
            response = SignupView.as_view()(request)
            needle = '<span>emailed you instructions to activate your account</span>'
            if not EMAIL_BACKEND:
                delattr(settings, 'EMAIL_BACKEND')
            else:
                settings.EMAIL_BACKEND = EMAIL_BACKEND
            self.assertInHTML(needle, str(response.content))
