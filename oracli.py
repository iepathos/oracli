#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import click
import platform
from openai import OpenAI
from dotenv import load_dotenv

import logging

APP_NAME = "oracli"

def _init_logger():
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO) 

_init_logger()
_logger = logging.getLogger(APP_NAME)

load_dotenv()


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

threads = {}


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
	threads[user] = thread


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
	print(message['content'][0]['text']['value'])


def create_message(user, msg):
	thread = threads[user]
	tags = [
		"in {os_type}".format(os_type=platform.system()),
		"in {shell_type}".format(shell_type=os.environ.get("SHELL")),
	]

	for tag in tags:
		msg += " {tag}".format(tag=tag)
	_logger.info(msg)
	message = client.beta.threads.messages.create(
	    thread_id=thread.id,
	    role="user",
	    content=msg,
	)
	# print(message)
	assistant_id = get_assistant_id()
	run = client.beta.threads.runs.create(
	  thread_id=thread.id,
	  assistant_id=assistant_id,
	  instructions="Assist user with shell commands to accomplish their goal."
	)

	while run.status != "completed":
		time.sleep(1)
		run = client.beta.threads.runs.retrieve(
		  thread_id=thread.id,
		  run_id=run.id
		)

	messages = client.beta.threads.messages.list(
	  thread_id=thread.id
	)

	for message in messages.model_dump()['data']:
		print_message(message)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('q')
def question(q):
	user = os.environ.get("USER")
	create_message(user, q)


if __name__ == '__main__':
	# create_assistant()
	user = os.environ.get("USER")
	create_thread(user)
	cli()