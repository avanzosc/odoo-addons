`1.3.5`
-------

- **Fix:** Fixed possibility to write inappropriate groups directly via write method after some odoo updates https://github.com/odoo/odoo/commit/5f12e244f6e57b8edb56788147774150e2ae134d

`1.3.4`
-------

- **Fix:** Allow superuser to write groups via settings menu

`1.3.3`
-------

- **Fix:** If no permission to add groups then just ignore write operations to groups model records but apply any other valid settings. In other words - do not block rest of the settings from applying if there is only no permission to add groups

`1.3.2`
-------

- **Fix:** regardless of ``Allow add implied groups from settings`` always allow to uncheck **group_XXX** fields from settings menu. This makes possible for ``access_apps`` module to independently install apps from settings menu. Otherwise users of ``access_apps`` need always be in ``Allow add implied...`` to install from settings

`1.3.1`
-------

- **Fix:** a user, if he has ``Allow add implied groups from settings`` group access right, should be able to uncheck **group_XXX** fields from a settings menu to exit from implied groups (all other users that are in implying group also quit from the implied group)

`1.3.0`
-------

- [ADD] security group that allows increasing rights from settings menu (by checking ``res.config.settings`` 'group_XXX' boolean fields)

`1.2.0`
-------

- [REF] clean and simplify code

`1.1.0`
-------

- ADD: Make restricted groups readonly in Settigs pages (res.config.settings)
- ADD: don't restrict access to Technical Settings group

`1.0.1`
-------

- FIX: update to the latest odoo 9.0 version due to this comit from Mar 24, 2016 https://github.com/odoo/odoo/commit/40a299c580c4608edab8781fda4e66f39611543b

`1.0.0`
-------

- init version
