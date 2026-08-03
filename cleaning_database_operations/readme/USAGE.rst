1. Go to **Cleaning Database > Cleaning Database** and create a new record.
2. Set the **Date Limit**: records created on or before this date will be deleted.
3. Select the **Companies** whose data you want to clean.
4. Enable or disable each cleaning step as needed:

   - **Step 1: Accounting** (analytic lines, assets, bank statements, journal
     entries, payment orders, partial reconciles, check deposits).
   - **Step 2: Manufacturing** (MRP workorders and productions).
   - **Step 3: Stock** (valuation layers, pickings/moves/move lines, inventories,
     lots, quants).
   - **Step 4: Sales** (sale orders and lines).
   - **Step 5: Purchases** (purchase orders and lines).
   - **Step 6: Point of Sale** (quotations, orders, payments and lines).

   Sub-steps within each step can be independently toggled on or off.

5. Optionally click **Restart Sequences** to reset all ``ir.sequence`` records for
   the selected companies back to 1.
6. Click **Schedule** to queue the cleaning job. The status changes to
   *Scheduled*.
7. The cron job will automatically pick up all *Scheduled* records and execute the
   full cleaning process. Each step is processed sequentially and its toggle is
   disabled once all data in that area has been removed.
8. When all data is clean, the record transitions to *Done* and a chatter message
   confirms completion.

Individual cleaning actions can also be triggered manually from each tab while
the record is in *Draft* state.
