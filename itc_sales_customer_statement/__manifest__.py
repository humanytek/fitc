{
    "name": "ITC - Estado de cuenta para vendedores",
    "summary": "Consulta automática de clientes asignados al vendedor del contacto",
    "version": "17.0.1.1.1",
    "category": "Sales",
    "license": "LGPL-3",
    "depends": ["account", "web"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/rules.xml",
        "views/assignment_views.xml",
        "views/partner_views.xml",
        "views/statement_templates.xml",
    ],
    "installable": True,
    "application": False,
}
