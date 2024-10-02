from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    cannot_do_contract = fields.Boolean(
        string="Cannot Do Contract",
        compute="_compute_cannot_do_contract",
        store=False,
    )

    @api.depends('recurring_next_date', 'date_start', 'display_type')
    def _compute_cannot_do_contract(self):
        for line in self:
            # Si es una sección de línea, no se evalúa
            if line.display_type == "line_section":
                line.cannot_do_contract = False
                continue
                
            # Inicializar como False
            line.cannot_do_contract = False
            
            # Comprobar las fechas solo si están definidas
            if line.recurring_next_date and line.date_start:
                line.cannot_do_contract = line.date_start > line.recurring_next_date
