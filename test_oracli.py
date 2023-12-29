#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from oracli import parse_shell_commands

class TestOracli(unittest.TestCase):

	def test_parse_shell_commands(self):
		input_text = '''
To open Firefox in Darwin using the `/bin/zsh` shell, you can use the `open` command. The specific command would be:

```shell
open -a Firefox
```

This command will open Firefox in the default web browser on your Darwin system.
		'''

		expected_output = ['open -a Firefox']
		output = parse_shell_commands(input_text)
		assert(output == expected_output)


		input_text2 = '''
To open Firefox in Darwin using the `/bin/zsh` shell, you can use the `open` command in the terminal. Here's the command you can use:

```bash
open -a Firefox
```

This command will open Firefox if it is installed on your system.
		'''
		output = parse_shell_commands(input_text2)
		assert(output == expected_output)


if __name__ == '__main__':
    unittest.main()