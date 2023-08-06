from pulumi_azure_native.storage import (
    NetworkRuleSetArgs as StorageNetworkRuleSetArgs,
    DefaultAction as StorageNetworkRuleSetDefaultAction,
)

from pulumi_azure_native.keyvault import (
    NetworkRuleSetArgs as KeyVaultNetworkRuleSetArgs,
)

key_vault_default_network_acl = KeyVaultNetworkRuleSetArgs(
    default_action="Allow",
    bypass="AzureServices",
    ip_rules=None,
    virtual_network_rules=None,
)

storage_default_network_acl = StorageNetworkRuleSetArgs(
    default_action=StorageNetworkRuleSetDefaultAction("Allow"),
    bypass="AzureServices",
    ip_rules=None,
    virtual_network_rules=None,
)

azure_iam_role_definitions = {
    # General
    "Owner": "/providers/Microsoft.Authorization/roleDefinitions/8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
    "Contributor": "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c",
    "Reader": "/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
    # Key Vault
    "Key Vault Administrator": "/providers/Microsoft.Authorization/roleDefinitions/00482a5a-887f-4fb3-b363-3b7fe8e74483",
    "Key Vault Secrets Reader": "/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86b69e6",
    # Storage
    "Storage Blob Data Owner": "/providers/Microsoft.Authorization/roleDefinitions/b7e6dc6d-f1e8-4753-8033-0f276bb0955b",
    "Storage Blob Data Contributor": "/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe",
    "Storage Blob Data Reader": "/providers/Microsoft.Authorization/roleDefinitions/2a2b9908-6ea1-4ae2-8e65-a410df84e7d1",
    "Storage Blob Delegator": "/providers/Microsoft.Authorization/roleDefinitions/db58b8e5-c6ad-4a2a-8342-4190687cbf4a",
}
