# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
    )
    manufacturer_id = fields.Many2one(
        string="Manufacturer",
        comodel_name="res.partner",
        related="product_id.manufacturer",
        store=True,
    )
    model_id = fields.Many2one(string="Model", comodel_name="product.model")
    chassis_id = fields.Many2one(string="Chassis", comodel_name="chassis")
    part_number = fields.Char(string="Part Nº")
    size_id = fields.Many2one(string="Screen Size", comodel_name="screen.size")
    resolution_id = fields.Many2one(string="Resolution", comodel_name="resolution")
    processor_id = fields.Many2one(string="Processor", comodel_name="processor")
    speed_id = fields.Many2one(string="Speed", comodel_name="speed")
    gen_id = fields.Many2one(string="Gen", comodel_name="gen")
    ram_id = fields.Many2one(string="RAM", comodel_name="ram")
    storage1_size_id = fields.Many2one(
        string="Storage 1 Size", comodel_name="storage.size"
    )
    storage1_type_id = fields.Many2one(
        string="Storage 1 Type", comodel_name="storage.type"
    )
    storage1_model = fields.Char(string="Storage 1 Model")
    storage1_serial = fields.Char(string="Storage 1 Serial")
    optical = fields.Char(string="Optical")
    keyb_id = fields.Many2one(string="Keyboard", comodel_name="keyboard")
    webcam = fields.Integer(string="Webcam")
    videocard = fields.Char(string="Videocard")
    videocard2 = fields.Char(sting="Videocard2")
    coa_id = fields.Many2one(string="COA", comodel_name="software.license.key")
    os_restore = fields.Char(string="OS Restored")
    observ_code = fields.Char(string="Observ Code")
    observ_notes = fields.Text(string="Observ Notes")
    grade_id = fields.Many2one(string="Grade", comodel_name="grade")
    grade_tested = fields.Selection(
        selection=[("ok", "OK"), ("no_ok", "No OK")],
        string="Grade tested",
        related="grade_id.tested",
        store=True,
        copy=False,
    )
    ram1_size_id = fields.Many2one(string="RAM 1 Size", comodel_name="storage.size")
    ram1_type_id = fields.Many2one(string="RAM 1 Type", comodel_name="ram.type")
    storage2_size = fields.Many2one(
        string="Storage 2 Size", comodel_name="storage.size"
    )
    ram2_size_id = fields.Many2one(string="RAM 2 Size", comodel_name="storage.size")
    ram2_type_id = fields.Many2one(string="RAM 2 Type", comodel_name="ram.type")
    battery_duration = fields.Char(string="Battery Duration")
    coa_number = fields.Char(string="COA Number")
    coa_serial = fields.Char(string="COA Serial")
    battery_model_id = fields.Many2one(
        string="Battery Model", comodel_name="battery.model"
    )
    battery_size = fields.Integer(string="Battery Size")
    battery_charge = fields.Text(string="Battery Charge")
    battery_cycles = fields.Char(string="Battery Cycles")
    lan = fields.Char(string="LAN")
    wifi = fields.Boolean(string="Wifi", default=False)
    bluetooth = fields.Boolean(string="Bluetooth", default=False)
    wwan = fields.Boolean(string="WWAN", default=False)
    touch_screen = fields.Boolean(string="Touch Screen", default=False)
    ram_slots = fields.Char(string="RAM Slots")
    ram1_serial = fields.Char(string="RAM 1 Serial")
    ram2_serial = fields.Char(string="RAM 2 Serial")
    storage2_type_id = fields.Many2one(
        string="Storage 2 Type", comodel_name="storage.type"
    )
    coa_part = fields.Char(string="COA Parts")
    lot_compotent_ids = fields.One2many(
        string="Lot Components", comodel_name="lot.component", inverse_name="lot_id"
    )
    purchase_order_id = fields.Many2one(
        string="Purchase Order", comodel_name="purchase.order"
    )
