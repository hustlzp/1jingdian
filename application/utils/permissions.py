from permission import Permission
from .rules import VisitorRule, UserRule, AdminRule, CollectionOwnerRule


class VisitorPermission(Permission):
    def rule(self):
        return VisitorRule()


class UserPermission(Permission):
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    def rule(self):
        return AdminRule()


class CollectionOwnerPermission(Permission):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionOwnerPermission, self).__init__()

    def rule(self):
        return AdminRule() | CollectionOwnerRule(self.collection)
