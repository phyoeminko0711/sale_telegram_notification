import logging

import requests

from odoo import _, fields, models
from odoo.tools import format_amount

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            order._notify_telegram_sale_confirmed()
        return result

    def _notify_telegram_sale_confirmed(self):
        self.ensure_one()

        config = self.env["ir.config_parameter"].sudo()
        token = (config.get_param("telegram_bot.token") or "").strip()
        partner = self.user_id.partner_id
        chat_id = (partner.telegram_chat_id or "").strip()
        fallback_chat_id = (config.get_param("telegram_bot.default_chat_id") or "").strip()
        target_chat_id = chat_id or fallback_chat_id

        if not token:
            self._post_telegram_message_to_chatter(
                _("Telegram notification skipped: missing system parameter 'telegram_bot.token'.")
            )
            return

        if not target_chat_id:
            self._post_telegram_message_to_chatter(
                _(
                    "Telegram notification skipped: no Telegram Chat ID found on the salesperson "
                    "partner and no fallback 'telegram_bot.default_chat_id' is configured."
                )
            )
            return

        message = self._build_telegram_confirmation_message()
        success, detail = self._send_telegram_message(target_chat_id, message)

        if success:
            self._post_telegram_message_to_chatter(
                _("Telegram notification sent successfully to chat ID %s.") % target_chat_id
            )
        else:
            self._post_telegram_message_to_chatter(
                _("Telegram notification failed for chat ID %s: %s")
                % (target_chat_id, detail)
            )

    def _build_telegram_confirmation_message(self):
        self.ensure_one()

        confirmation_date = self.date_order or fields.Datetime.now()
        amount = format_amount(self.env, self.amount_total, self.currency_id)
        confirmation_date_text = fields.Date.to_string(fields.Datetime.to_datetime(confirmation_date).date())

        return "\n".join(
            [
                "✅ Sale Order Confirmed",
                "",
                "SO Number: %s" % (self.name or ""),
                "Customer: %s" % (self.partner_id.display_name or ""),
                "Salesperson: %s" % (self.user_id.name or ""),
                "Total Amount: %s" % amount,
                "Confirmation Date: %s" % confirmation_date_text,
            ]
        )

    def _send_telegram_message(self, chat_id, message):
        self.ensure_one()

        token = (self.env["ir.config_parameter"].sudo().get_param("telegram_bot.token") or "").strip()
        if not token:
            return False, _("Missing Telegram bot token.")

        url = "https://api.telegram.org/bot%s/sendMessage" % token
        payload = {
            "chat_id": chat_id,
            "text": message,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as err:
            _logger.exception("Telegram notification request failed for sale order %s", self.name)
            return False, str(err)
        except ValueError as err:
            _logger.exception("Invalid Telegram API response for sale order %s", self.name)
            return False, _("Invalid Telegram API response: %s") % err

        if not response_data.get("ok"):
            error_description = response_data.get("description") or _("Unknown Telegram API error.")
            _logger.warning(
                "Telegram API returned an error for sale order %s: %s",
                self.name,
                error_description,
            )
            return False, error_description

        _logger.info("Telegram notification sent successfully for sale order %s", self.name)
        return True, _("Message sent.")

    def _post_telegram_message_to_chatter(self, body):
        self.ensure_one()
        try:
            self.message_post(body=body, subtype_xmlid="mail.mt_note")
        except Exception:
            _logger.exception(
                "Unable to post Telegram notification status in chatter for %s",
                self.name,
            )
