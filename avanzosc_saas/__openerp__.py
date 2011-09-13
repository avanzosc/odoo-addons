{
    "name": "Avanzosc_SAAS",
    "version": "1.0",
    "depends": ["base"],
    "author": "Avanzosc (Aitor Juaristi)",
    "category": "Custom Module",
    "description": """
    This module provide :
    * Client extra information for SAAS
    """,
    "init_xml": [],
    'update_xml': [
                   "res_partner_view.xml",
                   "saas_db_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}