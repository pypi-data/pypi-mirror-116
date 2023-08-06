# Thorgate Bitwarden password helper

Use with (for example) ansible vault to allow automatically
getting password from bitwarden instead of copying it over.

## Usage with ansible

Example ansible.cfg (considering you added tg-bw-helper with poetry):

```
[defaults]
vault_password_file=./ask-vault-pass.sh
```

ask-vault-pass.sh (needs to be executable):
```shell
#!/bin/sh
poetry run python -m tg_bw_helper --vault-item "Thorgate Ansible vault" --vault-entry-field "Main ansible"
```

## Parameters

* `--bw-executable` optional, should point to bw executable, defaults to /usr/bin/bw, can also be set with `TG_BW_AP_EXECUTABLE_PATH` env variable
* `--fallback-prompt` optional, prompt to display if bw fails, defaults to "Vault password: ", can also be set with `TG_BW_AP_FALLBACK_PROMPT` env variable
* `--vault-item` vault item ID or name, should be specific since tool will fail if multiple items are found
* `--vault-item-field`, optional, field to use on the item. If not specified, password is used
