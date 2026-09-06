from requests.models import Product


class CreateProducts:
    def __init__(self):
        self.products = [
            {
                "code": "101",
                "name_en": "Wheat flour mixed with paste",
                "name_ar": "طحين معجون مطحون",
            },
            {
                "code": "102",
                "name_en": "Wheat flour mixed with sugar",
                "name_ar": "طحين معجون محلول",
            },
            {
                "code": "201",
                "name_en": "Wheat flour mixed with salt",
                "name_ar": "طحين معجون ملح",
            },
        ]

    def execute(self):
        print("Creating products...")
        for product in self.products:
            _, created = Product.objects.get_or_create(
                code=product["code"],
                defaults={
                    "name_en": product["name_en"],
                    "name_ar": product["name_ar"],
                },
            )
            if created:
                print(f"Product {product['code']} created successfully")
            else:
                print(f"Product {product['code']} already exists")
        print("Products created successfully")
