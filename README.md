# lambdacloud

An unofficial python client for Lambda Lab's cloud computing platform.

## Installation

```
pip install lambdacloud
```

## Usage

#### Authenticate

```python
from lambdacloud import login

login(token="<your token>")
```

#### Create an Instance

See [here](#list-available-instance-types) for a list of available instance types. Also, see [here](#list-available-ssh-keys) for a list of available ssh keys.

```python
```python
from lambdacloud import create_instance

instance_id = create_instance("gpu_1x_a10", ssh_key_names="my-ssh-key")
print(instance_id)
"""
["<instance id>"]
"""
```

#### Delete an Instance

```python
from lambdacloud import delete_instance

delete_instance("<instance id>")
```

#### List Instances

```python
from lambdacloud import list_instances

instances = list_instances()
print(instances)
```

#### List Available Instance Types

```python
from lambdacloud import list_instance_types

instance_types = list_instance_types()
for instance_type in instance_types:
    print(instance_type)
"""
InstanceType(name=gpu_8x_a100_80gb_sxm4, price_cents_per_hour=1200, description=8x A100 (80 GB SXM4))
InstanceType(name=gpu_1x_a10, price_cents_per_hour=60, description=1x A10 (24 GB PCIe))
InstanceType(name=gpu_1x_a100_sxm4, price_cents_per_hour=110, description=1x A100 (40 GB SXM4))
InstanceType(name=gpu_8x_a100, price_cents_per_hour=880, description=8x A100 (40 GB SXM4))
InstanceType(name=gpu_8x_v100, price_cents_per_hour=440, description=8x Tesla V100 (16 GB))
"""

# To show all instance types, even if they are not available to create
instance_types = list_instance_types(show_all=True)
```

#### List Available SSH Keys

```python
from lambdacloud import list_ssh_keys

ssh_keys = list_ssh_keys()
for ssh_key in ssh_keys:
    print(ssh_key)

"""
SshKey(name=my-ssh-key)
"""
```

#### Add an SSH Key

```python
from lambdacloud import add_ssh_key

add_ssh_key("my-ssh-key", "<public key>")
```

#### Add an SSH Key from a File

```python
from lambdacloud import add_ssh_key_from_file

add_ssh_key_from_file("my-ssh-key", "<path to public key file>")
```

## Credits

This package is heavily inspired by [huggingface_hub](https://github.com/huggingface/huggingface_hub)
