from workflow.models import Action
from rest_framework.exceptions import ValidationError


class ActionService:
    """
    Service for actions related operations.
    """

    def get_action(self, action: str) -> Action:
        """
        Get an action by its type.
        """
        action = Action.objects.filter(type=action).first()
        if not action:
            raise ValidationError(f"No action found for type: {action}")
        return action
