# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def uninstall_hook(env):
    env["product.attribute"].with_context(active_test=False).search(
        [("hide_in_configuration", "=", True)]
    ).hide_in_configuration = False
