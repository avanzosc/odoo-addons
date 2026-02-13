from odoo import _, api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_rebuild_stock(self):
        """
        Rebuilds the quants for the products (all variants of the template) based on
        stock.move.line records with state='done'.

        - Takes into account: location_id, location_dest_id, lot_id, package_id, owner_id.
        - Does not delete quants: sets the quantity of existing quants for the product(s) to 0
          and then adds/subtracts according to the move lines.
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
        quants.write({"quantity": 0.0})

        move_lines = MoveLine.search(
            [("product_id", "in", product_ids), ("state", "=", "done")],
            order="date desc, id asc",
        )

        for ml in move_lines:
            qty = ml.qty_done or 0.0
            if not qty:
                continue

            origin_domain = [
                ("product_id", "=", ml.product_id.id),
                ("location_id", "=", ml.location_id.id),
                ("lot_id", "=", ml.lot_id.id or False),
                ("owner_id", "=", ml.owner_id.id or False),
                ("package_id", "=", ml.package_id.id or False),
            ]

            origin_quant = StockQuant.search(origin_domain, limit=1)

            if origin_quant:
                origin_quant.quantity -= qty
            else:
                StockQuant.create(
                    {
                        "product_id": ml.product_id.id,
                        "location_id": ml.location_id.id,
                        "lot_id": ml.lot_id.id or False,
                        "owner_id": ml.owner_id.id or False,
                        "package_id": ml.package_id.id or False,
                        "quantity": -qty,
                        "company_id": ml.company_id.id or self.env.company.id,
                    }
                )

            dest_domain = [
                ("product_id", "=", ml.product_id.id),
                ("location_id", "=", ml.location_dest_id.id),
                ("lot_id", "=", ml.lot_id.id or False),
                ("owner_id", "=", ml.owner_id.id or False),
                ("package_id", "=", ml.result_package_id.id or False),
            ]

            dest_quant = StockQuant.search(dest_domain, limit=1)

            if dest_quant:
                dest_quant.quantity += qty
            else:
                StockQuant.create(
                    {
                        "product_id": ml.product_id.id,
                        "location_id": ml.location_dest_id.id,
                        "lot_id": ml.lot_id.id or False,
                        "owner_id": ml.owner_id.id or False,
                        "package_id": ml.result_package_id.id or False,
                        "quantity": qty,
                        "company_id": ml.company_id.id or self.env.company.id,
                    }
                )

        return True

    @api.model
    def cron_convert_all_consumables_and_rebuild_stock(self, limit=100):
        Product = self.env["product.template"].sudo()
        while True:
            products = Product.search([("type", "=", "consu")], limit=limit)
            if not products:
                break
            for record in products:
                self.env.cr.execute(
                    """
                    UPDATE product_template
                    SET type = 'product'
                    WHERE id = %s
                """,
                    (record.id,),
                )
                record.invalidate_cache(["type"])
                record.sudo().action_rebuild_stock()
            self.env.cr.commit()
