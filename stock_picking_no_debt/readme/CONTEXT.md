**Business need**

In standard Odoo, a delivery picking can be validated even if the associated sale order has pending unpaid invoices. This can lead to financial and operational issues, as goods are delivered to customers who have not yet paid previous invoices.

**Use cases**

- A company that wants to avoid delivering goods to customers with unpaid invoices.
- A warehouse that needs a visual warning (*Pending Sale Invoices* field) to identify which pickings correspond to customers with debt.
- Financial control over stock outflows without forcibly blocking the operation, leaving the final decision to the user.

**Approach**

The module adds a computed boolean field *Pending Sale Invoices* to pickings, which indicates whether the associated sale order has posted and unpaid invoices. Additionally, it intercepts the picking validation flow to display a wizard that lets the user decide how to proceed.

**Related modules**

- Depends on *sale_stock*, which provides the integration between sale orders and pickings.
- No additional configuration required; works out of the box without developer mode.
