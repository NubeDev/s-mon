import os

from src.system.apps.base.frontend_app import FrontendApp


class WiresBuildsApp(FrontendApp):
    @classmethod
    def id(cls) -> str:
        return 'WIRES'

    def name(self) -> str:
        return 'wires-builds'

    def service_file_name(self) -> str:
        return 'nubeio-rubix-wires.service'

    def data_dir_name(self) -> str:
        return 'rubix-wires'

    def port(self) -> int:
        return 1313

    def min_support_version(self) -> str:
        return 'v1.8.7'

    def gateway_access(self) -> bool:
        return False

    def get_cwd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires/systemd')

    def get_wd(self) -> str:
        return os.path.join(super().get_cwd(), 'rubix-wires')
