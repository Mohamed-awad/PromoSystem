from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.utils import timezone
from promoApplication.models import Promo, User


class PromoAPITestCase(APITestCase):
    def setUp(self):
        # create admin user
        admin_obj = User(username="test_admin", email="test_admin@test.com", is_admin=True)
        admin_obj.set_password("test_admin_password")
        admin_obj.save()
        # create norml user
        user_obj = User(username="test_user", email="test_user@test.com", is_admin=False)
        user_obj.set_password("test_user_password")
        user_obj.save()

        # create promo for normal user
        promo_obj = Promo(
            promo_type="fkm",
            promo_code="125kju",
            promo_amount=50,
            user=user_obj,
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        promo_obj.save()

    def test_admin_login_and_create_promo(self):
        data = {
            'username': 'test_admin',
            'password': 'test_admin_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            normal_user = User.objects.filter(username='test_user')[0]
            data = {
                "user": normal_user.pk,
                "promo_type": "vgg",
                "promo_code": "152kij",
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "promo_amount": 76,
                "is_active": False,
                "description": "fff"
            }
            url = api_reverse('api-promo:create-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_login_and_create_promo(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            normal_user = User.objects.filter(username='test_user')[0]
            data = {
                "user": normal_user.pk,
                "promo_type": "vgg",
                "promo_code": "152kij",
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "promo_amount": 76,
                "is_active": False,
                "description": "fff"
            }
            url = api_reverse('api-promo:create-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_promos_without_login(self):
        url = api_reverse('api-promo:list-promo')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_promos_with_admin_login(self):
        data = {
            'username': 'test_admin',
            'password': 'test_admin_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:list-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_promos_with_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:list-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_promo_point_with_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-use-promo-points',  kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_use_promo_point_with_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-use-promo-points',  kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            data = {
                "deducted_points": 1
            }
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_promo_with_admin_login(self):
        data = {
            'username': 'test_admin',
            'password': 'test_admin_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-update-delete-promo', kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            data = {
                "user": 2,
                "promo_type": "vgg",
                "promo_code": "15kill",
                "created_at": "2020-10-02T21:45:42.641576Z",
                "start_time": "2020-09-10T05:58:00Z",
                "end_time": "2020-09-16T07:56:00Z",
                "promo_amount": 15,
                "is_active": False,
                "description": "fff"
            }
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_promo_with_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-update-delete-promo', kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            data = {
                "user": 2,
                "promo_type": "vgg",
                "promo_code": "15kill",
                "created_at": "2020-10-02T21:45:42.641576Z",
                "start_time": "2020-09-10T05:58:00Z",
                "end_time": "2020-09-16T07:56:00Z",
                "promo_amount": 15,
                "is_active": False,
                "description": "fff"
            }
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_promo_with_admin_login(self):
        data = {
            'username': 'test_admin',
            'password': 'test_admin_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-update-delete-promo', kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.delete(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_promo_with_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_user_password'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:get-update-delete-promo', kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # JWT <token>
            response = self.client.delete(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_signup_for_normal_user(self):
        data = {
            'username': 'test_normal_user',
            'password': 'test_normal_password'
        }
        url = api_reverse("api-signup")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_for_normal_user_with_username_exist(self):
        data = {
            'username': 'test_normal_user',
            'password': 'test_normal_password'
        }
        url = api_reverse("api-signup")
        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
