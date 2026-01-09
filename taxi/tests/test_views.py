from urllib import response
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


INDEX_URL = reverse("taxi:index")

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[1])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[1])

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[1])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", args=[1])
CAR_DELETE_URL = reverse("taxi:car-delete", args=[1])
CAR_ASSIGN_URL = reverse("taxi:toggle-car-assign", args=[1])

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[1])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[1])


class PublicHomePageTest(TestCase):
    def test_home_login_require(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="test", country="test")

    def test_list_login_require(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_require(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_require(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_require(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(model="model", manufacturer_id=1)
        

    def test_list_login_require(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_login_require(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_require(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_require(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_require(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_assign_login_require(self):
        response = self.client.get(CAR_ASSIGN_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_user(username="user")

    def test_list_login_require(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_login_require(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_require(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_require(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_require(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        test_user = Driver.objects.create_user(
            username="test.user",
            password="pass321",
        )
        self.client.force_login(test_user)

        Driver.objects.create_user(
            username="joyce.byers",
            first_name="Joyce",
            last_name="Byers",
            license_number="JOY26458",
        )
        Driver.objects.create_user(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="JIM26531",
        )
        Driver.objects.create_user(
            username="dustin.henderson",
            first_name="Dustin",
            last_name="Henderson",
            license_number="DUS25131",
        )
        Driver.objects.create_user(
            username="nancy.wheeler",
            first_name="Nancy",
            last_name="Wheeler",
            license_number="NAN34131",
        )

    def test_form_license_update_validation(self):
        form_data = {
            "license_number": "LUK35131"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_search(self):
        drivers = Driver.objects.filter(username__icontains="dus")
        response = self.client.get(DRIVER_LIST_URL + "?username=dus")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
