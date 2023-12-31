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

```shell
oracli sh "determine the VPN_IP from any active openvpn connection"
Prompt: determine the VPN_IP from any active openvpn connection, return the shell code to make a devops command line script to accomplish this, only give me the code for this script, with shell /bin/zsh
--------------------------
To determine the VPN_IP from any active OpenVPN connection, you can use the following shell script:
```

```shell
#!/bin/zsh

# Get the default gateway for the VPN connection
VPN_GATEWAY=$(netstat -rn | grep -m1 -E '^0\.0\.0\.0' | awk '{print $2}')

# Get the IP address associated with the VPN gateway
VPN_IP=$(ip -br addr show | grep $VPN_GATEWAY | awk '{print $3}' | cut -d'/' -f1)

echo "VPN IP: $VPN_IP"
```

```shell
Save the script to a file, such as `vpn_ip_script.sh`, and make it executable using the command `chmod +x vpn_ip_script.sh`. Then, you can run the script using `./vpn_ip_script.sh` to determine the VPN_IP associated with the active OpenVPN connection.

The script uses `netstat` to find the default gateway for the VPN connection, and then `ip` to extract the IP address associated with that gateway. Finally, it outputs the VPN IP to the console.

Please note that this script assumes there is an active OpenVPN connection and that `netstat` and `ip` commands are available on your system. Additionally, it requires superuser (root) privileges to execute the `netstat` and `ip` commands. Make sure to run the script with appropriate privileges.

Let me know if you have any further questions!
--------------------------
```

```shell
#!/bin/zsh



# Get the default gateway for the VPN connection

VPN_GATEWAY=$(netstat -rn | grep -m1 -E '^0\.0\.0\.0' | awk '{print $2}')



# Get the IP address associated with the VPN gateway

VPN_IP=$(ip -br addr show | grep $VPN_GATEWAY | awk '{print $3}' | cut -d'/' -f1)



echo "VPN IP: $VPN_IP"

--------------------------
Saved to output.sh
```
