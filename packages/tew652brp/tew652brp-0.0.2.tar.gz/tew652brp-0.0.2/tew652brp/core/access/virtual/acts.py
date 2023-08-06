import xml.etree.ElementTree as ET

from tew652brp.core.base import BaseAct
from tew652brp.core.access.virtual.types import VServerInfo


class GetServersAct(BaseAct):
    def __init__(self, request_method, url):
        super().__init__(request_method, url)
        self._params = {
            'ccp_act': 'get',
            'num_inst': '1',
            'oid_1': 'IGD_WANDevice_i_VirServRule_i_',
            'inst_1': '11000',
        }

    @staticmethod
    def xml_to_vservers(xml):
        raw_servers = ET.fromstring(xml).findall('IGD_WANDevice_i_VirServRule_i_')
        return [VServerInfo.from_xml(server) for server in raw_servers]

    def submit(self):
        return self.xml_to_vservers(super().submit().text)


class DeleteServerAct(BaseAct):
    def __init__(self, request_method, url, server_info):
        super().__init__(request_method, url)
        self._params = {
            'ccpSubEvent': 'CCP_SUB_VIRTUALSERVER',
            'nextPage': 'virtual_server.htm',
            'num_inst': '1',
            'oid_1': 'IGD_WANDevice_i_VirServRule_i_',
            'inst_1': server_info.instance,
        }


class UpdateServerAct(BaseAct):
    def __init__(self, request_method, url, server_info):
        super().__init__(request_method, url)
        self._params = server_info.to_dict()