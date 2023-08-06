import yamale
import hiyapyco as hco
from typing import Any
from hashlib import md5


class PlatformConfigurationException(Exception):
    ...


class PlatformConfiguration:
    def _validate_schema(self, schema_file_path: str, config: Any):
        schema = yamale.make_schema(schema_file_path)
        data = yamale.make_data(content=hco.dump(config))
        try:
            yamale.validate(schema, data)
            print("The configuration schema is valid. ✅")
        except ValueError as e:
            print(f"The configuration schema is NOT valid! ❌\n{e}")
            exit(1)

    def __init__(
        self,
        stack: str,
        schema_file_path: str,
        default_config_file_path: str,
        stack_config_file_path: str = None,
    ) -> None:

        # If no stack config file path is provided, we'll use the default config.
        if stack_config_file_path is None:
            stack_config_file_path = default_config_file_path

        # Merge the default + stack configs
        self.config_object = hco.load(
            [default_config_file_path, stack_config_file_path],
            method=hco.METHOD_MERGE,
        )

        # Validate the schema
        self._validate_schema(schema_file_path, self.config_object)

        region = self.config_object["general"]["region"].lower()
        if region not in self.azure_region_name_map:
            raise PlatformConfigurationException(
                f"Region name {region} not recognised."
            )

        self.stack = stack
        self.config_object = self.config_object
        self.prefix = self.config_object["general"]["prefix"]
        self.region_long_name = self.config_object["general"]["region"]
        self.region_short_name = self.azure_region_name_map[region]
        self.tags = self.config_object["general"]["tags"]
        self.unique_id = self.config_object["general"]["unique_id"]

    azure_region_name_map = {
        "eastus": "eus",
        "eastus2": "eus2",
        "centralus": "cus",
        "northcentralus": "ncus",
        "southcentralus": "scus",
        "westcentralus": "wcus",
        "westus": "wus",
        "westus2": "wus2",
        "westus3": "wus3",
        "australiaeast": "aue",
        "australiacentral": "auc",
        "australiacentral2": "auc2",
        "australiasoutheast": "ause",
        "southafricanorth": "san",
        "southafricawest": "saw",
        "centralindia": "cin",
        "southindia": "sin",
        "westindia": "win",
        "eastasia": "eas",
        "southeastasia": "seas",
        "japaneast": "jpe",
        "japanwest": "jpw",
        "jioindiawest": "jinw",
        "jioindiacentral": "jinc",
        "koreacentral": "koc",
        "koreasouth": "kos",
        "canadacentral": "cac",
        "canadaeast": "cae",
        "francecentral": "frc",
        "francesouth": "frs",
        "germanywestcentral": "gewc",
        "germanynorth": "gen",
        "norwayeast": "nwye",
        "norwaywest": "nwyw",
        "switzerlandnorth": "swn",
        "switzerlandwest": "sww",
        "uaenorth": "uaen",
        "uaecentral": "uaec",
        "brazilsouth": "brs",
        "brazilsoutheast": "brse",
        "northeurope": "neu",
        "westeurope": "weu",
        "swedencentral": "swec",
        "swedensouth": "swes",
        "uksouth": "uks",
        "ukwest": "ukw",
    }


class PlatformNameGenerator:
    def __init__(self, platform_config: PlatformConfiguration) -> None:
        self.platform_config = platform_config

    azure_resource_name_map = {
        "resource_group": "rg",
        "virtual_network": "vnet",
        "subnet": "snet",
        "route_table": "rt",
        "network_security_group": "nsg",
        "nat_gateway": "ngw",
        "public_ip": "pip",
        "private_endpoint": "pe",
        "databricks_workspace": "dbw",
        "databricks_cluster": "dbwc",
        "service_principal": "sp",
        "storage_blob_container": "sbc",
        "dns_zone": "dz",
        "private_dns_zone": "prdz",
        "datafactory": "adf",
    }

    def generate_resource_name(self, resource_type: str, resource_name: str) -> str:
        resource_type = resource_type.lower()
        if resource_type == "user_group":
            return f"{self.platform_config.prefix.upper()}-{self.platform_config.stack.title()}-{resource_name.title()}"
        elif resource_type == "gateway_subnet":
            return "Gateway"
        elif resource_type == "key_vault":
            return f"{self.platform_config.prefix}-{self.platform_config.stack}-{self.platform_config.region_short_name}-kv-{resource_name}-{self.platform_config.unique_id}"
        elif resource_type == "storage_account":
            return f"{self.platform_config.prefix}{self.platform_config.stack}{resource_name}{self.platform_config.unique_id}"
        elif resource_type in self.azure_resource_name_map:
            return f"{self.platform_config.prefix}-{self.platform_config.stack}-{self.platform_config.region_short_name}-{self.azure_resource_name_map[resource_type]}-{resource_name.lower()}"
        else:
            raise Exception(f"Resource type {resource_type} not recognised.")

    @classmethod
    def generate_hash(cls, *args: str) -> str:
        """
        This function takes arbitrary number of string arguments and returns an MD5 hash based on them.
        """
        concat = "".join(args).encode("utf-8")
        return md5(concat).hexdigest()
