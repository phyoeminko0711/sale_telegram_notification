from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    telegram_chat_id = fields.Char(string="Telegram Chat ID")
