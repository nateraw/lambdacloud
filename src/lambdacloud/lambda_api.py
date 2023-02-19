import json
from dataclasses import dataclass

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
        return f"InstanceType(name={self.name}, price_cents_per_hour={self.price_cents_per_hour}, description={self.description}, specs={self.specs}, regions_with_capacity_available={self.regions_with_capacity_available})"


class LambdaApi:
    def __init__(self, endpoint=None, token=None):
        self.endpoint = endpoint or ENDPOINT
        self.token = token

    def list_instance_types(self, token=None, show_all=False):
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
        instance_type_name,
        *,
        ssh_key_names=None,
        file_system_names=None,
        region_name=None,
        quantity=1,
        token=None,
    ):
        url = self.endpoint + "instance-operations/launch"
        headers = self._build_headers(token)
        instances = self.list_instance_types(token=token, show_all=False)
        instance = [i for i in instances if i.name == instance_type_name]
        if len(instance) == 0:
            raise ValueError(f"Instance type {instance_type_name} not found")
        instance = instance[0]
        if region_name is None:
            region_name = instance.regions_with_capacity_available[0]["name"]

        payload = {}
        if region_name is not None:
            payload["region_name"] = region_name
        else:
            raise ValueError("Must specify region_name")
        payload["instance_type_name"] = instance_type_name
        payload["ssh_key_names"] = ssh_key_names or []
        payload["file_system_names"] = file_system_names or []
        payload["quantity"] = quantity

        print(json.dumps(payload, indent=2, sort_keys=False))
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]["instance_ids"]

    def list_instances(self, token=None):
        url = self.endpoint + "instances"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()["data"]

    def get_instance(self, instance_id, token=None):
        url = self.endpoint + "instances/" + instance_id
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()["data"]

    def delete_instance(self, instance_id, token=None):
        url = self.endpoint + "instance-operations/terminate"
        headers = self._build_headers(token)
        payload = {"instance_ids": [instance_id]}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]

    def list_ssh_keys(self, token=None):
        url = self.endpoint + "ssh-keys"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()["data"]

    def add_ssh_key(self, name, public_key, token=None):
        url = self.endpoint + "ssh-keys"
        headers = self._build_headers(token)
        payload = {"name": name, "public_key": public_key}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()["data"]

    def list_file_systems(self, token=None):
        url = self.endpoint + "file-systems"
        headers = self._build_headers(token)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()["data"]

    def _build_headers(self, token=None):
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
delete_instance = api.delete_instance
