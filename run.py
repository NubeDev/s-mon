#!/usr/bin/env python3

import multiprocessing
import os

import click

from src import AppSetting, GunicornFlaskApplication

CLI_CTX_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


@click.command(context_settings=CLI_CTX_SETTINGS)
@click.option('-p', '--port', type=int, default=AppSetting.PORT, show_default=True, help='Port')
@click.option('-g', '--global-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.GLOBAL_DIR_ENV),
              help='Global dir')
@click.option('-d', '--data-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.DATA_DIR_ENV),
              help='Application data dir')
@click.option('-c', '--config-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.CONFIG_DIR_ENV),
              help='Application config dir')
@click.option('-a', '--artifact-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.ARTIFACT_DIR_ENV),
              help='Artifact downloaded dir')
@click.option('-b', '--backup-dir', type=click.Path(), default=lambda: os.environ.get(AppSetting.BACKUP_DATA_DIR_ENV),
              help='Backup dir')
@click.option('--prod', is_flag=True, help='Production mode')
@click.option('-s', '--setting-file', help='Rubix-Service: setting json file')
@click.option('--workers', type=int, help='Gunicorn: The number of worker processes for handling requests.')
@click.option('--gunicorn-config', help='Gunicorn: config file(gunicorn.conf.py)')
@click.option('--log-level', type=click.Choice(['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], case_sensitive=False),
              show_default=True, help='Logging level')
@click.option('--device-type', type=click.Choice(['amd64', 'arm64', 'armv7']), default='armv7', show_default=True,
              help='Device type')
@click.option('--auth', is_flag=True, help='Enable JWT authentication.')
@click.option('-l', '--logging-conf', help='Rubix-Service: logging config file')
def cli(port, global_dir, data_dir, config_dir, artifact_dir, backup_dir, prod, workers, setting_file, gunicorn_config,
        log_level, device_type, auth, logging_conf):
    setting = AppSetting(global_dir=global_dir, data_dir=data_dir, config_dir=config_dir, artifact_dir=artifact_dir,
                         backup_dir=backup_dir, prod=prod, device_type=device_type, auth=auth).reload(setting_file)
    options = {
        'bind': '%s:%s' % ('0.0.0.0', port),
        'workers': workers if workers is not None else number_of_workers() if prod else 1,
        'loglevel': (log_level if log_level is not None else 'ERROR' if prod else 'DEBUG').lower(),
        'preload_app': True,
        'config': gunicorn_config,
        'logconfig': logging_conf
    }
    GunicornFlaskApplication(setting, options).run()


if __name__ == '__main__':
    cli()
