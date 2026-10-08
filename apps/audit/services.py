from .models import AuditEvent


def record_event(*, office, actor, action, instance, client=None, metadata=None):
    return AuditEvent.objects.create(
        office=office,
        actor=actor,
        client=client,
        action=action,
        object_type=instance._meta.label_lower,
        object_public_id=str(instance.public_id),
        metadata=metadata or {},
    )
