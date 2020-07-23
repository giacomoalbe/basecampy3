import argparse
import logging
import os
import traceback

from basecampy3 import Basecamp3
from basecampy3.token_requestor import TokenRequester
from basecampy3.config import BasecampConfig

available_commands = [
    ("login", "Login with Basecamp using OAuth2"),
    ("projects", "Manage current user projects"),
    ("version", "Show BasecamPY3 CLI version"),
    ("me", "Show information about currently logged in user"),
]

class CLI(object):
    bc3 = Basecamp3()

    def __init__(self):
        pass

    @classmethod
    def from_command_line(cls):
        new = cls()

        parser = argparse.ArgumentParser(
            "bc3",
            description="BasecamPY3 API Tool"
        )

        parser.add_argument(
            "--debug",
            "--verbose",
            dest="debug",
            action="store_true",
            help="Enables more verbose output"
        )

        subparsers = parser.add_subparsers(
            metavar="command",
            dest="command"
        )

        for command in available_commands:
            subparsers.add_parser(command[0], help=command[1])

        args = parser.parse_args()

        loglevel = logging.DEBUG if args.debug else logging.INFO

        logging.getLogger().setLevel(loglevel)
        logging.basicConfig()

        if (args.command):
            getattr(cls, args.command)(cls.bc3)
        else:
            parser.print_help()

    @staticmethod
    def configure(basecamp = None):
        print("This will generate an access token and refresh token for using the Basecamp 3 API.")
        print("If you have not done so already, you need to create an app at:")
        print("https://launchpad.37signals.com/integrations")

        client_id = "d07cc672ec7c0fc1829490dfd7da963fe3b38070"
        client_secret = "9934efee6bcc7af32483333f5d2be5e668ea73bc"
        redirect_uri = "http://localhost:8081/auth"

        print("Obtaining your access key and refresh token...")
        requestor = TokenRequester(client_id, client_secret)

        code = requestor.get_access_token()

        tokens = Basecamp3.trade_user_code_for_access_token(
            client_id=client_id, redirect_uri=redirect_uri,
            client_secret=client_secret,
            code=code
        )

        print("Success! Your tokens are listed below.")
        print("Access Token: %s" % tokens['access_token'])
        print("Refresh Token: %s" % tokens['refresh_token'])

        while True:
            should_save = input("Do you want to save? (Y/N)").upper().strip()
            if should_save in ("Y", "YES"):
                should_save = True
                break
            elif should_save in ("N", "NO"):
                should_save = False
                break
            else:
                print("Sorry I don't understand. Please enter Y or N.")
        if should_save is False:
            return
        while True:
            location = input("Where should I save? (default ~/.conf/basecamp.conf)")
            location = location.strip()
            if not location:
                location = os.path.expanduser("~/.conf/basecamp.conf")
            try:
                conf = BasecampConfig(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                      access_token=tokens['access_token'], refresh_token=tokens['refresh_token'])
                conf.save(location)
                break
            except Exception as ex:
                logging.error(traceback.format_exc())
                print("Failed to save to '%s'" % location)

    @staticmethod
    def projects(basecamp = None):
        print("Project list")
        print("============")

        for project in basecamp.projects.list():
            print(project.name)

    @staticmethod
    def version():
        print("0.0.1")

    @staticmethod
    def me(basecamp = None):
        user_data = basecamp.who_am_i

        print(f"{user_data['identity']['first_name']} {user_data['identity']['last_name']}")


    # @staticmethod
    # def _get_modules():
    #     # find all endpoint modules
    #     endpoint_modules = inspect.getmembers(basecampy3.endpoints, inspect.ismodule)
    #     modules = []
    #     endpoint_map = {}
    #     for module_name, module in endpoint_modules:
    #         if module_name in ('_base', 'util'):  # exclude non-endpoint modules
    #             continue
    #         endpoint_dict = {}
    #
    #         classes = inspect.getmembers(module, inspect.isclass)
    #         for classname, cls in classes:
    #             # find the class for this Endpoint
    #             if cls is not BasecampEndpoint and issubclass(cls, BasecampEndpoint):
    #                 # this is our Endpoint, get its non-private methods
    #                 methods_dict = {mthd[0]: mthd for mthd in inspect.getmembers(cls, inspect.ismethod)
    #                                 if not mthd[0].startswith('_')}
    #
    #                 endpoint_dict[classname] = methods_dict
    #
    #                 endpoint_map[module_name] = endpoint_map
    #                 break
    #
    #         issubclass(inspect.getmembers(module, inspect.isclass)[3][1], basecampy3.endpoints._base.BasecampEndpoint)
    #     return {m[0]: m[1] for m in endpoint_modules if m[0] not in ("_base", "util")}


def main():
    return CLI.from_command_line()


if __name__ == "__main__":
    cli = main()
