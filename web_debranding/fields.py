# Copyright 2015-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Ilmir Karamov <https://it-projects.info/team/ilmir-k>
# Copyright 2017 Nicolas JEUDY <https://github.com/njeudy>
# License MIT (https://opensource.org/licenses/MIT).

from odoo.fields import _String

from .models.ir_translation import debrand

get_trans_func = _String.get_trans_func


def get_trans_func_debrand(self, records):
    if True:  # keep original indent
        if callable(self.translate):
            rec_src_trans = records.env["ir.translation"]._get_terms_translations(
                self, records
            )

            def translate(record_id, value):
                src_trans = rec_src_trans[record_id]

                def tr(source):
                    trans = src_trans.get(source, source)
                    return debrand(records.env, trans)

                return self.translate(tr, value)

        else:
            rec_trans = records.env["ir.translation"]._get_ids(
                "{},{}".format(self.model_name, self.name),
                "model",
                records.env.lang,
                records.ids,
            )

            def translate(record_id, value):
                return rec_trans.get(record_id) or value

        return translate


_String.get_trans_func = get_trans_func_debrand
