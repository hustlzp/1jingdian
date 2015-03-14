from permission import Permission
from .rules import VisitorRule, UserRule, AdminRule, CollectionOwnerRule, PieceAddRule, \
    PieceOwnerEditRule


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
        return AdminRule() | CollectionOwnerRule(self.collection)


class PieceEditPermission(Permission):
    def __init__(self, piece):
        self.piece = piece
        super(PieceEditPermission, self).__init__()

    def rule(self):
        return AdminRule() | PieceOwnerEditRule(self.piece)


class PieceAddPermission(Permission):
    def rule(self):
        return PieceAddRule()
