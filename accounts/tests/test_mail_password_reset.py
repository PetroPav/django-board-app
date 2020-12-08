from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

# Create your tests here.
class MailPasswordResetTests(TestCase):
    def setUp(self):
        self.email = 'jon@example.com'
        self.username = 'jon'
        User.objects.create_user(username=self.username, email=self.email, password='123abc')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email':self.email})
        self.mail = mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password', self.mail.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url ,self.mail.body)
        self.assertIn(self.username, self.mail.body)
        self.assertIn(self.email, self.mail.body)

    def test_email_to(self):
        self.assertEqual([self.email], self.mail.to)

