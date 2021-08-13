from .test_setup import TestSetUp
from ..models import Account


class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data,
                               format='json')
        self.assertEqual(res.status_code, 201)

    def test_logged_verified(self):
        """Test to see if the user can log if not verified"""
        self.client.post(self.register_url, self.user_data,
                         format='json')
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_logged_after_verified(self):
        """Test to see if the user can log if  verified"""
        response = self.client.post(self.register_url, self.user_data,
                                    format='json')

        email = response.data['email']
        user = Account.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

    def test_get_user_profile(self):
        """Test email verification"""
        response = self.client.post(self.register_url, self.user_data,
                                    format='json')
        email = response.data['email']
        user = Account.objects.get(email=email)
        user.is_verified = True
        user.save()
        response1 = self.client.post(self.login_url, self.user_data, format="json")
        tokens = response1.data['tokens']['access'][0]
        acces_token = tokens[1]
        import pdb
        pdb.set_trace()
