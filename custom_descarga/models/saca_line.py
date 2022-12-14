# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


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
        default="0",
        copy=False)
    forklift = fields.Boolean(string="Forklift", default=False, copy=False)
    download_unit = fields.Integer(string="Download Unit", copy=False)
    staff = fields.Integer(string="Staff", copy=False)
    crew = fields.Integer(string="Crew", copy=False)
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id,
        copy=False)
    total_cost = fields.Float(string="Total Cost", copy=False)
    kilo_discount = fields.Float(string="Kilo discount", copy=False)
    guide_number = fields.Char(string="Guide Number", copy=False)
    torista_id = fields.Many2one(
        string="Torista",
        comodel_name="res.partner",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.torista_category").id))],
        copy=False)
    slaughterer_ids = fields.Many2many(
        string="Slaughterer",
        comodel_name="res.partner",
        relation="rel_sacaline_slaughterer",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.slaughterer_category").id))],
        copy=False)
    hanger_ids = fields.Many2many(
        string="Hanger",
        comodel_name="res.partner",
        relation="rel_sacaline_hanger",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.hanger_category").id))],
        copy=False)
    forklift_operator_ids = fields.Many2many(
        string="Forklift Operator",
        comodel_name="res.partner",
        relation="rel_sacaline_forklift",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (
                self.env.ref("custom_descarga.forklift_category").id))],
        copy=False)
    clasification = fields.Selection(
        string="Clasification", selection=[
            ("normal", "Normal"),
            ("relaxed", "Relaxed"),
            ("demanding", "Demanding")],
        copy=False)
    craw = fields.Float(string="Craw", copy=False)
    weight_uom_name = fields.Char(
        string='Weight UOM', default=_get_default_weight_uom, copy=False)
    killing_staff = fields.Integer(string="Killing Stuff", copy=False)
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
    channel_temperature = fields.Float(
        string="Channel Temperature",
        copy=False)
    waiting_reason = fields.Selection(
        string="Waiting Reason", selection=[
            ("failure", "Failure"),
            ("lunch", "Lunch")],
        copy=False)
    waiting_time = fields.Float(string="Waiting Time", copy=False)
    origin_qty = fields.Float(
        string="Origin Qty",
        compute="_compute_origin_qty",
        store=True)
    dest_qty = fields.Float(
        string="Dest Qty",
        compute="_compute_dest_qty",
        store=True)
    purchase_price = fields.Float(
        string="Purchase Price",
        compute="_compute_puchase_price",
        store=True)
    purchase_unit_price = fields.Float(
        string="Purchase Unit Price",
        compute="_compute_puchase_unit_price",
        store=True)
    gross_origin = fields.Float(string="Gross Origin", copy=False)
    tara_origin = fields.Float(string="Tara Oringin", copy=False)
    net_origin = fields.Float(
        string="Net Origin", compute="_compute_net_origin", store=True)
    average_weight_origin = fields.Float(
        string="Average Weight Origin",
        compute="_compute_average_weight_origin",
        digits=dp.get_precision("Weight Decimal Precision"),
        store=True)
    gross_dest = fields.Float(string="Gross Dest.", copy=False)
    tara_dest = fields.Float(string="Tara Dest.", copy=False)
    net_dest = fields.Float(
        string="Net Dest", compute="_compute_net_dest", store=True)
    average_weight_dest = fields.Float(
        string="Average Weight Dest",
        digits=dp.get_precision("Weight Decimal Precision"),
        compute="_compute_average_weight_dest",
        store=True)
    dif_gross = fields.Float(
        string="Diff. Gross", compute="_compute_dif_gross", store=True)
    dif_tara = fields.Float(
        string="Diff. Tara", compute="_compute_dif_tara", store=True)
    dif_net = fields.Float(
        string="Diff. Net", compute="_compute_dif_net", store=True)
    dif_average_weight = fields.Float(
        string="Diff. Averga Weight",
        digits=dp.get_precision("Weight Decimal Precision"),
        compute="_compute_dif_average_weight", store=True)
    distance_done = fields.Float(
        string="Kilometers")

    @api.depends("download_unit", "net_dest")
    def _compute_average_weight_dest(self):
        for line in self:
            line.average_weight_dest = 0
            if line.download_unit != 0:
                line.average_weight_dest = line.net_dest / line.download_unit

    @api.depends("download_unit", "net_origin")
    def _compute_average_weight_origin(self):
        for line in self:
            line.average_weight_origin = 0
            if line.download_unit != 0:
                line.average_weight_origin = (
                    line.net_origin / line.download_unit)

    @api.depends("average_weight_origin", "average_weight_dest")
    def _compute_dif_average_weight(self):
        for line in self:
            line.dif_average_weight = (
                line.average_weight_origin - line.average_weight_dest)

    @api.depends("net_origin", "net_dest")
    def _compute_dif_net(self):
        for line in self:
            line.dif_net = line.net_origin - line.net_dest

    @api.depends("tara_origin", "tara_dest")
    def _compute_dif_tara(self):
        for line in self:
            line.dif_tara = line.tara_origin - line.tara_dest

    @api.depends("gross_origin", "gross_dest")
    def _compute_dif_gross(self):
        for line in self:
            line.dif_gross = line.gross_origin - line.gross_dest

    @api.depends("gross_origin", "tara_origin")
    def _compute_net_origin(self):
        for line in self:
            line.net_origin = line.gross_origin - line.tara_origin

    @api.depends("gross_dest", "tara_dest")
    def _compute_net_dest(self):
        for line in self:
            line.net_dest = line.gross_dest - line.tara_dest

    @api.depends("sale_order_id", "sale_order_id.picking_ids",
                 "sale_order_id.picking_ids.move_ids_without_package",
                 "sale_order_id.picking_ids.move_ids_without_package.quantity_done")
    def _compute_origin_qty(self):
        for line in self:
            if line.sale_order_id and line.sale_order_id.picking_ids and line.sale_order_id.picking_ids[0].move_ids_without_package:
                line.origin_qty = line.sale_order_id.picking_ids[0].move_ids_without_package[0].quantity_done

    @api.depends("purchase_order_id", "purchase_order_id.picking_ids",
                 "purchase_order_id.picking_ids.move_ids_without_package",
                 "purchase_order_id.picking_ids.move_ids_without_package.quantity_done")
    def _compute_dest_qty(self):
        for line in self:
            if line.purchase_order_id and line.purchase_order_id.picking_ids and line.purchase_order_id.picking_ids.move_ids_without_package:
                line.dest_qty = line.purchase_order_id.picking_ids[0].move_ids_without_package[0].quantity_done

    @api.depends("purchase_order_id",
                 "purchase_order_id.order_line",
                 "purchase_order_id.order_line.price_unit")
    def _compute_puchase_unit_price(self):
        for line in self:
            if line.purchase_order_id and line.purchase_order_id.order_line:
                line.purchase_unit_price = (
                    line.purchase_order_id.order_line[0].price_unit)

    @api.depends("purchase_order_id",
                 "purchase_order_id.amount_untaxed")
    def _compute_puchase_price(self):
        for line in self:
            if line.purchase_order_id:
                line.purchase_price = line.purchase_order_id.amount_untaxed

    def action_create_lot(self, product, name, company):
        lot = self.env["stock.production.lot"].create(
            {"name": name,
             "product_id": product.id,
             "company_id": company.id})
        return lot

    def write(self, values):
        result = super(SacaLine, self).write(values)
        if "gross_origin" in values or "tara_origin" in values and self.net_origin:
            for line in self.purchase_order_line_ids:
                line.product_qty = self.net_origin
            for line in self.stock_move_ids:
                line.product_uom_qty = self.net_origin
        return result

    def action_next_stage(self):
        self.ensure_one()
        stage_saca = self.env.ref("custom_saca_purchase.stage_saca")
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        stage_matanza = self.env.ref("custom_descarga.stage_matanza")
        stage_clasificado = self.env.ref("custom_descarga.stage_clasificado")
        stage_despiece = self.env.ref("custom_descarga.stage_despiece")
        if self.stage_id == stage_clasificado:
            self.write({
                "stage_id": stage_despiece.id})
        elif self.stage_id == stage_matanza:
            pickings = (
                self.purchase_order_id.picking_ids + (
                    self.sale_order_id.picking_ids))
            for picking in pickings:
                for line in picking.move_line_ids_without_package:
                    if not line.qty_done:
                        line.qty_done = line.move_id.product_uom_qty
                    if not line.lot_id and (
                        picking.picking_type_code) == (
                            "incoming"):
                        name = u'{}{}'.format(
                            line.saca_line_id.lot, line.saca_line_id.seq)
                        line.lot_id = self.action_create_lot(
                            line.product_id, name, picking.company_id).id
                if picking.state != "done":
                    picking.button_validate()
            self.write({
                "stage_id": stage_clasificado.id})
        elif self.stage_id == stage_descarga:
            for picking in self.sale_order_id.picking_ids:
                picking.custom_date_done = self.date
                picking.button_force_done_detailed_operations()
                for line in picking.move_line_ids_without_package:
                    name = u'{}{}'.format(
                        line.saca_line_id.lot, line.saca_line_id.seq)
                    line.lot_id = self.action_create_lot(
                        line.product_id, name, picking.company_id).id
                picking.button_validate()
            for picking in self.purchase_order_id.picking_ids:
                picking.custom_date_done = self.date
            self.write({
                "stage_id": stage_matanza.id})
        elif self.stage_id == stage_saca:
            if not self.purchase_order_line_ids:
                raise ValidationError(
                    _("There is no any purchase order line.")
                )
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
