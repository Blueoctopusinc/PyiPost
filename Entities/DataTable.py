from EntityBase import EntityBase

class DataTable(EntityBase):
    base_url_path = "DataTables"

    def create(self, DataTableName, ):
        url = self.build_url("create")

