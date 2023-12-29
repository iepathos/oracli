#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import click
import platform
# from typing import List
from openai import OpenAI
from dotenv import load_dotenv

import logging

APP_NAME = "oracli"


ORACLI_DIR = os.path.expanduser('~/.oracli')
ORACLI_THREAD_FILE = os.path.join(ORACLI_DIR, 'current_thread')


def write_thread_file(thread_id):
	if not os.path.exists(ORACLI_DIR):
		os.mkdir(ORACLI_DIR)
	with open(ORACLI_THREAD_FILE, 'w') as f:
		f.write(thread_id)


def get_thread():
	if not os.path.exists(ORACLI_THREAD_FILE):
		return None

	with open(ORACLI_THREAD_FILE) as f:
		thread_id = f.read()
	return thread_id


def _init_logger():
    logger = logging.getLogger(APP_NAME)
    if os.environ.get("DEBUG", False):
	    logging.basicConfig(level=logging.INFO)

_init_logger()
_logger = logging.getLogger(APP_NAME)

load_dotenv()


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def create_assistant():
	assistant = client.beta.assistants.create(
	    name="Shellai",
	    instructions="You are a personal command line shell assistant. Write and run code to accomplish command line tasks.",
	    tools=[{"type": "code_interpreter"}],
	    model="gpt-3.5-turbo"
	)
	return assistant.id


def get_assistant_id():
	data = client.beta.assistants.list().model_dump()
	if len(data['data']) > 0:
		for entry in data['data']:
			if entry['name'] == 'Shellai':
				return entry['id']
	return None


def get_or_create_assistant():
	assistant_id = get_assistant_id()
	if assistant_id is None:
		assistant_id = create_assistant()
	return assistant_id


def create_thread(user):
	thread = client.beta.threads.create()
	return thread


def get_or_create_thread():
	thread_id = get_thread()
	if thread_id is None:
		user = os.environ.get("USER")
		thread = create_thread(user)
		write_thread_file(thread.id)
		thread_id = thread.id
	return thread_id


def get_message_value(message):
	return message['content'][0]['text']['value']


def print_message(message):
	'''
	{
		'id': 'msg_zZ4fKCRWWfiAMHGY0Sz1rcfu',
		'assistant_id': 'asst_SdXbODvFlAeLUDHZb5latq2t',
		'content': [{
			'text': {
			'annotations': [],
			'value': 'To open a browser in macOS (Darwin) using the zsh shell, you can use the `open` command. Here\'s the syntax:\n\n```\nopen -a "Application Name"\n```\n\nReplace "Application Name" with the actual name of the browser application you want to open. For example, to open Google Chrome, you would use:\n\n```\nopen -a "Google Chrome"\n```\n\nPlease note that the actual name of the browser application may vary depending on the browser you have installed.'},
			'type': 'text'
		}],
		'created_at': 1703847172,
		'file_ids': [],
		'metadata': {},
		'object': 'thread.message',
		'role': 'assistant',
		'run_id': 'run_HxFioX50N2IZTFXdM6BfKikp',
		'thread_id': 'thread_Q9FHIWG3A3AyBto8lZVfHHDq'}
	'''
	print(get_message_value(message))



def parse_shell_commands(text, verbose=False):
	'''
	Shell commands in the message should be code fenced like

	```shell
	brew install pyenv
	```

	We'll use the code fences to find shell command chunks in the text
	'''
	res = []
	start = None
	for idx, line in enumerate(text.split('\n')):
		if verbose:
			_logger.info('{} {}'.format(idx, line))
		if "```" in line and start is None:
			start = idx
			if verbose:
				_logger.info('start code fence')
		elif "```" in line and start is not None:
			# end = idx
			start = None
			if verbose:
				_logger.info('end code fence')
		elif '```' not in line and start is not None:
			if verbose:
				_logger.info('add line from code fence')
			res.append(line)
	return res



def confirm_response(prompt_response):
	if prompt_response.strip() == '' or prompt_response.strip().lowercase() in ['y', 'ye', 'yes']:
		return True
	return False

def create_message(user, msg):
	# thread = threads[user]
	thread_id = get_or_create_thread()
	tags = [
		"in {os_type}".format(os_type=platform.system()),
		"in {shell_type}".format(shell_type=os.environ.get("SHELL")),
	]

	for tag in tags:
		msg += " {tag}".format(tag=tag)
	_logger.info(msg)
	message = client.beta.threads.messages.create(
	    thread_id=thread_id,
	    role="user",
	    content=msg,
	)
	# print(message)
	assistant_id = get_or_create_assistant()
	run = client.beta.threads.runs.create(
	  thread_id=thread_id,
	  assistant_id=assistant_id,
	  instructions="Assist user with shell commands to accomplish their goal."
	)

	while run.status != "completed":
		time.sleep(1)
		run = client.beta.threads.runs.retrieve(
		  thread_id=thread_id,
		  run_id=run.id
		)

	messages = client.beta.threads.messages.list(
	  thread_id=thread_id
	)

	for message in messages.model_dump()['data']:
		print_message(message)

	text = get_message_value(message)
	shell_commands = parse_shell_commands(text)
	if len(shell_commands) == 0:
		return

	execute_shell_prompt = input("Execute shell commands? (yes)")
	if confirm_response(execute_shell_prompt):
		for shell_command in shell_commands:
			print('Execute:')
			yes = input(shell_command + " (yes)")
			if confirm_response(yes):
				cmd = shell_command.split()
				subprocess.call(cmd)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('q')
def question(q):
	user = os.environ.get("USER")
	create_message(user, q)


@cli.command()
def clear():
	if os.path.exists(ORACLI_THREAD_FILE):
		_logger.warning("Removing existing assistant thread")
		os.remove(ORACLI_THREAD_FILE)
	else:
		_logger.info("No assistant thread found. {}".format(ORACLI_THREAD_FILE))
	print("Done.")


if __name__ == '__main__':
	user = os.environ.get("USER")
	create_thread(user)
	cli()