from tew652brp.core.base import BaseHandler
from tew652brp.core.access.virtual.acts import (
    GetServersAct,
    UpdateServerAct,
    DeleteServerAct
)


class VirtualHandler(BaseHandler):
    def __init__(self, session, url):
        super().__init__(session, url)

    def get_servers(self):
        return GetServersAct(
            self._session.post, self._routes['get_set']
        ).submit()

    def update_server(self, server_info):
        return UpdateServerAct(
            self._session.post, self._routes['get_set'], server_info
        ).submit()

    def delete_server(self, server_info):
        return DeleteServerAct(
            self._session.post, self._routes['get_set'], server_info
        ).submit()
