import logging
from typing import List, Dict, Union

from mrb.mapper import api_to_slaves_broadcast_topic_mapper
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info

from src import AppSetting
from src.slaves.resources.slaves_base import SlavesBase
from src.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class RemoteDeviceRegistry(metaclass=Singleton):
    def __init__(self):
        self.__app_setting: Union[AppSetting, None] = None
        self.__devices: Dict[str, Dict] = {}
        self.__available_inserted_devices_global_uuids: List[str] = []

    @property
    def devices(self) -> Dict[str, Dict]:
        return self.__devices

    @property
    def available_inserted_devices_global_uuids(self) -> List[str]:
        return self.__available_inserted_devices_global_uuids

    def register(self, app_setting: AppSetting):
        logger.info(f"Called devices registration")
        self.__app_setting = app_setting
        while True:
            self.poll_devices()

    def poll_devices(self):
        """
        We don't need to sleep the response itself has sleep of bridge timeout seconds
        """
        devices: Dict[str, Dict] = api_to_slaves_broadcast_topic_mapper('/api/wires/plat').content
        for global_uuid in devices:
            device = devices[global_uuid]
            device_info_model: DeviceInfoModel = get_device_info()
            devices[global_uuid] = {
                **device,
                'is_master': global_uuid == device_info_model.global_uuid
            }
        available_inserted_devices_global_uuids: List[str] = []
        slaves: Dict[str, Dict] = SlavesBase.get_slaves_by_app_setting(self.__app_setting)[0]
        for global_uuid in devices:
            if global_uuid in slaves:
                available_inserted_devices_global_uuids.append(global_uuid)

        self.__devices = devices
        self.__available_inserted_devices_global_uuids = available_inserted_devices_global_uuids
