from eblast.models import EmailGroup


def create_emailgroup(basicgroup):
    emailgroup, created = EmailGroup.objects.get_or_create(
        name=basicgroup.name,
        basic_group=basicgroup
    )
    for user in basicgroup.super_admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.admins.all():
        emailgroup.users.add(user)
    for user in basicgroup.moderators.all():
        emailgroup.users.add(user)
    for user in basicgroup.members.all():
        emailgroup.users.add(user)

    return 1
