# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _default_stage_id(self):
        try:
            return self.env.ref("custom_descarga.stage_saca").id
        except Exception:
            return False

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="saca.line.stage",
        default=_default_stage_id)
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
    amoun_farm = fields.Float(string="Amount Farm")
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
    task_ids = fields.One2many(
        string="Tasks",
        comodel_name="project.task",
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

    def write(self, vals):
        stage = self.env.ref("custom_descarga.stage_descarga")
        res = super(SacaLine, self).write(vals)
        if "stage_id" in vals and vals["stage_id"] == (
            stage.id) and not (
                self.task_ids):
            project = self.env.ref("custom_descarga.project_saca")
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Carga",
                "saca_line_id": self.id})
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Espera",
                "saca_line_id": self.id})
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Chofer",
                "saca_line_id": self.id})
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Matanza",
                "saca_line_id": self.id})
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Averías",
                "saca_line_id": self.id})
        return res
