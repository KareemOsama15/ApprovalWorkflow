from workflow.models import Action


class CreateApprovalActions:
    APPROVAL_ACTIONS = [
        {
            "type": "approve",
            "name_en": "Approve",
            "name_ar": "موافقة",
        },
        {
            "type": "reject",
            "name_en": "Reject",
            "name_ar": "رفض",
        },
        {
            "type": "reassign_customer",
            "name_en": "Reassign Customer",
            "name_ar": "إعادة تعيين العميل",
        },
        {
            "type": "reassign_committee",
            "name_en": "Reassign Committee",
            "name_ar": "إعادة تعيين عضو لجنة الزيارة",
        },
        {
            "type": "reassign_technical",
            "name_en": "Reassign Technical",
            "name_ar": "إعادة تعيين عضو اللجنة الفنية",
        },
        {
            "type": "reassign_both_committees",
            "name_en": "Reassign Both Committees",
            "name_ar": "إعادة تعيين عضو لجنة الزيارة واللجنة الفنية",
        },
        {
            "type": "save_technical_form",
            "name_en": "Save Technical Form",
            "name_ar": "حفظ الاستمارة الفنية",
        },
        {
            "type": "save_committee_form",
            "name_en": "Save Committee Form",
            "name_ar": "حفظ استمارة لجنة الزيارة",
        },
        {
            "type": "reopen",
            "name_en": "Reopen",
            "name_ar": "إعادة فتح الطلب",
        },
        {
            "type": "assign_committee",
            "name_en": "Assign Committee",
            "name_ar": "تعيين عضو لجنة الزيارة",
        },
        {
            "type": "assign_technical",
            "name_en": "Assign Technical",
            "name_ar": "تعيين عضو لجنة الفنية",
        },
        {
            "type": "gfsa_action",
            "name_en": "GFSA Action",
            "name_ar": "إجراء من قبل GFSA",
        },
    ]

    def execute(self):
        print("Creating approval actions...")

        for approval_action in self.APPROVAL_ACTIONS:
            _, created = Action.objects.get_or_create(
                type=approval_action["type"],
                defaults={
                    "name_en": approval_action["name_en"],
                    "name_ar": approval_action["name_ar"],
                },
            )
            if created:
                print(
                    f"Approval action {approval_action['name_en']} created successfully"
                )

        print("All approval actions created successfully..")
