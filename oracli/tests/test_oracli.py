#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from oracli import gen

TEST_FILE = os.path.join("tmp", "current_thread")


class TestOracli(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOracli, self).__init__(*args, **kwargs)
        os.environ["DEBUG"] = "True"

    def test_parse_codefences(self):
        input_text = """
To open Firefox in Darwin using the `/bin/zsh` shell, you can use the `open` command. The specific command would be:

```shell
open -a Firefox
```

This command will open Firefox in the default web browser on your Darwin system.
        """

        expected_output = ["open -a Firefox"]
        output = gen.parse_codefences(input_text)
        assert output == expected_output

        input_text2 = """
To open Firefox in Darwin using the `/bin/zsh` shell, you can use the `open` command in the terminal. Here's the command you can use:

```bash
open -a Firefox
```

This command will open Firefox if it is installed on your system.
        """
        output = gen.parse_codefences(input_text2)
        assert output == expected_output

    def test_thread_file_get_and_clear(self):
        """ """

        TMP_DIR = os.environ.get("TMP_DIR", "/tmp")
        gen.ORACLI_DIR = ORACLI_DIR = os.path.join(TMP_DIR, "test_oracli")
        thread_file_path = os.path.join(ORACLI_DIR, "current_thread")
        sample_thread_str = "thread_mw8zu2QznCPsf1Y02WyNmBTH"
        gen.ORACLI_THREAD_FILE = thread_file_path
        # try not to require OPENAI_API_KEY we do not need
        # to test their API functionality just local functions
        # thread_id = gen.get_or_create_thread()
        thread_id = sample_thread_str
        if not os.path.exists(ORACLI_DIR):
            os.mkdir(ORACLI_DIR)
        with open(thread_file_path, "w") as f:
            f.write(sample_thread_str)
        output = gen.get_thread()
        assert thread_id == output

        self.assertTrue(
            "thread file {} exists".format(thread_file_path),
            os.path.exists(thread_file_path),
        )
        gen.clear_thread()
        self.assertTrue(
            "thread file {} does not exist".format(thread_file_path),
            not os.path.exists(thread_file_path),
        )

    def test_write_commands_to_file(self):
        TMP_DIR = os.environ.get("TMP_DIR", "/tmp")
        output_file = os.path.join(TMP_DIR, "test_commands.sh")
        shebang = "/bin/bash"
        commands = ["echo 'Hello, World!'", "echo 'and farewell!'"]
        gen.write_commands_to_file(commands, output_file, shebang)

        with open(output_file) as f:
            lines = f.readlines()

        shebang_line = "#!/bin/bash"
        expected_lines = [shebang_line] + commands
        for idx, line in enumerate(lines):
            self.assertTrue(expected_lines[idx].strip() == line.strip())

    def test_get_message_value(self):
        sample_message = {
            "id": "msg_zZ4fKCRWWfiAMHGY0Sz1rcfu",
            "assistant_id": "asst_SdXbODvFlAeLUDHZb5latq2t",
            "content": [
                {"text": {"annotations": [], "value": "testing123"}, "type": "text"}
            ],
            "created_at": 1703847172,
            "file_ids": [],
            "metadata": {},
            "object": "thread.message",
            "role": "assistant",
            "run_id": "run_HxFioX50N2IZTFXdM6BfKikp",
            "thread_id": "thread_Q9FHIWG3A3AyBto8lZVfHHDq",
        }

        expected_output = "testing123"
        output = gen.get_message_value(sample_message)
        self.assertTrue(expected_output == output)


if __name__ == "__main__":
    unittest.main()
