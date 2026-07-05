{
    "name": "Sale Telegram Notification",
    "version": "18.0.1.0.0",
    "summary": "Send Telegram notifications when sale orders are confirmed",
    "category": "Sales/Sales",
    "author": "dev_pmk",
    "license": "LGPL-3",
    "depends": ["sale"],
    "external_dependencies": {
        "python": ["requests"],
    },
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": False,
}
