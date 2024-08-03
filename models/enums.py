import enum

class RoleType(enum.Enum):
    ADMIN = "admin"
    NEW_USER = "user"
    AGENT = "agent"