import json
from dataclasses import dataclass
from typing import List, Optional, Union

import requests

from ._login import LambdaFolder
from .constants import ENDPOINT


@dataclass
class InstanceType:
    def __init__(self, name, price_cents_per_hour, description, specs, regions_with_capacity_available):
        self.name = name
        self.price_cents_per_hour = price_cents_per_hour
        self.description = description
        self.specs = specs
        self.regions_with_capacity_available = regions_with_capacity_available

    def __repr__(self):
        return f"InstanceType(name={self.name}, price_cents_per_hour={self.price_cents_per_hour}, description={self.description})"


@dataclass
class SshKey:
    def __init__(self, id: str, name: str, public_key: str):
        self.id = id
        self.name = name
        self.public_key = public_key

    def __repr__(self):
        return f"SshKey(name={self.name})"


@dataclass
class Instance:
    def __init__(
        self,
        id: str,
        region: dict,
        instance_type: dict,
        status: str,
        ssh_key_names: List[str],
        file_system_names: List[str],
        name: Optional[str] = None,
        hostname: Optional[str] = None,
        ip: Optional[str] = None,
        jupyter_token: Optional[str] = None,
        jupyter_url: Optional[str] = None,
    ):
        self.id = id
        self.region = region
        self.instance_type = instance_type
        self.status = status
        self.ssh_key_names = ssh_key_names
        self.file_system_names = file_system_names
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.jupyter_token = jupyter_token
        self.jupyter_url = jupyter_url

    def __repr__(self):
        if self.name is None:
            return f"Instance(id={self.id}, status={self.status})"
        return f"Instance(id={self.id}, name={self.name}, status={self.status})"

    def delete(self, token: Optional[str] = None):
        return delete_instance(self.id, token=token)


class LambdaApi:
    def __init__(self, endpoint: Optional[str] = None, token: Optional[str] = None):
        self.endpoint = endpoint or ENDPOINT
        self.token = token

    def list_instance_types(self, show_all: bool = False, token=None):
        url = self.endpoint + "instance-types"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()["data"]
        instances = [
            InstanceType(regions_with_capacity_available=d["regions_with_capacity_available"], **d["instance_type"])
            for d in data.values()
        ]
        if show_all:
            return instances
        return [i for i in instances if i.regions_with_capacity_available]

    def create_instance(
        self,
        instance_type_name: str,
        ssh_key_names: Union[str, List[str]],
        file_system_names: Optional[Union[str, List[str]]] = None,
        region_name: Optional[str] = None,
        quantity: int = 1,
        token: Optional[str] = None,
    ):
        """Create a new Lambda Cloud VM instance.

        Args:
            instance_type_name (str): The name of the instance type to create.
            ssh_key_names (Union[str, List[str]]): The name (or names) of the SSH key to use for the instance.
            file_system_names (Optional[Union[str, List[str]]], optional): Name of file system to attach to instance. Defaults to None.
            region_name (Optional[str], optional): Region to launch the instance in. Defaults to None.
            quantity (int, optional): Number of instances of this type to create. Defaults to 1.
            token (Optional[str], optional): Your Lambda Labs API token. Defaults to None.

        Raises:
            ValueError: If the instance type is not found.
            ValueError: If the region is not available for the instance type.

        Returns:
            dict: The response from the API.
        """
        url = self.endpoint + "instance-operations/launch"
        headers = self._build_headers(token)
        instances = self.list_instance_types(token=token, show_all=False)
        instance = [i for i in instances if i.name == instance_type_name]
        if len(instance) == 0:
            raise ValueError(f"Instance type {instance_type_name} not found")
        instance = instance[0]

        if region_name is None:
            if len(instance.regions_with_capacity_available) == 0:
                raise ValueError(f"No regions available for instance type {instance_type_name}")
            region_name = instance.regions_with_capacity_available[0]["name"]

        if isinstance(ssh_key_names, str):
            ssh_key_names = [ssh_key_names]

        if isinstance(file_system_names, str):
            file_system_names = [file_system_names]
        elif file_system_names is None:
            file_system_names = []

        payload = dict(
            region_name=region_name,
            instance_type_name=instance_type_name,
            ssh_key_names=ssh_key_names,
            file_system_names=file_system_names,
            quantity=quantity,
        )
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]["instance_ids"]

    def list_instances(self, token: Optional[str] = None):
        """List all instances in your account.

        Args:
            token (Optional[str], optional): Your Lambda Labs API token. Defaults to None.

        Returns:
            List[dict]: The response from the API.
        """
        url = self.endpoint + "instances"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()["data"]
        instances = [Instance(**d) for d in data]
        return instances

    def get_instance(self, instance_id: str, token: Optional[str] = None):
        """Get information about a specific instance.

        Args:
            instance_id (str): The name of the instance to get information about.
            token (Optional[str], optional): Your Lambda Labs API token. Defaults to None.

        Returns:
            dict: The response from the API.
        """
        url = self.endpoint + "instances/" + instance_id
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()["data"]
        return Instance(**data)

    def delete_instance(self, instance_id, token: Optional[str] = None):
        """Delete an instance."""
        url = self.endpoint + "instance-operations/terminate"
        headers = self._build_headers(token)
        payload = {"instance_ids": [instance_id]}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]

    def list_ssh_keys(self, token: Optional[str] = None):
        """List all SSH keys in your account."""
        url = self.endpoint + "ssh-keys"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()["data"]
        return [SshKey(**d) for d in data]

    def add_ssh_key(self, name: str, public_key: str, token: Optional[str] = None):
        """Add an SSH key to your account."""
        url = self.endpoint + "ssh-keys"
        headers = self._build_headers(token)
        payload = {"name": name, "public_key": public_key}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]

    def add_ssh_key_from_file(self, name, public_key_file, token: Optional[str] = None):
        """Add an SSH key to your account from a file."""
        with open(public_key_file, "r") as f:
            public_key = f.read()
        return self.add_ssh_key(name, public_key, token=token)

    def _build_headers(self, token: Optional[str] = None):
        if token is None:
            token = self.token

        if token is None:
            token = LambdaFolder.get_token()

        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        return headers


api = LambdaApi()
list_instance_types = api.list_instance_types
create_instance = api.create_instance
list_instances = api.list_instances
get_instance = api.get_instance
delete_instance = api.delete_instance
list_ssh_keys = api.list_ssh_keys
add_ssh_key = api.add_ssh_key
add_ssh_key_from_file = api.add_ssh_key_from_file
