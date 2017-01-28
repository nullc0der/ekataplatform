from django.utils.crypto import get_random_string


def unique_ekata_id_setter(sender, profile):
    not_unique = True
    ekata_id = ''
    while not_unique:
        random_string = get_random_string(
            length=10,
            allowed_chars='0123456789'
        )
        ekata_id = 'ekatasocial.{}.registered'.format(random_string)
        userprofiles = sender.objects.filter(ekata_id=ekata_id)
        if not len(userprofiles):
            not_unique = False
    profile.ekata_id = ekata_id
    profile.save()
    return "{0} ekata_id set to {1}".format(profile.user.username.encode('utf-8'), ekata_id)
