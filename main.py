#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import logging
from oracli.gen import generate_script, reindent_python_script, black_python_script, clear_thread


def _initlog():
    if os.environ.get("DEBUG", False):
        logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('prompt')
@click.option('-o', '--output-file')
def sh(prompt, output_file='output.sh'):
    shebang = os.environ.get("SHELL")
    generate_script(prompt, shebang, output_file)


@cli.command()
@click.argument('prompt')
@click.option('-o', '--output-file')
def py(prompt, output_file='output.py'):
    shebang = '/usr/bin/env python'
    generate_script(prompt, shebang, output_file)
    reindent_python_script(output_file)
    black_python_script(output_file)


@cli.command()
def clear():
    clear_thread()
    print("Done.")


if __name__ == '__main__':
    _initlog()
    cli()