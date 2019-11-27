#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from acrscan.lib_downloader import download_lib

try:
    from acrscan.acrscan import ACRCloudScan
except ImportError:
    download_lib()
    from acrscan.acrscan import ACRCloudScan
import logging
import yaml
import os
import click

with open('config.yaml', 'r') as f:
    try:
        config_dict = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        logging.error(exc)

acrcloud_config = config_dict.get('acrcloud')
acrcloud_config.get('')
logging.basicConfig(level=logging.INFO)

if acrcloud_config.get('debug'):
    logging.basicConfig(level=logging.DEBUG)


class OptionRequiredIf(click.Option):

    def full_process_value(self, ctx, value):
        value = super(OptionRequiredIf, self).full_process_value(ctx, value)
        if not ctx.params.get('with_duration') and value:
            msg = 'Required --with-duration, if you want filter pls add --with-duration'
            raise click.MissingParameter(ctx=ctx, param=self, message=msg)
        return value


@click.command()
@click.option('--target', '-t',
              help='The target need to scan (a folder or a file).')
@click.option('--output', '-o', default='',
              help='Output result to this folder. (Must be a folder path)')
@click.option('--format', 'output_format', type=click.Choice(['csv', 'json']),
              help='output format.(csv or json)')
@click.option('--with-duration/--no-duration', '-w', default=False,
              help='Add played duration to the result')
@click.option('--filter-results/--no-filter', default=False,
              help='Enable filter.(It must be used when the with-duration option is on)', cls=OptionRequiredIf)
def main(target, output, output_format, with_duration, filter_results):
    ctx = click.get_current_context()
    if not any(v for v in ctx.params.values()):
        click.echo(ctx.get_help())
        ctx.exit()

    acr = ACRCloudScan(acrcloud_config)
    acr.with_duration = with_duration
    acr.filter_results = filter_results
    if output:
        if not os.path.exists(output):
            open(output, 'w+')
    acr.scan_target(target, output, output_format)


if __name__ == '__main__':
    main()
