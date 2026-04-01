from odoo import _, api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_rebuild_stock(self):
        """
        Rebuilds the quants for the products (all variants of the template) based on
        stock.move.line records with state='done'.

        - Takes into account: location_id, location_dest_id, lot_id, package_id,
          owner_id.
        - Does not delete quants: sets the quantity of existing quants for the
          product(s) to 0 and then adds/subtracts according to the move lines.
        - If a quant for the combination does not exist, it creates one.

        Usage: button from the template form view.
        """
        self.ensure_one()

        product_ids = self.product_variant_ids.ids or [self.product_variant_id.id]
        if not product_ids:
            raise UserError(_("There are not variants for this product."))

        StockQuant = self.env["stock.quant"]
        MoveLine = self.env["stock.move.line"]

        quants = StockQuant.search([("product_id", "in", product_ids)])
        for quant in quants:
            if quant.quantity:
                StockQuant._update_available_quantity(
                    quant.product_id,
                    quant.location_id,
                    -quant.quantity,
                    lot_id=quant.lot_id or None,
                    package_id=quant.package_id or None,
                    owner_id=quant.owner_id or None,
                )

        move_lines = MoveLine.search(
            [("product_id", "in", product_ids), ("state", "=", "done")],
            order="date desc, id asc",
        )

        for ml in move_lines:
            qty = ml.quantity or 0.0
            if not qty:
                continue

            StockQuant._update_available_quantity(
                ml.product_id,
                ml.location_id,
                -qty,
                lot_id=ml.lot_id or None,
                package_id=ml.package_id or None,
                owner_id=ml.owner_id or None,
            )

            StockQuant._update_available_quantity(
                ml.product_id,
                ml.location_dest_id,
                qty,
                lot_id=ml.lot_id or None,
                package_id=ml.result_package_id or None,
                owner_id=ml.owner_id or None,
            )

        return True

    @api.model
    def cron_convert_all_consumables_and_rebuild_stock(self, limit=100):
        Product = self.env["product.template"].sudo()
        while True:
            products = Product.search(
                [("type", "=", "consu"), ("is_storable", "=", False)], limit=limit
            )
            if not products:
                break
            for record in products:
                self.env.cr.execute(
                    "UPDATE product_template SET is_storable = True WHERE id = %s",
                    (record.id,),
                )
                record.invalidate_recordset(["is_storable"])
                record.sudo().action_rebuild_stock()
            self.env.cr.flush()
