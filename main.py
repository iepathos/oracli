#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import logging
import platform

from oracli import gen


def _initlog():
    if os.environ.get("DEBUG", False):
        logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    """AI script generation tool."""
    pass


@cli.command()
@click.argument("prompt")
@click.option("-o", "--output-file")
@click.option("-c", "--context-file")
def sh(prompt, output_file, context_file):
    """Generate a shell script to accomplish tasks auomatically."""
    if not output_file:
        output_file = "output.sh"

    shebang = os.environ.get("SHELL")
    tags = [
        # "generate script",
        "for {os_type}".format(os_type=platform.system()),
        "with shell {shebang}".format(shebang=shebang),
    ]
    commands = gen.generate_commands(prompt, tags, context_file)
    gen.write_commands_to_file(commands, output_file, shebang)


@cli.command()
@click.argument("prompt")
@click.option("-o", "--output-file")
@click.option("-c", "--context-file")
def py(prompt, output_file, context_file):
    """Generate a python script to accomplish tasks auomatically."""
    if not output_file:
        output_file = "output.py"

    shebang = "/usr/bin/env python"
    tags = [
        # "generate script",
        "for {os_type}".format(os_type=platform.system()),
        "with {shebang}".format(shebang=shebang),
    ]
    commands = gen.generate_commands(prompt, tags, context_file)
    gen.write_commands_to_file(commands, output_file, shebang)
    gen.reindent_python(output_file)
    gen.black_python(output_file)


@cli.command()
def clear():
    """Clear AI assistant thread to start over fresh."""
    gen.clear_thread()


if __name__ == "__main__":
    _initlog()
    cli()
