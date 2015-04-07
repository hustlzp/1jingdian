from permission import Permission
from .rules import VisitorRule, UserRule, AdminRule, PieceAddRule, PieceOwnerRule, TrustedUserRule


class VisitorPermission(Permission):
    def rule(self):
        return VisitorRule()


class UserPermission(Permission):
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    def rule(self):
        return AdminRule()


class CollectionEditPermission(Permission):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionEditPermission, self).__init__()

    def rule(self):
        return AdminRule()


class PieceEditPermission(Permission):
    def __init__(self, piece):
        self.piece = piece
        super(PieceEditPermission, self).__init__()

    def rule(self):
        return AdminRule() | PieceOwnerRule(self.piece) | TrustedUserRule()


class PieceAddPermission(Permission):
    def rule(self):
        return PieceAddRule()
