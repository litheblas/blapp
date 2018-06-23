def user_info(claims, user):
    person = user.person

    return {
        **claims,
        # profile
        'name': person.full_name,
        'given_name': person.first_name,
        'family_name': person.last_name,
        'nickname': person.nickname,
        'preferred_username': user.username,
        'birthdate': person.date_of_birth.isoformat(),

        # email
        'email': person.email,

        # phone

        # address

    }
