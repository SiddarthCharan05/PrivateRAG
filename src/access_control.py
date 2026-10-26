ROLE_PERMISSIONS = {
    "general": ["general"],

    "it": [
        "general",
        "it",
    ],

    "hr": [
        "general",
        "hr",
    ],

    "finance": [
        "general",
        "finance",
    ],
}


def get_allowed_departments(role):
    """Return departments accessible to an employee role."""

    role = role.lower()

    if role not in ROLE_PERMISSIONS:
        return ["general"]

    return ROLE_PERMISSIONS[role]


def is_authorized(role, department):
    """Check whether a role can access a department."""

    allowed_departments = get_allowed_departments(role)

    return department in allowed_departments