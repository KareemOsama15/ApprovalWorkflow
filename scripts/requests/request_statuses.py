from requests.models import RequestStatus


class CreateRequestStatuses:
    REQUEST_STATUSES = [
        {
            "code": 1,
            "name_en": "New",
            "name_ar": "جديد",
        },
        {
            "code": 3,
            "name_en": "Under Processing",
            "name_ar": "قيد المراجعة لأعضاء اللجان",
        },
        {
            "code": 5,
            "name_en": "Delayed",
            "name_ar": "مؤجل",
        },
        {
            "code": 7,
            "name_en": "Approved",
            "name_ar": "مقبول",
        },
        {
            "code": 9,
            "name_en": "Rejected",
            "name_ar": "مرفوض من جفسا",
        },
        {
            "code": 10,
            "name_en": "Branch Manager",
            "name_ar": "مدير الفرع",
        },
        {
            "code": 11,
            "name_en": "Sales Manager",
            "name_ar": "مدير المبيعات",
        },
        {
            "code": 13,
            "name_en": "CEO",
            "name_ar": "رئيس مجلس الإدارة",
        },
        {
            "code": 14,
            "name_en": "GFSA For Review",
            "name_ar": "للمراجعة من قبل GFSA",
        },
        {
            "code": 15,
            "name_en": "Complete Data",
            "name_ar": "إستكمال البيانات",
        },
        {
            "code": 16,
            "name_en": "Rejected By Company",
            "name_ar": "مرفوض من قبل الشركة",
        },
        {
            "code": 98,
            "name_en": "Reassign Customer",
            "name_ar": "إعادة تعيين العميل",
        },
        {
            "code": 99,
            "name_en": "Reassign",
            "name_ar": "إعادة التعيين",
        },
    ]

    def execute(self):
        print("Creating request statuses...")

        for request_status in self.REQUEST_STATUSES:
            _, created = RequestStatus.objects.get_or_create(
                code=request_status["code"],
                defaults={
                    "name_en": request_status["name_en"],
                    "name_ar": request_status["name_ar"],
                },
            )
            if created:
                print(
                    f"Request status {request_status['name_en']} created successfully"
                )

        print("All request statuses created successfully..")
