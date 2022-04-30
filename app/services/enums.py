import enum


class UserRole(enum.Enum):
    Admin: str = "ADMIN"
    User: str = "USER"
    