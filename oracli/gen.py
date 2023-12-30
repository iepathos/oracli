#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import time
import black
import reindent
from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger as log

APP_NAME = "oracli"
ORACLI_DIR = os.path.expanduser('~/.oracli')
ORACLI_THREAD_FILE = os.path.join(ORACLI_DIR, 'current_thread')

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


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


def clear_thread(thread_file=ORACLI_THREAD_FILE):
    if os.path.exists(thread_file):
        log.warning("Removing existing assistant thread.")
        os.remove(thread_file)
    else:
        log.info("No assistant thread found. {}".format(thread_file))


def create_assistant():
    assistant = client.beta.assistants.create(
        name="Oracli",
        instructions="You are a personal command line shell assistant. Write shell, python, ansible, and terraform scripts to automate command line tasks on MacOS Darwin and Ubuntu Linux.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo"
    )
    return assistant.id


def get_assistant_id():
    data = client.beta.assistants.list().model_dump()
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
    return message['content'][0]['text']['value']


def print_message(message):
    print(get_message_value(message))


def parse_codefences(text):
    '''
    Shell commands in the message should be code fenced like

    ```shell
    brew install pyenv
    ```

    We'll use the code fences to find shell command chunks in the text
    '''
    res = []
    start = None
    # print(text.split('\n'))
    for idx, line in enumerate(text.split('\n')):
        # log.debug('{} {}'.format(idx, line))
        if "```" in line and start is None:
            start = idx
            # log.debug('start code fence')
        elif "```" in line and start is not None:
            # end = idx
            start = None
            # log.debug('end code fence')
        elif '```' not in line and start is not None:
            # log.debug('add line from code fence')
            res.append(line)
    return res


def write_commands_to_file(commands, output_file, shebang):
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w') as f:
        shebang = '#!{shebang}\n'.format(shebang=shebang)
        if shebang not in commands[0]:
            f.write(shebang)
        for line in commands:
            f.write(line + "\n")

    st = os.stat(output_file)
    os.chmod(output_file, st.st_mode | stat.S_IEXEC)

    print("Generated {}".format(output_file))


def reindent_python(script_path):
    log.info("Running reindent to check indentation on {script}".format(script=script_path))
    reindent.makebackup = False
    reindent.check(script_path)


def black_python(script_path):
    log.info("Formatting {script} with black".format(script=script_path))
    BLACK_MODE = black.Mode(target_versions={black.TargetVersion.PY311}, line_length=120)

    with open(script_path) as f:
        code = f.read()

    try:
        code = black.format_file_contents(code, fast=False, mode=BLACK_MODE)
    except black.NothingChanged:
        pass
    except Exception as e:
        log.error(e)

    with open(script_path, 'w') as f:
        f.write(code)


def generate_commands(msg, tags):
    thread_id = get_or_create_thread()

    for tag in tags:
        msg += " {tag}".format(tag=tag)
    log.info(msg)
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
      instructions="Assist user with script commands to accomplish their goals."
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

    message = messages.model_dump()['data'][0]
    print_message(message)

    text = get_message_value(message)
    commands = parse_codefences(text)
    if len(commands) == 0:
        log.warning("No code fenced commands parsed from openai response text.")
        return

    print()

    return commands
    
