`1.3.3`
-------
- **Fix:** Grant `Allow installing apps` to Admin and System users (it was only System)

`1.3.2`
-------

- **Fix:** allow users in group `Allow install apps only from settings` also to uninstall from settings
- **Fix:** `Allow install apps only from settings` security group should imply `Administration: Settings` - no access to settings otherwise

`1.3.1`
-------

- **Fix:** `Access Error` when administrators without access to apps trying to open ``[[ Website Admin ]] >> Configuratiion >> Settings``

`1.3.0`
-------

- **Fix:** the "Allow install apps" group is now implies "Administration: Settings" ("base.group_system") since in Odoo 11.0 only group_system users can install apps

`1.2.0`
-------

- **Improvement:** rename "Show Apps Menu" to "Allow install apps"
- **New:** "Allow install apps only from settings"
- **Improvement:** group "Show Apps Menu" and "Allow install apps only from settings" under "Apps access" security category

`1.0.1`
-------

- **Fix:** updates for recent odoo 9.0
- **Improvement:** apps dashboard can be showed if user has access 'Show Apps Menu'
