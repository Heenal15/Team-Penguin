""" This view is to check what sort of user type a user has """


def is_member(user):
    if (user.is_authenticated):
        return user.user_type == 1
    else:
        return False

def is_club_officer(user):
    if (user.is_authenticated):
        return user.user_type == 2
    else:
        return False

def is_club_owner(user):
    if (user.is_authenticated):
        return user.user_type == 3
    else:
        return False

def is_club_owner_or_officer(user):
    if (user.is_authenticated):
        return (user.user_type == 2 or user.user_type == 3)
    else:
        return False

def is_club_owner_or_officer_or_member(user):
    if (user.is_authenticated):
        return (user.user_type == 1 or user.user_type == 2 or user.user_type == 3)
    else:
        return False
