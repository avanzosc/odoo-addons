# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    model_name = 'hr.employee.supervised.year'
    model_id = env['ir.model']._get_id(model_name)
    cr.execute("""
        UPDATE calendar_event SET res_id = supervised_year_id,
                                  res_model = '%s',
                                  res_model_id = %s
        WHERE supervised_year_id IS NOT Null;
    """ % (model_name, model_id))
