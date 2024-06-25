# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _get_default_weight_uom(self):
        return self.env[
            "product.template"
        ]._get_weight_uom_name_from_ir_config_parameter()

    priority = fields.Selection(
        [
            ("0", "Very Low"),
            ("1", "Low"),
            ("2", "Normal"),
            ("3", "High"),
            ("4", "Very High"),
            ("5", "Super High"),
        ],
        string="Valuation",
        default="0",
        copy=False,
    )
    forklift = fields.Boolean(default=False, copy=False)
    download_unit = fields.Integer(copy=False)
    staff = fields.Integer(copy=False)
    crew = fields.Integer(copy=False)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    total_cost = fields.Float(copy=False)
    kilo_discount = fields.Float(copy=False)
    guide_number = fields.Char(copy=False)
    torista_id = fields.Many2one(
        string="Torista",
        comodel_name="res.partner",
        domain=lambda self: [
            ("category_id", "=", (self.env.ref("custom_descarga.torista_category").id))
        ],
    )
    slaughterer_ids = fields.Many2many(
        string="Slaughterer",
        comodel_name="res.partner",
        relation="rel_sacaline_slaughterer",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            (
                "category_id",
                "=",
                (self.env.ref("custom_descarga.slaughterer_category").id),
            )
        ],
    )
    hanger_ids = fields.Many2many(
        string="Hanger",
        comodel_name="res.partner",
        relation="rel_sacaline_hanger",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (self.env.ref("custom_descarga.hanger_category").id))
        ],
    )
    forklift_operator_ids = fields.Many2many(
        string="Forklift Operator",
        comodel_name="res.partner",
        relation="rel_sacaline_forklift",
        column1="partner_id",
        column2="saca_line_id",
        domain=lambda self: [
            ("category_id", "=", (self.env.ref("custom_descarga.forklift_category").id))
        ],
    )
    craw = fields.Float(copy=False)
    weight_uom_name = fields.Char(
        string="Weight UOM",
        default=_get_default_weight_uom,
        copy=False,
    )
    color_name = fields.Selection(
        string="Color",
        related="stage_id.color_name",
        store=True,
    )
    is_canceled = fields.Boolean(string="Canceled", default=False)
    waiting_reason = fields.Selection(
        selection=[
            ("failure", "Failure"),
            ("lunch", "Lunch"),
            ("truck_delay", "Truck Delay"),
        ],
        copy=False,
    )
    origin_qty = fields.Float(compute="_compute_origin_qty", store=True)
    dest_qty = fields.Float(compute="_compute_dest_qty", store=True)
    purchase_price = fields.Float(compute="_compute_puchase_price", store=True)
    purchase_unit_price = fields.Float(
        compute="_compute_puchase_unit_price", store=True
    )
    gross_origin = fields.Float(copy=False)
    tara_origin = fields.Float(copy=False)
    net_origin = fields.Float(compute="_compute_net_origin", store=True)
    average_weight_origin = fields.Float(
        compute="_compute_average_weight_origin",
        digits="Weight Decimal Precision",
        store=True,
    )
    gross_dest = fields.Float(string="Gross Dest.", copy=False)
    tara_dest = fields.Float(string="Tara Dest.", copy=False)
    net_dest = fields.Float(compute="_compute_net_dest", store=True)
    average_weight_dest = fields.Float(
        digits="Weight Decimal Precision",
        compute="_compute_average_weight_dest",
        store=True,
    )
    dif_gross = fields.Float(
        string="Diff. Gross", compute="_compute_dif_gross", store=True
    )
    dif_tara = fields.Float(
        string="Diff. Tara", compute="_compute_dif_tara", store=True
    )
    dif_net = fields.Float(string="Diff. Net", compute="_compute_dif_net", store=True)
    dif_average_weight = fields.Float(
        string="Diff. Averge Weight",
        digits="Weight Decimal Precision",
        compute="_compute_dif_average_weight",
        store=True,
    )
    distance_done = fields.Float(string="Kilometers", copy=False)
    is_presaca = fields.Boolean(compute="_compute_stage", store=True)
    is_saca = fields.Boolean(compute="_compute_stage", store=True)
    is_descarga = fields.Boolean(compute="_compute_stage", store=True)
    is_killing = fields.Boolean(compute="_compute_stage", store=True)
    is_classified = fields.Boolean(compute="_compute_stage", store=True)
    historic_line_ids = fields.One2many(
        string="Historic Lines",
        comodel_name="saca.line",
        inverse_name="historic_id",
        copy=False,
    )
    historic_id = fields.Many2one(
        string="Historic", comodel_name="saca.line", copy=False
    )
    hard_chicken = fields.Integer(string="Hard Chicken %", copy=False)
    yellowish_chicken = fields.Boolean(default=False)
    burned_leg = fields.Boolean(string="Burned Legs", default=False)
    dirt = fields.Boolean(default=False)
    count_historic = fields.Integer(compute="_compute_count_historic")
    descarga_order = fields.Char(
        string="Deccarga Order", compute="_compute_descarga_order"
    )
    img_origin = fields.Binary(string="Ticket Farm", attachment=True, copy=False)
    img_dest = fields.Binary(string="Ticket Slaughterhouse", copy=False)
    staff_crew = fields.Integer(copy=False)
    floor = fields.Selection(
        [("single", "Single"), ("top", "Top"), ("below", "Below")], copy=False
    )

    def _compute_descarga_order(self):
        for line in self:
            line.descarga_order = "0"
            saca_lines = line.saca_id.saca_line_ids.filtered(lambda c: c.unload_date)
            if saca_lines and line.unload_date:
                saca_lines = sorted(
                    saca_lines, key=lambda c: c.unload_date, reverse=False
                )
                position = saca_lines.index(line)
                line.descarga_order = "{}".format(position + 1)

    def _compute_count_historic(self):
        for line in self:
            line.count_historic = len(line.historic_line_ids)

    @api.depends("stage_id")
    def _compute_stage(self):
        for line in self:
            presaca = self.env.ref("custom_saca_purchase.stage_presaca")
            saca = self.env.ref("custom_saca_purchase.stage_saca")
            descarga = self.env.ref("custom_descarga.stage_descarga")
            matanza = self.env.ref("custom_descarga.stage_matanza")
            clasificado = self.env.ref("custom_descarga.stage_clasificado")
            line.is_presaca = False
            line.is_saca = False
            line.is_descarga = False
            line.is_killing = False
            line.is_classified = False
            if line.stage_id == presaca:
                line.is_presaca = True
                line.is_saca = False
                line.is_descarga = False
                line.is_killing = False
                line.is_classified = False
            if line.stage_id == saca:
                line.is_presaca = False
                line.is_saca = True
                line.is_descarga = False
                line.is_killing = False
                line.is_classified = False
            if line.stage_id == descarga:
                line.is_presaca = False
                line.is_saca = False
                line.is_descarga = True
                line.is_killing = False
                line.is_classified = False
            if line.stage_id == matanza:
                line.is_presaca = False
                line.is_saca = False
                line.is_descarga = False
                line.is_killing = True
                line.is_classified = False
            if line.stage_id == clasificado:
                line.is_presaca = False
                line.is_saca = False
                line.is_descarga = False
                line.is_killing = False
                line.is_classified = True

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
                line.average_weight_origin = line.net_origin / line.download_unit

    @api.depends("average_weight_origin", "average_weight_dest")
    def _compute_dif_average_weight(self):
        for line in self:
            line.dif_average_weight = (
                line.average_weight_dest - line.average_weight_origin
            )

    @api.depends("net_origin", "net_dest")
    def _compute_dif_net(self):
        for line in self:
            line.dif_net = line.net_dest - line.net_origin

    @api.depends("tara_origin", "tara_dest")
    def _compute_dif_tara(self):
        for line in self:
            line.dif_tara = line.tara_dest - line.tara_origin

    @api.depends("gross_origin", "gross_dest")
    def _compute_dif_gross(self):
        for line in self:
            line.dif_gross = line.gross_dest - line.gross_origin

    @api.depends("gross_origin", "tara_origin")
    def _compute_net_origin(self):
        for line in self:
            line.net_origin = line.gross_origin - line.tara_origin
            line.onchange_origin()

    @api.depends("gross_dest", "tara_dest")
    def _compute_net_dest(self):
        for line in self:
            line.net_dest = line.gross_dest - line.tara_dest

    @api.depends(
        "sale_order_id",
        "sale_order_id.picking_ids",
        "sale_order_id.picking_ids.move_ids_without_package",
        "sale_order_id.picking_ids.move_ids_without_package.quantity_done",
    )
    def _compute_origin_qty(self):
        for line in self:
            if (
                line.sale_order_id
                and (line.sale_order_id.picking_ids)
                and (line.sale_order_id.picking_ids[0].move_ids_without_package)
            ):
                line.origin_qty = (
                    line.sale_order_id.picking_ids[0]
                    .move_ids_without_package[0]
                    .quantity_done
                )

    @api.depends(
        "purchase_order_id",
        "purchase_order_id.picking_ids",
        "purchase_order_id.picking_ids.move_ids_without_package",
        "purchase_order_id.picking_ids.move_ids_without_package.quantity_done",
    )
    def _compute_dest_qty(self):
        for line in self:
            if (
                line.purchase_order_id
                and (line.purchase_order_id.picking_ids)
                and (line.purchase_order_id.picking_ids.move_ids_without_package)
            ):
                line.dest_qty = (
                    line.purchase_order_id.picking_ids[0]
                    .move_ids_without_package[0]
                    .quantity_done
                )

    @api.depends(
        "purchase_order_id",
        "purchase_order_id.order_line",
        "purchase_order_id.order_line.price_unit",
    )
    def _compute_puchase_unit_price(self):
        for line in self:
            if line.purchase_order_id and line.purchase_order_id.order_line:
                line.purchase_unit_price = line.purchase_order_id.order_line[
                    0
                ].price_unit

    @api.depends(
        "purchase_order_id",
        "purchase_order_id.amount_untaxed",
    )
    def _compute_puchase_price(self):
        for line in self:
            if line.purchase_order_id:
                line.purchase_price = line.purchase_order_id.amount_untaxed

    def write(self, values):
        result = super().write(values)
        if "download_unit" in values:
            for record in self:
                for line in record.move_line_ids:
                    line.download_unit = record.download_unit
                    for move in record.stock_move_ids:
                        move.download_unit = record.download_unit
        if "gross_origin" in (values) or "tara_origin" in (values) and self.net_origin:
            for line in self.stock_move_ids:
                line.product_uom_qty = self.net_origin
            for line in self.sudo().move_line_ids:
                line.qty_done = self.net_origin
                line.amount = line.qty_done * line.standard_price
            for line in self.sudo().purchase_order_line_ids:
                line.product_qty = self.net_origin
        return result

    @api.onchange("download_unit")
    def onchange_download_unit(self):
        if self.download_unit:
            for line in self.move_line_ids:
                line.download_unit = self.download_unit
            for move in self.stock_move_ids:
                move.download_unit = self.download_unit

    @api.onchange("staff")
    def onchange_staff(self):
        if self.staff:
            for line in self.saca_id.saca_line_ids:
                if not line.staff:
                    line.staff = self.staff

    @api.onchange("crew")
    def onchange_crew(self):
        if self.crew:
            for line in self.saca_id.saca_line_ids:
                if not line.crew:
                    line.crew = self.crew

    @api.onchange("slaughterer_ids")
    def onchange_slaughterer_ids(self):
        if self.slaughterer_ids:
            for line in self.saca_id.saca_line_ids:
                if not line.slaughterer_ids:
                    line.slaughterer_ids = [(6, 0, self.slaughterer_ids.ids)]

    @api.onchange("hanger_ids")
    def onchange_hanger_ids(self):
        if self.hanger_ids:
            for line in self.saca_id.saca_line_ids:
                if not line.hanger_ids:
                    line.hanger_ids = [(6, 0, self.hanger_ids.ids)]

    @api.onchange("forklift_operator_ids")
    def onchange_forklift_operator_ids(self):
        if self.forklift_operator_ids:
            for line in self.saca_id.saca_line_ids:
                if not line.forklift_operator_ids:
                    line.forklift_operator_ids = [
                        (6, 0, self.forklift_operator_ids.ids)
                    ]

    @api.onchange("gross_origin", "tara_origin", "download_unit")
    def onchange_origin(self):
        if self.breeding_id and self.breeding_id.estimate_weight_ids:
            line = self.breeding_id.estimate_weight_ids.filtered(
                lambda c: c.date == self.date
            )
            if line:
                line.write(
                    {
                        "saca_casualties": self.download_unit,
                        "real_weight": self.average_weight_origin * 1000,
                    }
                )

    def action_next_stage(self):
        self.ensure_one()
        stage_saca = self.env.ref("custom_saca_purchase.stage_saca")
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        stage_matanza = self.env.ref("custom_descarga.stage_matanza")
        stage_clasificado = self.env.ref("custom_descarga.stage_clasificado")
        if self.stage_id == stage_matanza:
            pickings = self.sudo().purchase_order_id.picking_ids + (
                self.sudo().sale_order_id.picking_ids
            )
            for picking in pickings:
                if picking.state != "done":
                    if not picking.custom_date_done:
                        picking.custom_date_done = self.date + timedelta(days=1)
                    picking.sudo().button_validate()
            self.write({"stage_id": stage_clasificado.id})
        elif self.stage_id == stage_descarga:
            for picking in self.sudo().sale_order_id.picking_ids:
                for move in picking.move_ids_without_package:
                    if self.sudo().breeding_id:
                        name = "{}".format(self.sudo().breeding_id.name)
                    else:
                        name = "E{}".format(self.lot)
                    lot = (
                        self.env["stock.production.lot"]
                        .sudo()
                        .search(
                            [
                                ("product_id", "=", move.product_id.id),
                                ("name", "=", name),
                                ("company_id", "=", picking.company_id.id),
                            ],
                            limit=1,
                        )
                    )
                    if not lot:
                        lot = (
                            self.env["stock.production.lot"]
                            .sudo()
                            .action_create_lot(
                                move.product_id, name, picking.company_id
                            )
                        )
                if picking.state != "done":
                    picking.custom_date_done = self.date + timedelta(days=1)
                    picking.action_confirm()
                    picking.action_assign()
                    picking.button_force_done_detailed_operations()
                    for line in picking.move_line_ids_without_package:
                        line.write(
                            {"lot_id": lot.id, "download_unit": self.download_unit}
                        )
                    picking.sudo().button_validate()
            for picking in self.purchase_order_id.picking_ids:
                picking.custom_date_done = self.date + timedelta(days=1)
                picking.button_force_done_detailed_operations()
                for line in picking.move_line_ids_without_package:
                    if not line.qty_done:
                        line.qty_done = line.move_id.product_uom_qty
                    if picking.picking_type_code == "incoming":
                        name = "{}{}".format(
                            line.saca_line_id.lot, line.saca_line_id.seq
                        )
                        lot = self.env["stock.production.lot"].search(
                            [
                                ("product_id", "=", line.product_id.id),
                                ("name", "=", name),
                                ("company_id", "=", picking.company_id.id),
                            ],
                            limit=1,
                        )
                        if not lot:
                            lot = self.env["stock.production.lot"].action_create_lot(
                                line.product_id, name, picking.company_id
                            )
                        line.lot_id = lot.id
                picking.sudo().button_validate()
            self.sudo().sale_order_id.commitment_date = self.date + timedelta(days=1)
            self.purchase_order_id.date_planned = self.date + timedelta(days=1)
            self.write({"stage_id": stage_matanza.id})
        elif self.stage_id == stage_saca:
            if not self.purchase_order_line_ids:
                raise ValidationError(_("There is no any purchase order line."))
            price = self.purchase_order_line_ids[0].price_unit
            self.purchase_order_id.sudo().button_confirm()
            if price:
                self.purchase_order_line_ids.sudo().price_unit = price
            type_normal = self.env["sale.order.type"].search(
                [
                    ("name", "ilike", "Normal"),
                    ("company_id", "=", self.sale_order_id.company_id.id),
                ],
                limit=1,
            )
            if type_normal:
                self.sale_order_id.sudo().type_id = type_normal.id
            for line in self.sale_order_id.picking_ids:
                line.sudo().batch_id = self.breeding_id.id
            if self.download_unit:
                for line in self.stock_move_ids.sudo():
                    line.sudo().download_unit = self.download_unit
                for line in self.move_line_ids.sudo():
                    line.sudo().download_unit = self.download_unit
            vals = {"stage_id": stage_descarga.id}
            if not self.unload_date:
                date = self.date
                time = datetime.now().time()
                time = time.strftime("%H:%M:%S")
                fecha = "{} {}".format(date, time)
                vals.update({"unload_date": fecha})
            self.sudo().write(vals)

    def action_create_purchase(self):
        result = super().action_create_purchase()
        stage_saca = self.env.ref("custom_saca_purchase.stage_saca")
        if self.stage_id == stage_saca:
            self.action_create_historic()
        return result

    def action_create_historic(self):
        self.ensure_one()
        stage_historico = self.env.ref("custom_descarga.stage_historico")
        historic = self.copy()
        historic.sudo().write(
            {
                "historic_id": self.id,
                "is_historic": True,
                "saca_id": False,
                "stage_id": stage_historico.id,
                "is_canceled": True,
            }
        )

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
            self.write({"stage_id": stage_cancelado.id})
        else:
            raise ValidationError(
                _(
                    "You cannot cancel because some products have already "
                    + "been delivered."
                )
            )

    def action_view_historic(self):
        context = self.env.context.copy()
        context.update({"default_historic_id": self.id})
        return {
            "name": _("Historics"),
            "view_mode": "tree,form",
            "res_model": "saca.line",
            "domain": [
                ("id", "in", self.historic_line_ids.ids),
                ("is_historic", "=", True),
            ],
            "type": "ir.actions.act_window",
            "context": context,
        }
