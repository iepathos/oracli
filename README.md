# Oracli

Command line AI assistant for generating devops scripts.


## Install Oracli

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

## Add OpenAI API Key to .env

Create a .env files in oracli repository and add your OpenAI API key.

file: .env
```
OPENAI_API_KEY=sk-<your-personal-openai-api-key>
```

## Example Usage

```shell
$ oracli sh "test internet connection"
```


```shell              
2023-12-30 06:47:56.942 | INFO     | oracli.gen:generate_commands:239 - test internet connection for Darwin with shell /bin/zsh
Unfortunately, in this notebook environment, I don't have access to the internet to perform network-related operations such as testing internet connectivity.

However, you can use the `ping` command in your terminal to test internet connectivity. Here's an example of how you can use it on macOS with zsh shell:
```

```shell
ping -c 5 google.com
```

```shell
This command will send 5 ICMP echo request packets to `google.com` and display the response. You should see successful responses if you have an internet connection.

If you receive a `ping: cannot resolve google.com: Unknown host` error, it means that your DNS settings might be incorrect. In that case, you can try using a different DNS server or check your network configuration.

Let me know if you have any other questions!

Generated output.sh
```


```shell
$ cat output.sh
#!/bin/zsh
ping -c 5 google.com
```

```shell
$ ./output.sh
PING google.com (142.251.46.206): 56 data bytes
64 bytes from 142.251.46.206: icmp_seq=0 ttl=117 time=12.707 ms
64 bytes from 142.251.46.206: icmp_seq=1 ttl=117 time=17.068 ms
64 bytes from 142.251.46.206: icmp_seq=2 ttl=117 time=12.292 ms
64 bytes from 142.251.46.206: icmp_seq=3 ttl=117 time=16.748 ms
64 bytes from 142.251.46.206: icmp_seq=4 ttl=117 time=14.942 ms

--- google.com ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 12.292/14.751/17.068/1.981 ms
```



