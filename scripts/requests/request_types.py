from requests.models import RequestType, RequestSequence


class CreateRequestTypes:

    REQUEST_TYPES = [
        {
            "code": "JOIN_REQUEST",
            "name_en": "Join Request",
            "name_ar": "طلب الانضمام",
        },
        {
            "code": "UPDATE_PRODUCT_REQUEST",
            "name_en": "Update Product Request",
            "name_ar": "طلب تحديث المنتج",
        },
        {
            "code": "CUSTOMER_CHANGE_INFO",
            "name_en": "Customer Change Information",
            "name_ar": "طلب تحديث بيانات العميل",
        },
        {
            "code": "INCREASE_PRODUCT_REQUEST",
            "name_en": "Increase Product Quantity Request",
            "name_ar": "طلب زيادة كمية المنتج",
        },
    ]

    def execute(self):
        print("Creating request types...")
        for request_type in self.REQUEST_TYPES:
            _, created = RequestType.objects.get_or_create(
                code=request_type["code"],
                defaults={
                    "name_en": request_type["name_en"],
                    "name_ar": request_type["name_ar"],
                },
            )
            if created:
                print(f"Request type {request_type['name_en']} created successfully")

        print("All Request types created successfully..")
        self._create_request_sequence()

    def _create_request_sequence(self):
        print("Creating request sequence...")
        RequestSequence.objects.create(sequence=1)
        print("Request sequence created successfully..")
