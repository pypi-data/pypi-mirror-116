# TEW-652BRP

#### Python interface for working with the TEW-652BRP router API 

## Installation
```bash
pip install tew652brp
```

## Usage
```python
import getpass

from tew652brp.client import Client


# Session creation
client = Client('http://192.168.10.1')

# Enter your data
username = input('Username: ')
password = getpass.getpass()

# Try to login
if client.login.login(username, password):

    # Get all virtual servers
    virtual_servers = client.virtual.get_servers()

    # Turns on all virtual servers
    for server in virtual_servers:
        server.enabled = 1
        client.virtual.update_server(server)
```