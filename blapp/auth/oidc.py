from django.utils.translation import ugettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims


class CustomScopeClaims(ScopeClaims):
    info_mattermost = (
        _("Mattermost"),
        _("Access to information needed to create a Mattermost account."),
    )

    def scope_mattermost(self):
        # Mattermost is hard-wired to GitLab's payload:
        # https://docs.gitlab.com/ee/api/users.html#user
        return {
            # Wraps the UUID to an integer fitting in 63 bits (or Mattermost
            # will fall on its side)
            "id": self.user.id.int % (2 ** 63 - 1),
            "username": self.userinfo["preferred_username"],
        }


def user_info(claims, user):
    person = user.person

    return {
        **claims,
        # profile
        "name": person.full_name,
        "given_name": person.first_name,
        "family_name": person.last_name,
        "nickname": person.nickname,
        "preferred_username": user.username,
        "birthdate": person.date_of_birth.isoformat(),
        # email
        "email": person.email,
        # phone
        # address
    }
