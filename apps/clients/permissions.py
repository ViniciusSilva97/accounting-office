from .models import ClientAssignment


def can_access_client(user, client):
    if not user.is_authenticated or not user.is_active or user.office_id != client.office_id:
        return False
    if user.role == user.Role.ADMIN:
        return True
    return ClientAssignment.objects.filter(
        user=user, client=client, revoked_at__isnull=True
    ).exists()


def can_register_client(user):
    return (
        user.is_authenticated
        and user.is_active
        and user.role
        in {
            user.Role.ADMIN,
            user.Role.ACCOUNTANT,
        }
    )
