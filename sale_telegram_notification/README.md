# Sale Telegram Notification

`sale_telegram_notification` is a custom Odoo 18 addon that sends a Telegram message when a Sales Order is confirmed.

The module is designed to be lightweight and operationally safe:

- it does not hard-code credentials
- it reads the bot token from `ir.config_parameter`
- it does not block Sales Order confirmation if Telegram is unavailable
- it logs notification status in the Sales Order chatter

## Features

- Adds `Telegram Chat ID` to partner records
- Extends `sale.order` confirmation workflow
- Sends a Telegram notification after successful confirmation
- Uses Python `requests` with timeout protection
- Handles Telegram API errors without interrupting business flow
- Posts success or failure information to the chatter

## Supported Version

- Odoo 18

## Dependencies

### Odoo modules

- `sale`

### Python packages

- `requests`

## Module Structure

```text
sale_telegram_notification/
|-- __init__.py
|-- __manifest__.py
|-- README.md
|-- models/
|   |-- __init__.py
|   |-- res_partner.py
|   `-- sale_order.py
`-- views/
    `-- res_partner_views.xml
```

## Functional Overview

When a Sales Order is confirmed, the module:

1. calls the standard Odoo confirmation flow
2. retrieves the Telegram bot token from system parameters
3. retrieves the target chat ID from the salesperson's related partner
4. builds a formatted Telegram message
5. sends the message using the Telegram Bot API
6. logs the result in the Sales Order chatter

If Telegram configuration is missing or the API request fails, the order is still confirmed successfully.

## Configuration

### 1. Configure the Bot Token

Go to:

`Settings -> Technical -> Parameters -> System Parameters`

Create or update this parameter:

- `Key`: `telegram_bot.token`
- `Value`: `<your_telegram_bot_token>`

Example:

```text
telegram_bot.token = 123456789:AAExampleBotToken
```

### 2. Configure the Salesperson Chat ID

Open the partner record related to the salesperson and fill:

- `Telegram Chat ID`

The module uses:

```python
self.user_id.partner_id.telegram_chat_id
```

So the chat ID must be stored on the salesperson's partner record, not necessarily the customer.

### 3. Optional Fallback Chat ID

The current implementation also supports an optional fallback parameter:

- `telegram_bot.default_chat_id`

If the salesperson does not have a `Telegram Chat ID`, the module will use this fallback chat ID when configured. This can be used for a team group or central notification channel.

## Message Format

The Telegram message is sent in the following format:

```text
✅ Sale Order Confirmed

SO Number: [SO Number]
Customer: [Customer Name]
Salesperson: [Salesperson Name]
Total Amount: [Amount] [Currency]
Confirmation Date: [Date]
```

## Installation

1. Place the addon in your custom addons path.
2. Ensure the addons path is included in `odoo.conf`.
3. Restart the Odoo service.
4. Update the apps list.
5. Install the `Sale Telegram Notification` module.

For existing installations after code changes:

1. restart Odoo
2. upgrade the module

## Behavior Notes

- Sale confirmation is never blocked by Telegram failures
- Missing token or missing chat ID causes the notification to be skipped
- Telegram request failures are caught and logged
- Status is posted to chatter as an internal note

## Technical Notes

Core implementation points:

- `res.partner.telegram_chat_id`
- `sale.order.action_confirm()`
- `sale.order._notify_telegram_sale_confirmed()`
- `sale.order._build_telegram_confirmation_message()`
- `sale.order._send_telegram_message(chat_id, message)`

## Security and Operations

- Do not hard-code the Telegram bot token in source code
- Store the bot token only in `ir.config_parameter`
- Rotate the bot token immediately if it is exposed in screenshots, logs, or shared documents
- Restrict access to Technical Settings in production environments

## Troubleshooting

### No message is sent

Check all of the following:

- `telegram_bot.token` exists in System Parameters
- the salesperson is set on the Sales Order
- the salesperson's related partner has `Telegram Chat ID`
- the bot is allowed to message the target chat

### Field not visible on partner form

Check:

- the module is installed
- the module was upgraded after code changes
- the view inheritance loaded successfully

### Telegram API error

Review:

- Sales Order chatter note
- Odoo server log output

## Future Enhancements

- settings UI using `res.config.settings`
- configurable message templates
- per-company configuration
- notification enable/disable switch
- support for different Telegram message targets by sales team

## License

LGPL-3
