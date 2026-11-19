/** @odoo-module **/

import {
  ProductLabelSectionAndNoteField,
  productLabelSectionAndNoteField,
} from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";
import {ProductConfiguratorDialog} from "@sale/js/product_configurator_dialog/product_configurator_dialog";
import {serializeDateTime} from "@web/core/l10n/dates";
import {x2ManyCommands} from "@web/core/orm_service";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

const {DateTime} = luxon;

/**
 * We inherit the standard Sale dialog only to make exclusion data defensive.
 * No template, components, layout or display options are changed, therefore
 * the rendered interface is exactly sale.ProductConfiguratorDialog.
 */
class PurchaseProductConfiguratorDialog extends ProductConfiguratorDialog {
  _checkExclusions(product) {
    if (product.exclusions) {
      for (const ptavId of this._getCombination(product)) {
        product.exclusions[ptavId] ||= [];
      }
    }
    return super._checkExclusions(product);
  }
}

export class PurchaseProductField extends ProductLabelSectionAndNoteField {
  static template = "purchase_product_configurator.PurchaseProductField";

  setup() {
    super.setup();
    this.dialog = useService("dialog");
  }

  get hasConfigurationButton() {
    const line = this.props.record.data;
    return Boolean(
      line.product_id &&
        line.is_configurable_product &&
        !line.display_type &&
        !line.is_downpayment
    );
  }

  async onEditConfiguration() {
    const record = this.props.record;
    const line = record.data;
    const order = record.model.root.data;

    const variantPtavIds = line.product_template_attribute_value_ids.records.map(
      (record) => record.resId
    );
    const noVariantPtavIds = line.product_no_variant_attribute_value_ids.records.map(
      (record) => record.resId
    );

    this.dialog.add(PurchaseProductConfiguratorDialog, {
      productTemplateId: line.configurator_product_tmpl_id[0],
      ptavIds: [...variantPtavIds, ...noVariantPtavIds],
      customPtavs: [],
      quantity: line.product_qty,
      productUOMId: line.product_uom?.[0],
      companyId: line.company_id?.[0],
      pricelistId: line.configurator_pricelist_id?.[0],
      currencyId: line.configurator_currency_id?.[0],
      soDate: serializeDateTime(order.date_order || DateTime.now()),
      edit: true,

      // IMPORTANT: do not pass `options` here.
      // ProductConfiguratorDialog defaults to showQuantity=true and
      // showPrice=true, exactly as the standard Sale configurator.

      save: async (mainProduct) => {
        const selectedNoVariantPtavIds = mainProduct.attribute_lines
          .filter((ptal) => ptal.create_variant === "no_variant")
          .flatMap((ptal) => ptal.selected_attribute_value_ids);

        // Let Purchase execute its normal product onchange first.
        await record.update({
          product_id: [mainProduct.id, mainProduct.display_name],
          product_no_variant_attribute_value_ids: [
            x2ManyCommands.set(selectedNoVariantPtavIds),
          ],
        });

        // Then apply the quantity chosen in the same standard dialog.
        // Purchase will recompute vendor price/date using the final qty.
        if (record.data.product_qty !== mainProduct.quantity) {
          await record.update({
            product_qty: mainProduct.quantity,
          });
        }
      },
      discard: () => null,
    });
  }
}

export const purchaseProductField = {
  ...productLabelSectionAndNoteField,
  component: PurchaseProductField,
};

registry
  .category("fields")
  .add("purchase_product_configurator_many2one", purchaseProductField);
