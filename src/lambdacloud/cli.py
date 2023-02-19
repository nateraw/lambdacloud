import fire
from tabulate import tabulate

from ._login import login
from .lambda_api import create_instance, delete_instance, list_instance_types, list_instances


def cli_list_instance_types():
    """List available instance types."""
    instances = list_instance_types()
    print("Available instance types:")

    tabular_data = {"name": [], "price": [], "description": []}
    for instance in instances:
        tabular_data["name"].append(instance.name)
        tabular_data["price"].append(f"${instance.price_cents_per_hour / 100:-2.2f}")
        tabular_data["description"].append(instance.description)

    print(tabulate(tabular_data, headers=list(tabular_data), tablefmt="github"))


def main():
    fire.Fire(
        {
            "login": login,
            "instance_types": cli_list_instance_types,
            "list": list_instances,
            "create": create_instance,
            "delete": delete_instance,
        }
    )
