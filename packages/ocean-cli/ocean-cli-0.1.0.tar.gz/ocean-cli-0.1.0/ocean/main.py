import argparse
import click
from pathlib import Path
import os
import yaml
import sentry_sdk

from ocean import code

# from ocean import api, auth, utils, job, config, init, data, command


sentry_sdk.init(
    "https://a6b6c48c3f444b9f99ca70b543c09a46@o922093.ingest.sentry.io/5881410",
    traces_sample_rate=1.0,
)


CONTEXT_SETTINGS = dict(auto_envvar_prefix="COMPLEX")


class Environment:
    def __init__(self, load=True):
        self.verbose = False
        self.config_path = Path.home() / ".ocean" / "config.yaml"
        self.config = {}

        if load:
            self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            click.echo(
                f"Config file '{self.config_path}' is not exist.\nPlease run \n\n\tocean init\n"
            )
            exit()

        with open(self.config_path, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def save_config(self):
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f)

    def update_config(self, key, value):
        self.config.update({key: value})
        self.save_config()

    def get_auth_token(self):
        return self.config.get(code.AUTH_TOKEN)

    def get_url(self):
        return self.config.get(code.OCEAN_URL)

    def get_token(self):
        return self.config.get(code.TOKEN)

    def get_username(self):
        self.config.get("username")

    def get_uuid(self):
        return self.config.get("uuid")

    def get_presets(self):
        return self.config["presets"]

    def add_presets(self, preset):
        self.config["presets"].append(preset)
        self.save_config()

    def delete_presets(self, key):
        for idx, pre in enumerate(self.config["presets"]):
            if pre["name"] == key:
                del self.config["presets"][idx]
                self.save_config()
                break
        else:
            click.echo(f"Preset `{key}` not found.")
            exit()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_env = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"ocean.commands.cmd_{name}", None, None, ["cli"])
        except ImportError as e:
            print(e)
            return
        return mod.cli


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
# @pass_env
def cli():
    pass

    # parser = argparse.ArgumentParser(description='Ocean CLI.')
    # parser.set_defaults(func=lambda x: parser.print_help())
    # subparsers = parser.add_subparsers(title='subcommands', dest='cmd')

    # # init
    # init_parser = subparsers.add_parser("init", help='initialize ocean-cli.')
    # init_parser.set_defaults(func=init.init)

    # # get parser
    # get_parser = subparsers.add_parser("get", help='get ocean resources.')
    # get_parser.add_argument("resource", help="ocean resource")
    # get_parser.set_defaults(func=command.get)

    # # auth parser
    # login_parser = subparsers.add_parser("login", help='login to ocean.')
    # # login_parser.add_argument("email", help="email address")
    # # login_parser.add_argument("password", help="password")
    # login_parser.set_defaults(func=auth.login)

    # logout_parser = subparsers.add_parser("logout", help='logout from ocean.')
    # logout_parser.set_defaults(func=auth.logout)

    # # job parser
    # job_parser = subparsers.add_parser("job", help='working with job')
    # job_parser.set_defaults(func=lambda x: job_parser.print_help())
    # job_subparsers = job_parser.add_subparsers(title='Job subcommands', dest='job')
    # # job_subparsers.set_defaults(func=lambda x: job_parser.print_help())

    # job_submit_parser = job_subparsers.add_parser("submit", help='submit job')
    # job_submit_parser.add_argument("name", help="job name")
    # job_submit_parser.add_argument("--command", "--cmd", nargs='*', required=True, help="command for job")
    # job_submit_parser.add_argument("--image", default="mlvclab/pytorch:1.6.0-cuda10.1-cudnn7-devel", help="job base image")
    # job_submit_parser.add_argument("--cpu", default=4, help="cpu for job")
    # job_submit_parser.add_argument("--memory", default=16, help="memory for job")
    # job_submit_parser.add_argument("--gpu", default=1, help="gpu for job")
    # job_submit_parser.add_argument("--gpu_type", default="nvidia-rtx-2080ti", help="gpu type for job")
    # job_submit_parser.add_argument("--volume", default="default", help="volume to attach job")
    # job_submit_parser.add_argument("--logs", "-l", default=False, action="store_true", help="printing logs")
    # job_submit_parser.add_argument("--debug", "-d", default=False, action="store_true", help="debug mode")
    # job_submit_parser.set_defaults(func=job.submit)

    # job_logs_parser = job_subparsers.add_parser("logs", help='show job logs')
    # job_logs_parser.add_argument("name", help="job name")
    # job_logs_parser.set_defaults(func=job.logs)

    # # config parser
    # config_parser = subparsers.add_parser("config", help='config of ocean CLI.')
    # config_parser.set_defaults(func=lambda x: config_parser.print_help())
    # config_subparsers = config_parser.add_subparsers(title='config subcommands', dest='config')

    # config_get_parser = config_subparsers.add_parser("get", help='get config')
    # config_get_parser.add_argument("--url", action="store_true", help="get ocean url")
    # config_get_parser.set_defaults(func=config.get)

    # config_set_parser = config_subparsers.add_parser("set", help='set config')
    # config_set_parser.add_argument("--url", default="", help="set ocean url")
    # config_set_parser.set_defaults(func=config.set)

    # # data file upload
    # data_parser = subparsers.add_parser("data", help='data management')
    # data_parser.set_defaults(func=lambda x: data_parser.print_help())
    # data_subparsers = data_parser.add_subparsers(title='data subcommands', dest='data')

    # data_upload_parser = data_subparsers.add_parser("upload", help='upload data to server')
    # data_upload_parser.add_argument("name", help="data name")
    # data_upload_parser.add_argument("--path", help="specify file path to upload")
    # data_upload_parser.set_defaults(func=data.upload)

    # data_list_parser = data_subparsers.add_parser("list", help='list uploaded data')
    # data_list_parser.set_defaults(func=data.list_datasync)

    # # parse
    # args = parser.parse_args()
    # if args.cmd != 'init' and not utils.check_env_exist():
    #     print("Config file '.oceanrc' is not exist.\nPlease run \n\n\tocean init\n")
    # else:
    #     args.func(args)


if __name__ == "__main__":
    cli()
