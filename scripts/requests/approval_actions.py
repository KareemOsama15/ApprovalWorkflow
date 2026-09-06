from requests.models import Action, ActionType


class CreateApprovalActions:
    APPROVAL_ACTIONS = [
        {
            "type": ActionType.APPROVE,
            "name_en": "Approve",
            "name_ar": "موافقة",
        },
        {
            "type": ActionType.REJECT,
            "name_en": "Reject",
            "name_ar": "رفض",
        },
        {
            "type": ActionType.REASSIGN_CUSTOMER,
            "name_en": "Reassign Customer",
            "name_ar": "إعادة تعيين العميل",
        },
        {
            "type": ActionType.REASSIGN_COMMITTEE,
            "name_en": "Reassign Committee",
            "name_ar": "إعادة تعيين عضو لجنة الزيارة",
        },
        {
            "type": ActionType.REASSIGN_TECHNICAL,
            "name_en": "Reassign Technical",
            "name_ar": "إعادة تعيين عضو اللجنة الفنية",
        },
        {
            "type": ActionType.REASSIGN_BOTH_COMMITTEES,
            "name_en": "Reassign Both Committees",
            "name_ar": "إعادة تعيين عضو لجنة الزيارة واللجنة الفنية",
        },
        {
            "type": ActionType.SAVE_TECHNICAL_FORM,
            "name_en": "Save Technical Form",
            "name_ar": "حفظ الاستمارة الفنية",
        },
        {
            "type": ActionType.SAVE_COMMITTEE_FORM,
            "name_en": "Save Committee Form",
            "name_ar": "حفظ استمارة لجنة الزيارة",
        },
        {
            "type": ActionType.REOPEN,
            "name_en": "Reopen",
            "name_ar": "إعادة فتح الطلب",
        },
        {
            "type": ActionType.ASSIGN_COMMITTEE,
            "name_en": "Assign Committee",
            "name_ar": "تعيين عضو لجنة الزيارة",
        },
        {
            "type": ActionType.ASSIGN_TECHNICAL,
            "name_en": "Assign Technical",
            "name_ar": "تعيين عضو لجنة الفنية",
        },
        {
            "type": ActionType.GFSA_ACTION,
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
