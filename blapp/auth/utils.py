import re


def token_from_request(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        return None
    match = re.match(r"^Service-Token (\S*)$", auth_header)
    if not match:
        return None
    return match[1]
