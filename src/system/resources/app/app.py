from flask_restful import Resource

from src.inheritors import inheritors
from src.system.apps.base.installable_app import InstallableApp


class AppResource(Resource):
    @classmethod
    def get(cls):
        apps = []
        for subclass in inheritors(InstallableApp):
            instance = subclass()
            app = instance.to_property_dict()
            app['service'] = instance.service()
            apps.append(app)
        return apps