# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    cr.execute(
        """
        UPDATE product_mould AS mould
           SET concave_id = data.res_id
          FROM ir_model_data AS data
         WHERE data.module = 'product_shape_mould'
           AND data.name = CASE mould.name
               WHEN 'M01' THEN 'product_shape_concave_low'
               WHEN 'M02' THEN 'product_shape_concave_high'
               WHEN 'M03' THEN 'product_shape_concave_low'
               WHEN 'M04' THEN 'product_shape_concave_medium'
           END
           AND mould.type = 'mould'
           AND mould.concave_id IS NULL
        """
    )
    cr.execute(
        """
        UPDATE product_shape AS shape
           SET concave_id = mould.concave_id
          FROM product_mould AS mould
         WHERE shape.mould_id = mould.id
           AND mould.concave_id IS NOT NULL
           AND shape.concave_id IS DISTINCT FROM mould.concave_id
        """
    )
