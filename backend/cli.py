import argparse
import multiprocessing
import os
import platform
import sys
from pathlib import Path

import django
from django.core import management
from environs import Env

from .config.celery import app

env = Env()
DOCCANO_HOME = os.path.expanduser(os.environ.get("DOCCANO_HOME", "~/doccano"))
Path(DOCCANO_HOME).mkdir(parents=True, exist_ok=True)
env.bool("DEBUG", False)
os.environ["STANDALONE"] = "True"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
os.environ.setdefault("DATABASE_URL", os.path.join(f"sqlite:///{DOCCANO_HOME}", "db.sqlite3"))
os.environ.setdefault("MEDIA_ROOT", os.path.join(DOCCANO_HOME, "media"))
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base)
parser = argparse.ArgumentParser(description="doccano, text annotation for machine learning practitioners.")


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def is_windows():
    return platform.system() == "Windows"


def run_on_nix(args):
    import gunicorn.app.base
    import gunicorn.util

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, options=None):
            self.options = options or {}
            super().__init__()

        def load_config(self):
            config = {
                key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return gunicorn.util.import_app("config.wsgi")

    options = {
        "bind": "%s:%s" % ("0.0.0.0", args.port),
        "workers": args.workers,
        "chdir": base,
        "capture_output": True,
        "loglevel": "info",
    }
    StandaloneApplication(options).run()


def run_on_windows(args):
    from waitress import serve

    from config.wsgi import application

    serve(application, port=args.port, threads=args.workers)


def command_db_init(args):
    print("Setup Database.")
    management.call_command("wait_for_db")
    management.call_command("migrate")
    management.call_command("create_roles")


def command_user_create(args):
    print("Create admin user.")
    management.call_command(
        "create_admin", "--noinput", username=args.username, password=args.password, email=args.email
    )


def command_migrate(args):
    print("Start migration.")
    management.call_command("migrate")


def command_run_webserver(args):
    print(f"Starting server with port {args.port}.")
    if is_windows():
        run_on_windows(args)
    else:
        run_on_nix(args)


def command_run_task_queue(args):
    print("Starting task queue.")
    argv = [
        "--app=config",
        "--workdir={}".format(base),
        "worker",
        "--loglevel=info",
        "--concurrency={}".format(args.concurrency),
    ]
    if is_windows():
        argv.append("--pool=solo")
    app.worker_main(argv=argv)


def command_run_flower(args):
    print("Starting flower.")
    argv = [
        "--app=config",
        "--workdir={}".format(base),
        "flower",
    ]
    if args.basic_auth:
        argv.append("--basic_auth={}".format(args.basic_auth))
    app.worker_main(argv=argv)


def command_help(args):
    print(parser.parse_args([args.command, "--help"]))


def main():
    # Create a command line parser.
    subparsers = parser.add_subparsers()

    # Create a parser for db initialization.
    parser_init = subparsers.add_parser("init", help="see `init -h`")
    parser_init.set_defaults(handler=command_db_init)

    # Create a parser for migration.
    parser_migration = subparsers.add_parser("migrate", help="Updates database schema.")
    parser_migration.set_defaults(handler=command_migrate)

    # Create a parser for user creation.
    parser_create_user = subparsers.add_parser("createuser", help="see `createuser -h`")
    parser_create_user.add_argument("--username", type=str, default="admin", help="admin username")
    parser_create_user.add_argument("--password", type=str, default="password", help="admin password")
    parser_create_user.add_argument("--email", type=str, default="example@example.com", help="admin email")
    parser_create_user.set_defaults(handler=command_user_create)

    # Create a parser for web server.
    parser_server = subparsers.add_parser("webserver", help="see `webserver -h`")
    parser_server.add_argument("--port", type=int, default=8000, help="port number")
    parser_server.add_argument("--workers", type=int, default=number_of_workers(), help="the number of workers")
    parser_server.add_argument("--env_file", type=str, help="read in a file of environment variables")
    parser_server.set_defaults(handler=command_run_webserver)

    # Create a parser for task queue.
    parser_queue = subparsers.add_parser("task", help="see `task -h`")
    parser_queue.add_argument("--concurrency", type=int, default=2, help="concurrency")
    parser_queue.add_argument("--env_file", type=str, help="read in a file of environment variables")
    parser_queue.set_defaults(handler=command_run_task_queue)

    parser_flower = subparsers.add_parser("flower", help="see `flower -h`")
    parser_flower.add_argument("--env_file", type=str, help="read in a file of environment variables")
    parser_flower.add_argument("--basic_auth", type=str, help="username and password for basic authentication")
    parser_flower.set_defaults(handler=command_run_flower)

    # Create a parser for help.
    parser_help = subparsers.add_parser("help", help="see `help -h`")
    parser_help.add_argument("command", help="command name which help is shown")
    parser_help.set_defaults(handler=command_help)

    # Dispatch handler.
    args = parser.parse_args()
    if hasattr(args, "env_file") and args.env_file and Path(args.env_file).is_file():
        env.read_env(args.env_file, recurse=False, override=True)
    if hasattr(args, "handler"):
        django.setup()
        args.handler(args)
    else:
        # If specified unknown command, show help.
        parser.print_help()


if __name__ == "__main__":
    main()
