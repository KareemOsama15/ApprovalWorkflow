from requests.models import CustomerCategory, Customer
import random


class CreateCustomerCategory:

    CUSTOMER_CATEGORIES = [
        {
            "code": 1,
            "name_en": "Direct Customer",
            "name_ar": "عميل مباشر",
        },
        {
            "code": 2,
            "name_en": "Distributor Customer",
            "name_ar": "عميل التوزيع",
        },
        {
            "code": 3,
            "name_en": "Multi-Branch Customer",
            "name_ar": "عميل متعدد الفروع",
        },
        {
            "code": 4,
            "name_en": "Beneficiary Customer",
            "name_ar": "عميل المستفيد",
        },
    ]

    def execute(self):
        print("Creating customer categories...")
        for customer_category in self.CUSTOMER_CATEGORIES:
            _, created = CustomerCategory.objects.get_or_create(
                code=customer_category["code"],
                defaults={
                    "name_ar": customer_category["name_ar"],
                    "name_en": customer_category["name_en"],
                },
            )
            if created:
                print(
                    f"Customer category {customer_category['name_en']} created successfully"
                )
        print("All customer categories created successfully..")

        self._create_dummy_customers()

    def _create_dummy_customers(self):
        print("Creating dummy customers...")
        for i in range(10):
            id_number = random.randint(1234567890, 9999999999)
            category = CustomerCategory.objects.get(code=random.randint(1, 4))
            Customer.objects.create(
                name_en=f"Customer Name {i}",
                name_ar=f"اسم العميل {i}",
                id_number=id_number,
                category=category,
            )
        print("All dummy customers created successfully..")
