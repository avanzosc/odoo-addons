# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    priority = fields.Selection([
        ("0", "Very Low"),
        ("1", "Low"),
        ("2", "Normal"),
        ("3", "High"),
        ("4", "Very High"),
        ("5", "Super High")],
        string="Valuation",
        default="0")
    forklift = fields.Boolean(string="Forklift", default=False)
    download_unit = fields.Integer(string="Download Unit")
    carriage = fields.Float(string="Carriage")
    amount_farm = fields.Float(string="Amount Farm")
    staff = fields.Integer(string="Staff")
    crew = fields.Integer(string="Crew")
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)
    total_cost = fields.Float(string="Total Cost")
    kilo_discount = fields.Float(string="Kilo discount")
    guide_number = fields.Char(string="Guide Number")
    torista_id = fields.Many2one(
        string="Torista",
        comodel_name="res.partner",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.torista_category").id))])
    slaughterer_ids = fields.Many2many(
        string="Slaughterer",
        comodel_name="res.partner",
        relation="rel_sacaline_slaughterer",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.slaughterer_category").id))])
    hanger_ids = fields.Many2many(
        string="Hanger",
        comodel_name="res.partner",
        relation="rel_sacaline_hanger",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.hanger_category").id))])
    forklift_operator_ids = fields.Many2many(
        string="Forklift Operator",
        comodel_name="res.partner",
        relation="rel_sacaline_forklift",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.forklift_category").id))])
    clasification = fields.Selection(
        string="Clasification", selection=[
            ("normal", "Normal"),
            ("relaxed", "Relaxed"),
            ("demanding", "Demanding")])
    craw = fields.Float(string="Craw")
    weight_uom_name = fields.Char(
        string='Weight UOM', default=_get_default_weight_uom)
    killing_staff = fields.Integer(string="Killing Stuff")
    timesheet_ids = fields.One2many(
        string="Timesheet",
        comodel_name="account.analytic.line",
        inverse_name="saca_line_id")
    color_name = fields.Selection(
        string="Color",
        selection=[
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green"),
            ("yellow", "Yellow"),
            ("gray", "Gray"),
            ("purple", "Purple")],
        related="stage_id.color_name",
        store="True")
    is_canceled = fields.Boolean(string="Canceled", default=False)
    production_ids = fields.One2many(
        string="Production",
        comodel_name="mrp.production",
        inverse_name="saca_line_id")

    def action_next_stage(self):
        self.ensure_one()
        stage_saca = self.env.ref("custom_saca_purchase.stage_saca")
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        stage_matanza = self.env.ref("custom_descarga.stage_matanza")
        stage_clasificado = self.env.ref("custom_descarga.stage_clasificado")
        stage_despiece = self.env.ref("custom_descarga.stage_despiece")
        if self.stage_id == stage_clasificado:
            for line in self.move_line_ids.filtered(lambda c: not c.move_id.sale_line_id):
                bom = self.env["mrp.bom"].search(
                    [("product_tmpl_id", "=", line.product_id.product_tmpl_id.id)],
                    limit=1)
                production = self.env["mrp.production"].create({
                    "bom_id": bom.id,
                    "product_id": line.product_id.id,
                    "product_uom_id": line.product_uom_id.id,
                    "product_qty": line.qty_done,
                    "saca_line_id": self.id
                    })
                production._onchange_move_raw()
            self.write({
                "stage_id": stage_despiece.id})
        if self.stage_id == stage_matanza:
            for picking in self.purchase_order_id.picking_ids:
                for line in picking.move_line_ids_without_package:
                    if not line.lot_id:
                        lot = self.env["stock.production.lot"].create({
                            "name": u'{}{}'.format(line.saca_line_id.lot, line.saca_line_id.seq),
                            "product_id": line.product_id.id,
                            "company_id": picking.company_id.id})
                        line.lot_id = lot.id
                    if not line.qty_done:
                        line.qty_done = line.move_id.product_uom_qty
                picking.button_validate()
            self.write({
                "stage_id": stage_clasificado.id})
        if self.stage_id == stage_descarga:
            for picking in self.sale_order_id.picking_ids:
                picking.button_force_done_detailed_operations()
                for line in picking.move_line_ids_without_package:
                    lot = self.env["stock.production.lot"].create({
                        "name": u'{}{}'.format(line.saca_line_id.lot, line.saca_line_id.seq),
                        "product_id": line.product_id.id,
                        "company_id": picking.company_id.id})
                    line.lot_id = lot.id
                picking.button_validate()
            self.write({
                "stage_id": stage_matanza.id})
        if self.stage_id == stage_saca:
            if not self.purchase_order_line_ids:
                raise ValidationError(
                    _("There is no any purchase order line.")
                )
            if not self.timesheet_ids:
                project = self.env.ref("custom_descarga.project_saca")
                today = fields.Date.today()
                cond = [('user_id', '=', self.env.user.id)]
                employee = self.env['hr.employee'].search(cond, limit=1)
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": u'{} {}'.format("Carga", self.name),
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Carga"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": u'{} {}'.format("Espera", self.name),
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Espera"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": u'{} {}'.format("Chofer", self.name),
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Chofer"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": u'{} {}'.format("Matanza", self.name),
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Matanza"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": u'{} {}'.format("Corte", self.name),
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Corte"),
                        "project_id": project.id})]})
            self.purchase_order_id.button_confirm()
            self.write({
                "stage_id": stage_descarga.id})

    def action_cancel(self):
        self.ensure_one()
        stage_presaca = self.env.ref("custom_saca_purchase.stage_presaca")
        stage_saca = self.env.ref("custom_saca_purchase.stage_saca")
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        stage_cancelado = self.env.ref("custom_descarga.stage_cancelado")
        if self.stage_id in (stage_presaca, stage_saca, stage_descarga):
            self.is_canceled = True
            for move in self.stock_move_ids:
                move.picking_id.action_cancel()
            if self.sale_order_id:
                self.sale_order_id.action_cancel()
            if self.purchase_order_id:
                self.purchase_order_id.button_cancel()
            self.write({
                "stage_id": stage_cancelado.id})
        else:
            raise ValidationError(
                _("You cannot cancel because some products have already been delivered."))
