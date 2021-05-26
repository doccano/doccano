import argparse
import multiprocessing
import os
import sys
import subprocess

import gunicorn.app.base
import gunicorn.util

from .app.celery import app
base = os.path.abspath(os.path.dirname(__file__))
manage_path = os.path.join(base, 'manage.py')
parser = argparse.ArgumentParser(description='doccano, text annotation for machine learning practitioners.')


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, options=None):
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        sys.path.append(base)
        return gunicorn.util.import_app('app.wsgi')


def command_db_init(args):
    print('Setup Database.')
    subprocess.call([sys.executable, manage_path, 'wait_for_db'], shell=False)
    subprocess.call([sys.executable, manage_path, 'migrate'], shell=False)
    subprocess.call([sys.executable, manage_path, 'create_roles'], shell=False)


def command_user_create(args):
    print('Create admin user.')
    subprocess.call([sys.executable, manage_path, 'create_admin',
                     '--username', args.username,
                     '--password', args.password,
                     '--email', args.email,
                     '--noinput'], shell=False)


def command_run_webserver(args):
    print(f'Starting server with port {args.port}.')
    options = {
        'bind': '%s:%s' % ('0.0.0.0', args.port),
        'workers': number_of_workers(),
        'chdir': base
    }
    StandaloneApplication(options).run()


def command_run_task_queue(args):
    print('Starting task queue.')
    app.worker_main(
        argv=[
            '--app=app',
            '--workdir={}'.format(base),
            'worker',
            '--loglevel=info',
            '--concurrency={}'.format(args.concurrency),
        ]
    )


def command_help(args):
    print(parser.parse_args([args.command, '--help']))


def main():
    # Create a command line parser.
    subparsers = parser.add_subparsers()

    # Create a parser for db initialization.
    parser_init = subparsers.add_parser('init', help='see `init -h`')

    parser_init.set_defaults(handler=command_db_init)

    # Create a parser for user creation.
    parser_create_user = subparsers.add_parser('createuser', help='see `createuser -h`')
    parser_create_user.add_argument('--username', type=str, default='admin', help='admin username')
    parser_create_user.add_argument('--password', type=str, default='password', help='admin password')
    parser_create_user.add_argument('--email', type=str, default='example@example.com', help='admin email')
    parser_create_user.set_defaults(handler=command_user_create)

    # Create a parser for web server.
    parser_server = subparsers.add_parser('webserver', help='see `webserver -h`')
    parser_server.add_argument('--port', type=int, default=8000, help='port number')
    parser_server.set_defaults(handler=command_run_webserver)

    # Create a parser for task queue.
    parser_queue = subparsers.add_parser('task', help='see `task -h`')
    parser_queue.add_argument('--concurrency', type=int, default=2, help='concurrency')
    parser_queue.set_defaults(handler=command_run_task_queue)

    # Create a parser for help.
    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    # Dispatch handler.
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        # If specified unknown command, show help.
        parser.print_help()


if __name__ == '__main__':
    main()
