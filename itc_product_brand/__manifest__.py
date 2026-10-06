{
    "name": "ITC - Marcas de Producto",
    "version": "17.0.1.0.2",
    "summary": "Dato maestro de Marca para productos y análisis de facturación",
    "description": "Catálogo formal de marcas, campo Marca en productos y dimensión Marca en account.invoice.report para pivotes, Spreadsheet y Dashboards.",
    "author": "ITC",
    "license": "LGPL-3",
    "category": "Sales",
    "depends": ["product", "account"],
    "data": [
        "security/product_brand_security.xml",
        "security/ir.model.access.csv",
        "views/product_brand_views.xml",
        "views/product_template_views.xml",
        "views/account_invoice_report_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}
