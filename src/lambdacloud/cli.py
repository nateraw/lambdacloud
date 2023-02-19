import fire

from ._login import login
from .lambda_api import create_instance, delete_instance, list_instance_types, list_instances


def cli_list_instance_types():
    instances = list_instance_types()
    print("Available instance types:")
    for instance in instances:
        print(
            f"  - {instance.name}, Price: {instance.price_cents_per_hour / 100:.2f} USD/hour, Description: {instance.description}"
        )


def main():
    fire.Fire(
        {
            "login": login,
            "list_instance_types": cli_list_instance_types,
            "list": list_instances,
            "create": create_instance,
            "delete": delete_instance,
        }
    )
