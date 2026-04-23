# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import unicodedata

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.models import expression


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    salesorder_external_id = fields.Char(
        string="SalesOrder ID",
        copy=False,
    )
    origin_import = fields.Char(
        string="Origin",
        copy=False,
    )
    sales_team_import = fields.Char(
        string="Sales Team",
        copy=False,
    )
    currency_code_import = fields.Char(
        string="Currency Code",
        copy=False,
    )
    entity_discount_percent = fields.Float(
        copy=False,
    )
    quantity_invoiced = fields.Float(
        copy=False,
    )
    quantity_packed = fields.Float(
        copy=False,
    )
    order_name = fields.Char(
        copy=False,
    )
    confirmation_date = fields.Date(
        copy=False,
    )
    discount = fields.Float(
        copy=False,
    )
    product_uos_qty = fields.Float(
        string="Ordered Quantity (UoS)",
        copy=False,
    )
    product_uom_name = fields.Char(
        string="Unit of Measure",
        copy=False,
    )
    line_type = fields.Char(
        copy=False,
    )
    salesman_name = fields.Char(
        string="Salesperson",
        copy=False,
    )
    invoiced = fields.Boolean(
        copy=False,
    )
    line_subtotal_amount = fields.Float(
        string="Line Subtotal",
        copy=False,
    )
    line_total_amount = fields.Float(
        string="Line Total",
        copy=False,
    )
    item_total_amount = fields.Float(
        string="Item Total",
        copy=False,
    )
    usage_unit = fields.Char(
        copy=False,
    )
    warehouse_name_import = fields.Char(
        string="Warehouse Name",
        copy=False,
    )
    payment_terms_import = fields.Char(
        string="Payment Terms",
        copy=False,
    )
    payment_terms_label_import = fields.Char(
        string="Payment Terms Label",
        copy=False,
    )
    purchase_order_import = fields.Char(
        string="Purchase Order",
        copy=False,
    )
    exchange_rate_import = fields.Float(
        string="Exchange Rate",
        copy=False,
    )
    is_inclusive_tax_import = fields.Boolean(
        string="Is Inclusive Tax",
        copy=False,
    )
    historical = fields.Boolean(
        related="import_id.historical",
        store=True,
        index=True,
        readonly=True,
    )

    def action_process(self):
        if self.filtered("historical"):
            raise UserError(_("Historical import lines cannot be processed."))
        return super().action_process()

    @staticmethod
    def _record_id_or_false(record):
        return record.id if record and len(record) == 1 else False

    @staticmethod
    def _collapse_to_single_commercial_partner(partners):
        if len(partners) <= 1:
            return partners
        commercial_partners = partners.mapped("commercial_partner_id")
        if len(commercial_partners) == 1:
            return commercial_partners
        return partners

    @staticmethod
    def _normalize_partner_name(value):
        value = "".join(
            char
            for char in unicodedata.normalize("NFD", (value or "").lower())
            if unicodedata.category(char) != "Mn"
        )
        value = "".join(char if char.isalnum() else " " for char in value)
        return " ".join(value.split())

    @classmethod
    def _normalize_partner_name_compact(cls, value):
        return "".join(
            char for char in cls._normalize_partner_name(value) if char.isalnum()
        )

    @staticmethod
    def _normalize_reference(value):
        return "".join(char for char in (value or "").lower() if char.isalnum())

    @staticmethod
    def _singularize_token(token):
        if token.endswith("ies") and len(token) > 4:
            return token[:-3] + "y"
        if token.endswith("es") and len(token) > 4:
            return token[:-2]
        if token.endswith("s") and len(token) > 3:
            return token[:-1]
        return token

    @classmethod
    def _normalized_partner_tokens(cls, value):
        stopwords = {
            "llc",
            "sl",
            "sa",
            "srl",
            "ltd",
            "inc",
            "corp",
            "co",
            "company",
            "corporation",
            "group",
        }
        tokens = set()
        for token in cls._normalize_partner_name(value).split():
            token = token.strip()
            if len(token) <= 1 or token in stopwords:
                continue
            tokens.add(token)
            tokens.add(cls._singularize_token(token))
        return tokens

    @classmethod
    def _is_similar_partner_name(cls, left, right):
        left_tokens = cls._normalized_partner_tokens(left)
        right_tokens = cls._normalized_partner_tokens(right)
        if not left_tokens or not right_tokens:
            return False
        common = len(left_tokens & right_tokens)
        if common < 2:
            return False
        if common == min(len(left_tokens), len(right_tokens)):
            return True
        return (common / max(len(left_tokens), len(right_tokens))) >= 0.6

    def _resolve_partner(
        self,
        current_partner,
        name,
        reference,
        vat,
        not_found_msg,
        multiple_found_msg,
        only_if_data=False,
        collapse_to_commercial=False,
    ):
        if current_partner:
            return current_partner, []
        if only_if_data and not (name or reference or vat):
            return current_partner, []
        partner = self._check_partner(name, reference, vat)
        if collapse_to_commercial:
            partner = self._collapse_to_single_commercial_partner(partner)
        return partner, [
            msg
            for condition, msg in (
                (not partner, not_found_msg),
                (len(partner) > 1, multiple_found_msg),
            )
            if condition and msg
        ]

    def _action_validate(self):
        update_values = {}
        log_infos = []
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        customer, customer_logs = self._resolve_partner(
            self.customer_id,
            self.customer_name,
            self.customer_reference,
            False,
            _("Customer not found."),
            _("More than one customer already exist."),
            collapse_to_commercial=True,
        )
        log_infos.extend(customer_logs)

        invoice_address = delivery_address = False
        if not self.historical:
            _sale, log_info_origin = self._check_origin()
            if log_info_origin:
                log_infos.append(log_info_origin)
            for prefix, not_found_msg, multiple_found_msg in (
                (
                    "invoice_address",
                    False,
                    _("More than one Invoice Address already exist."),
                ),
                (
                    "delivery_address",
                    False,
                    _("More than one Delivery Address already exist."),
                ),
            ):
                partner, partner_logs = self._resolve_partner(
                    getattr(self, f"{prefix}_id"),
                    getattr(self, f"{prefix}_name"),
                    getattr(self, f"{prefix}_reference"),
                    getattr(self, f"{prefix}_vat"),
                    not_found_msg,
                    multiple_found_msg,
                    only_if_data=True,
                )
                log_infos.extend(partner_logs)
                if prefix == "invoice_address":
                    invoice_address = partner
                else:
                    delivery_address = partner

        update_values.update(
            {
                "product_id": self._record_id_or_false(product),
                "customer_id": self._record_id_or_false(customer),
                "invoice_address_id": self._record_id_or_false(invoice_address),
                "delivery_address_id": self._record_id_or_false(delivery_address),
                "log_info": "\n".join(log_infos),
                "state": "error" if log_infos else "pass",
                "action": "create",
            }
        )
        return update_values

    def _check_origin(self):
        """Keep header consistency check but ignore total amount differences.

        In DRC files, the imported total can vary per line even for the same
        customer order reference, so it cannot be treated as a strict header field.
        """
        log_info = ""
        error = _(
            "Error: Rows with the same Customer Order Reference have "
            "different information for importing sales order header "
            "data."
        )
        search_domain = [("client_order_ref", "=", self.client_order_ref)]
        sale = self.env["sale.order"].search(search_domain, limit=1)
        if sale and (not sale.sale_import_id or sale.sale_import_id != self.import_id):
            log_info = _(
                "Error: Sale Order already exist with this Client Order "
                "Ref.: %(client_order_ref)s."
            ) % {
                "client_order_ref": self.client_order_ref,
            }
        if not log_info:
            lines = self.import_id.import_line_ids.filtered(
                lambda x: x.client_order_ref == self.client_order_ref
            )
            if lines:
                found = lines.filtered(
                    lambda x: x.customer_name != self.customer_name
                    or x.customer_vat != self.customer_vat
                    or x.customer_reference != self.customer_reference
                    or x.invoice_address_name != self.invoice_address_name
                    or x.invoice_address_vat != self.invoice_address_vat
                    or x.invoice_address_reference != self.invoice_address_reference
                    or x.delivery_address_name != self.delivery_address_name
                    or x.delivery_address_vat != self.delivery_address_vat
                    or x.delivery_address_reference != self.delivery_address_reference
                    or x.date_order != self.date_order
                    or x.delivery_date != self.delivery_date
                )
                if found:
                    log_info = error
        return sale, log_info

    def _check_product(self):
        """Validate product prioritizing SKU + name, with graceful fallbacks."""
        self.ensure_one()
        product_obj = self.env["product.product"]
        log_info = ""
        if self.product_id:
            return self.product_id, log_info

        search_domains = []
        name_domain = False
        product_name = (self.product_name or "").strip()
        product_code = (self.product_code or "").strip()
        if product_name:
            normalized_name = product_name.replace(" ", "")
            normalized_name = "".join(
                c
                for c in unicodedata.normalize("NFD", normalized_name)
                if unicodedata.category(c) != "Mn"
            )
            name_domain = expression.OR(
                [
                    [("trim_name", "=ilike", normalized_name)],
                    [("name", "=ilike", product_name)],
                ]
            )
        code_domain = [("default_code", "=", product_code)] if product_code else False

        if code_domain and name_domain:
            search_domains.append(expression.AND([code_domain, name_domain]))
        if code_domain:
            search_domains.append(code_domain)
        if name_domain:
            search_domains.append(name_domain)

        for search_domain in search_domains:
            products = product_obj.search(search_domain, limit=2)
            if len(products) == 1:
                return products, log_info
            if len(products) > 1:
                error = _("More than one product already exist.")
                log_info = error if not log_info else f"{log_info} {error}"
                return product_obj.browse(), log_info

        if "from_sale_wizard_laser" not in self.env.context:
            error = _("Product not found.")
            log_info = error if not log_info else f"{log_info} {error}"
        return product_obj.browse(), log_info

    def _partner_with_company_domain(self, domain):
        if self.import_id.company_id:
            return expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    domain,
                ]
            )
        return domain

    @staticmethod
    def _materialize_partner_records(partner_obj, records):
        return partner_obj.browse(records.ids)

    def _filter_partners_by_normalized_ref(
        self, partner_obj, records, normalized_reference
    ):
        if not records or not normalized_reference:
            return partner_obj.browse()
        ids = []
        for values in records.read(["ref"], load=False):
            if self._normalize_reference(values.get("ref")) == normalized_reference:
                ids.append(values["id"])
        return partner_obj.browse(ids)

    def _filter_partners_by_normalized_name(
        self, partner_obj, records, normalized_partner_name
    ):
        if not records or not normalized_partner_name:
            return partner_obj.browse()
        normalized_name_compact = self._normalize_partner_name_compact(
            normalized_partner_name
        )
        ids = []
        for values in records.read(["name"], load=False):
            partner_name = values.get("name")
            partner_name_normalized = self._normalize_partner_name(partner_name)
            partner_name_compact = self._normalize_partner_name_compact(partner_name)
            if (
                partner_name_normalized == normalized_partner_name
                or partner_name_compact == normalized_name_compact
            ):
                ids.append(values["id"])
        return partner_obj.browse(ids)

    def _filter_partners_by_similar_name(self, partner_obj, records, compared_name):
        if not records or not compared_name:
            return partner_obj.browse()
        ids = []
        for values in records.read(["name"], load=False):
            if self._is_similar_partner_name(values.get("name"), compared_name):
                ids.append(values["id"])
        return partner_obj.browse(ids)

    def _filter_partners_by_exact_ref(self, partner_obj, records, exact_reference):
        if not records or not exact_reference:
            return partner_obj.browse()
        normalized_exact_reference = exact_reference.strip().lower()
        ids = []
        for values in records.read(["ref"], load=False):
            if (values.get("ref") or "").strip().lower() == normalized_exact_reference:
                ids.append(values["id"])
        return partner_obj.browse(ids)

    def _partner_token_domain(self, name):
        normalized_tokens = sorted(self._normalized_partner_tokens(name))
        if not normalized_tokens:
            return []
        token_domain = [
            ("name", "ilike", token) for token in normalized_tokens if len(token) > 1
        ]
        return token_domain[:6]

    def _search_partners(self, partner_obj, domain, limit):
        records = partner_obj.search(
            self._partner_with_company_domain(domain), limit=limit
        )
        return self._materialize_partner_records(partner_obj, records)

    def _partner_candidates_by_reference(
        self, partner_obj, reference, normalized_reference
    ):
        if not reference:
            return partner_obj.browse()
        ref_candidates = self._search_partners(
            partner_obj, [("ref", "=", reference)], limit=80
        )
        if ref_candidates or not normalized_reference:
            return ref_candidates

        initial_chunk = normalized_reference[:8]
        if not initial_chunk:
            return ref_candidates
        candidate_pool = self._search_partners(
            partner_obj, [("ref", "ilike", initial_chunk)], limit=200
        )
        normalized_ref_matches = self._filter_partners_by_normalized_ref(
            partner_obj, candidate_pool, normalized_reference
        )
        return normalized_ref_matches or ref_candidates

    def _partner_candidates_by_name(
        self, partner_obj, name, normalized_name, token_domain
    ):
        if not name:
            return partner_obj.browse()

        name_domain = expression.OR([[("name", "=", name)], [("name", "=ilike", name)]])
        name_candidates = self._search_partners(partner_obj, name_domain, limit=80)
        if not name_candidates and token_domain:
            name_candidates = self._search_partners(partner_obj, token_domain, limit=80)

        if not name_candidates and normalized_name:
            normalized_name_parts = normalized_name.split()
            seed_token = normalized_name_parts[0] if normalized_name_parts else False
            if seed_token:
                candidate_pool = self._search_partners(
                    partner_obj, [("name", "ilike", seed_token)], limit=200
                )
                normalized_name_matches = self._filter_partners_by_normalized_name(
                    partner_obj, candidate_pool, normalized_name
                )
                if normalized_name_matches:
                    return normalized_name_matches
                fuzzy_name_matches = self._filter_partners_by_similar_name(
                    partner_obj, candidate_pool, name
                )
                if fuzzy_name_matches:
                    return fuzzy_name_matches

        if name_candidates and normalized_name:
            normalized_matches = self._filter_partners_by_normalized_name(
                partner_obj, name_candidates, normalized_name
            )
            if normalized_matches:
                return normalized_matches
        return name_candidates

    @staticmethod
    def _combine_partner_candidates(partner_obj, ref_candidates, name_candidates):
        if ref_candidates and name_candidates:
            ref_name_candidates = ref_candidates & name_candidates
            return ref_name_candidates or ref_candidates
        return ref_candidates or name_candidates or partner_obj.browse()

    def _refine_partner_candidates(
        self, partner_obj, candidates, normalized_name, reference
    ):
        if len(candidates) > 1 and normalized_name and not reference:
            normalized_matches = self._filter_partners_by_normalized_name(
                partner_obj, candidates, normalized_name
            )
            if normalized_matches:
                candidates = normalized_matches
        if len(candidates) > 1 and reference:
            exact_ref = self._filter_partners_by_exact_ref(
                partner_obj, candidates, reference
            )
            if exact_ref:
                candidates = exact_ref
        return candidates

    def _check_partner(self, name, reference, vat):
        """Validate customer by reference and normalized name."""
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        if self.import_id.company_id:
            partner_obj = partner_obj.with_company(self.import_id.company_id)

        name = (name or "").strip()
        reference = (reference or "").strip()
        normalized_name = self._normalize_partner_name(name)
        normalized_reference = self._normalize_reference(reference)
        token_domain = self._partner_token_domain(name)
        ref_candidates = self._partner_candidates_by_reference(
            partner_obj, reference, normalized_reference
        )
        name_candidates = self._partner_candidates_by_name(
            partner_obj, name, normalized_name, token_domain
        )
        candidates = self._combine_partner_candidates(
            partner_obj, ref_candidates, name_candidates
        )
        candidates = self._refine_partner_candidates(
            partner_obj, candidates, normalized_name, reference
        )
        # We only need to know 0/1/many; cap to 2 for faster validation on big imports.
        return candidates[:2]
