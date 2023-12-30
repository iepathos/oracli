Oracli
-----

Command line AI assistant for generating devops scripts.


# Install Oracli

Oracli uses Poetry to manage python dependencies. To install Poetry, you can use the following command on your macOS with zsh shell:

```shell
curl -sSL https://install.python-poetry.org | sh
```

Install project dependencies.

```shell
poetry install --sync
```

Optionally add bin to PATH.

```shell
export PATH=$PATH:/path/to/oracli/bin
```

# Add OPENAI API Key to .env

Create a .env files in oracli repository and add your OpenAI API key.

file: .env
```
OPENAI_API_KEY=sk-<your-personal-openai-api-key>
```
