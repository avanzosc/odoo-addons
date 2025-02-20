/** @odoo-module **/

import {Component, xml} from "@odoo/owl";
import {useBus, useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {useState, onMounted, onWillDestroy} from "@odoo/owl";

export class WebCustomMessageRibbon extends Component {
  setup() {
    this.state = useState({
      comparisonCount: 0,
      debitCount: 0,
      creditCount: 0,
      amountCurrencyCount: 0,
    });
    this.orm = useService("orm");

    // Buscar todos los registros de "account.move.line.comparison"
    this.orm.search("account.move.line.comparison", [], {}).then((records) => {
      const comparisonCount = records.length;
      console.log("Comparison count:", comparisonCount);
      this.state.comparisonCount = comparisonCount;

      // Buscar registros donde is_debit_different sea true
      this.orm
        .search("account.move.line.comparison", [["is_debit_different", "=", true]], {})
        .then((debitRecords) => {
          const debitCount = debitRecords.length;
          console.log("Debit count:", debitCount);
          this.state.debitCount = debitCount;
        });

      // Buscar registros donde is_credit_different sea true
      this.orm
        .search(
          "account.move.line.comparison",
          [["is_credit_different", "=", true]],
          {}
        )
        .then((creditRecords) => {
          const creditCount = creditRecords.length;
          console.log("Credit count:", creditCount);
          this.state.creditCount = creditCount;
        });

      // Buscar registros donde is_amount_currency_different sea true
      this.orm
        .search(
          "account.move.line.comparison",
          [["is_amount_currency_different", "=", true]],
          {}
        )
        .then((amountCurrencyRecords) => {
          const amountCurrencyCount = amountCurrencyRecords.length;
          console.log("Amount Currency count:", amountCurrencyCount);
          this.state.amountCurrencyCount = amountCurrencyCount;
        });
      this.clearTemplate = window.clearTemplate;
    });

    onMounted(() => {
      window.showTemplate();
    });

    onWillDestroy(() => {
      window.clearTemplate();
    });

    useBus(this.env.bus, "ROUTE_CHANGE", () => {
      if (!window.location.href.includes("account.move.line.comparison")) {
        window.clearTemplate();
      }
    });
  }
}

window.clearTemplate = () => {
  const components = registry.category("main_components").entries;
  const componentExists = components.some(
    (entry) => entry[0] === "WebCustomMessageRibbon"
  );
  if (!components) {
    return;
  }

  if (componentExists) {
    registry.category("main_components").remove("WebCustomMessageRibbon");
  }
};

window.showTemplate = (firstTime = false) => {
  const components = registry.category("main_components").entries;

  if (firstTime && window.location.href.includes("account.move.line.comparison")) {
    registry.category("main_components").add("WebCustomMessageRibbon", {
      Component: WebCustomMessageRibbon,
    });
  }

  if (!components) {
    return;
  }
  const componentExists = components.some(
    (entry) => entry[0] === "WebCustomMessageRibbon"
  );
  if (
    !componentExists &&
    window.location.href.includes("account.move.line.comparison")
  ) {
    registry.category("main_components").add("WebCustomMessageRibbon", {
      Component: WebCustomMessageRibbon,
    });
  }
};

WebCustomMessageRibbon.template = xml`
    <div class="alert alert-primary border border-primary rounded shadow-lg p-4 d-flex flex-column align-items-start" style="margin-bottom: 0;">
        <h4 class="text-primary mb-3">Resumen de Comparación</h4>
        <ul class="list-group w-100">
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Número total de registros:</span>
                <strong><t t-esc="this.state.comparisonCount" /></strong>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Registros con <code>is_debit_different = true</code>:</span>
                <strong class="text-danger"><t t-esc="this.state.debitCount" /></strong>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Registros con <code>is_credit_different = true</code>:</span>
                <strong class="text-warning"><t t-esc="this.state.creditCount" /></strong>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>Registros con <code>is_amount_currency_different = true</code>:</span>
                <strong class="text-success"><t t-esc="this.state.amountCurrencyCount" /></strong>
            </li>
        </ul>
        <button class="btn btn-danger mt-3 align-self-end" t-on-click="clearTemplate">
            <i class="fa fa-trash"></i> Limpiar
        </button>
    </div>
`;

WebCustomMessageRibbon.props = {};
window.showTemplate(true);
if (registry.categories) {
  console.log("Registry categories:", Object.keys(registry.categories));
} else {
  console.log("No categories found in the registry.");
}
