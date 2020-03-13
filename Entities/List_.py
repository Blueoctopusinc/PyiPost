from math import ceil

from EntityBase import EntityBase
from exceptions_ import PyiPostHTTPError, PyiPostError


class List_(EntityBase):
    base_url_path = "lists"

    def create(self, list_name, list_type="static", description=None, folder_id=None, permissions=None):
        """
        Create List - https://ipost.readme.io/reference#create-list
        Creates a new List
        https://endpoint.enterprise.ipost.com/api/v1/ClientToken/lists/create/
        @param list_name: Name of the list you want to create
        @param list_type: List type, either "static" or "suppression"
        @param description:  List description e.g. Top buyers list
        @param folder_id:  Folder this list will be places in
        @param permissions: Permission level, either - "private" or "public"
        @return:
        """
        # Build the full URL
        url = self.build_url("create")

        payload_temp = {"ListName": list_name,
                        "ListType": list_type,
                        "Description": description,
                        "FolderID": folder_id,
                        "Permissions": permissions}

        # Filter out None values from the payload dictionary
        payload = {key: val for key, val in payload_temp.items() if val is not None}

        try:
            response = self.client.make_request(url, payload, "POST")
            return response.get("data").get("ListID")
            check = 2
        except PyiPostHTTPError as e:
            raise e
        except Exception as  e:
            raise e

    def get_lists(self, list_name=None, list_type=None, list_description=None, list_creation_time_before=None,
                  list_creation_time_after=None, list_folder_id=None, public=None):
        """
        Search for lists - https://ipost.readme.io/reference#search-lists
        Gets all lists n the account with optional filter criteria
        @param list_name:
        @param list_type:
        @param list_description:
        @param list_creation_time_before:
        @param list_creation_time_after:
        @param list_folder_id:
        @param public:
        @return:
        """
        url = self.build_url("search")

        payload_temp = {"ListName": list_name,
                        "ListType": list_type,
                        "ListDescription": list_description,
                        "ListCreationTimeBefore": list_creation_time_before,
                        "ListCreateTimeAfter": list_creation_time_after,
                        "ListFolderID": list_folder_id,
                        "Public": public}

        # Filter out None values from the payload dictionary
        payload = {key: val for key, val in payload_temp.items() if val is not None}
        try:
            response = self.client.make_request(url, payload)
            return response.get("data")
        except PyiPostHTTPError as e:
            raise e

    def get_list_contacts(self, list_id, search_fields=None, existing_results=None):
        """

        @param list_id:
        @param search_fields:
        @param existing_results:
        @return:
        """

        def get_remaining_contacts(total_results, last_result, contacts, search_fields, url):
            """

            @param total_results:
            @param last_result:
            @param contacts:
            @param search_fields:
            @param url:
            @return:
            """
            if last_result < total_results:

                response = self.client.make_request(url, search_fields, "POST", {"start": last_result})
                contacts.extend(response["data"]["contacts"])
                total_results = int(response["metadata"]["total_results"])
                last_result = int(response["metadata"]["results"]["last"])
                get_remaining_contacts(total_results, last_result, contacts, search_fields, url)

        """
        @param list_id:
        @return:
        """

        url = self.build_url("{list_id}/contacts".format(list_id=list_id))
        contacts = []
        try:
            # Make initial request
            response = self.client.make_request(url, search_fields, "POST")
            contacts.extend(response["data"]["contacts"])
            total_results = int(response["metadata"]["total_results"])
            last_result = int(response["metadata"]["results"]["last"])
            get_remaining_contacts(total_results, last_result, contacts, search_fields, url)
            return contacts
        except Exception as e:
            pass

    def add_contacts_to_list(self, contacts, list_id):
        """

        @param contacts:
        @param list_id:
        @return:
        """

        def remove_invalid_contacts(contacts):
            return [contact for contact in contacts if contact.get("Email") or contact.get("ContactID")]

        vetted_contacts = remove_invalid_contacts(contacts)
        if not vetted_contacts:
            if len(contacts) != len(vetted_contacts):
                raise PyiPostError("all {removed_contacts} have no Email or ContactID.".format(
                    removed_contacts=len(contacts)))

        payload = {"ContactStatus": vetted_contacts}
        try:
            url = self.build_url("{list_id}/add/".format(list_id=list_id)
            response = self.client.make_request(url, payload, "POST")
        except Exception as e:
            pass

    def add_contacts_to_MD5_list(self):
        raise NotImplementedError

    def empty_list(self, list_id, contact_type="all"):
        url = self.build_url("{list_id}/clean/".format(list_id=list_id)
        payload = {"ContactType": contact_type}
        try:
            self.client.make_request(url, payload, "POST")
        except Exception as e:
            pass