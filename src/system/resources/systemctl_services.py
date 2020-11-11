import enum
from flask_restful import Resource, reqparse, abort

from src.system.utils.shell_commands import execute_command, systemctl_status_check

'''
sudo systemctl status nubeio-rubix-wires.service
'''
'''
sudo systemctl status nubeio-bac-rest.service
'''
'''
sudo systemctl status nubeio-wires-plat.service
'''


class ServiceAction(enum.Enum):
    START = 1
    STOP = 2
    RESTART = 3


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    PLAT = 'nubeio-wires-plat.service'
    MOSQUITTO = 'mosquitto.service'


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart`')


def _validate_and_create_service(action, service) -> str:
    if service.upper() in Services.__members__.keys():
        return "sudo systemctl {} {}".format(action, Services[service.upper()].value)
    else:
        abort(400, message="service {} does not exist in our system".format(service))


class SystemctlCommand(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, help='action should be `start | stop | restart`', required=True)
        parser.add_argument('service',
                            type=str,
                            help='service type is required example: (wires, mosquitto)',
                            required=True)
        args = parser.parse_args()
        action = _validate_and_create_action(args['action'])
        service = _validate_and_create_service(action, args['service'])
        call = execute_command(service)
        if call:
            return {"service: {}".format(call)}
        else:
            return {"service: {} failed".format(call)}, 404




class SystemctlStatus(Resource):
    @classmethod
    def get(cls, service):
        if service.upper() in Services.__members__.keys():
            check = systemctl_status_check(Services[service.upper()].value)
            print(3333)
            print(check)
            print(3333)
            if check:
                msg = "status: {} is running".format(service)
                return {'msg': msg}
            else:
                msg = "status: {} is not running".format(service)
                return {'msg': msg}
        else:
            msg = "status: {}  does not exist in our system".format(service)
            return {'msg': msg}

