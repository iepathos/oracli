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

    def test_thread_file_write_get_and_clear(self):
        """ """

        gen.ORACLI_DIR = os.path.expanduser("/tmp/test_oracli")
        thread_file_path = os.path.join(gen.ORACLI_DIR, "current_thread")
        gen.ORACLI_THREAD_FILE = thread_file_path
        thread_id = gen.get_or_create_thread()
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


if __name__ == "__main__":
    unittest.main()
