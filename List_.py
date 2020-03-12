from .EntityBase import EntityBase


class List(EntityBase):
    base_url_path = "/lists/"

    def create(self, list_name, list_type=None, description=None, FolderID=None, Permissions=None):
        url = self.build_url("create")
