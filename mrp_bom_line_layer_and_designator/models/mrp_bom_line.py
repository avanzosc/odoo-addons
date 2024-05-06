# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    layer = fields.Char(string='Layer')
    designator = fields.Char(string='Designator')

    def init(self):
        if 'x_notes' in self._fields and 'x_designator' in self._fields:
            bom_lines = self.env['mrp.bom.line'].search(['|', ('x_notes', '!=', False), ('x_designator', '!=', False)])
            _logger.info("\n\nUpdating bom lines: %s", bom_lines)
            for line in bom_lines:
                vals = {}
                if line.x_notes and not line.layer:
                    vals['layer'] = line.x_notes
                    _logger.info("\n\nUpdated notes on bom line: %s", line)
                if line.x_designator and not line.designator:
                    vals['designator'] = line.x_designator
                    _logger.info("\n\nUpdated designator on bom line: %s", line)
                if vals:
                    line.write(vals)
                    _logger.info("\n\nUpdated bom line: %s", line)
        else:
            _logger.warning("Fields 'x_notes' and/or 'x_designator' do not exist in model 'mrp.bom.line'")
