{
    'name': "Product Final Position",

    'summary': """
       Some new fields added for Final Product variants""",

    'description': """
       Some menus in sale and stock have been added, so both customized final product codes and quartering locations could be added. 
    """,

    'author': "Gonzalo Nuin",
    'website': "https://avanzosc.es/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '14.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','stock',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_final_view.xml',       
    ],
    
    # only loaded in demonstration mode
    'demo': [
      
    ],
}
