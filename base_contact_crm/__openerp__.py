{
    'name' : 'Base Contact CRM',
    'author' : 'Tiny SPRL & Avanzosc',
    'version' : '0.1',
    'website' : 'http://www.openerp.com',
    "category" : "Generic Modules/Base",
    'description' : 'This module extends the CRM with the base_contact addon', 
    'depends' : ['base_contact','crm_claim','crm'],
    'init_xml' : [],
    'update_xml' : [
        'base_contact_crm_view.xml',
    ],
    'demo_xml' : [],
    'installable' : True,
    'active' : False,
}
