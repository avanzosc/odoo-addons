# Sale Product By Location

Allows to define a specific source location on each Sale Order line and sell the
products from the different locations, that may not be children of the default
location of the same SO picking type.

It will raise a warning when the same product with the same location already
exists in the sales order line.

When the SO is confirmed, it will generate one Outgoing Shipment per combination
of source location.

---