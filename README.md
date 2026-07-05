# Sale Telegram Notification

Automatically send Telegram notifications when a Sales Order is confirmed in Odoo.

## Features

* Send Telegram notifications automatically after Sales Order confirmation.
* Supports Telegram Bot API integration.
* Configurable Bot Token using Odoo System Parameters.
* Store Telegram Chat ID on each Contact (Partner).
* Reusable notification method for future module extensions.
* Safe error handling that never blocks the Sales Order confirmation process.
* Logs notification status in the Sales Order chatter.
* Clean, modular, and production-ready code.

---

## Supported Version

* Odoo 18 Community
* Odoo 18 Enterprise

---

## Module Information

| Item        | Value                      |
| ----------- | -------------------------- |
| Module Name | sale_telegram_notification |
| License     | LGPL-3                     |
| Category    | Sales                      |
| Author      | Phyoe Min Ko               |
| Dependency  | sale                       |

---

## Installation

1. Copy the module into your custom addons directory.
2. Update the Apps List.
3. Install **Sale Telegram Notification**.
4. Configure your Telegram Bot Token.
5. Enter the Telegram Chat ID for each Contact that should receive notifications.

---

## Configuration

### Step 1

Create a Telegram Bot using **@BotFather**.

You will receive a Bot Token.

Example:

```text
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Step 2

Open:

**Settings → Technical → System Parameters**

Create a new parameter.

| Key                | Value                   |
| ------------------ | ----------------------- |
| telegram_bot.token | Your Telegram Bot Token |

---

### Step 3

Open the Contact.

A new field is available:

* Telegram Chat ID

Example:

```text
123456789
```

or for a Telegram Group

```text
-1001234567890
```

---

## Workflow

```text
Sales Order
      │
Confirm
      │
action_confirm()
      │
Generate Notification
      │
Telegram Bot API
      │
Telegram User / Group
```

---

## Example Notification

```text
✅ Sale Order Confirmed

SO Number: S00025

Customer: ABC Company

Salesperson: John Smith

Total Amount: 12,500.00 USD

Confirmation Date:
2026-07-05
```

---

## Technical Details

The module extends:

* res.partner
* sale.order

Uses:

* Telegram Bot API
* Python requests library
* ir.config_parameter

No Bot Token is hard-coded.

---

## Error Handling

The module is designed for production use.

If:

* Telegram API is unavailable
* Invalid Chat ID
* Missing Bot Token
* Network timeout

the Sales Order confirmation continues normally.

Errors are logged in the Sales Order chatter.

---

## Roadmap

Future enhancements:

* Purchase Order Notifications
* Invoice Notifications
* Delivery Order Notifications
* Manufacturing Notifications
* Approval Notifications
* Telegram Group Support
* HTML Message Formatting
* Inline Buttons
* Send PDF Quotation
* Send PDF Invoice
* Multiple Telegram Recipients
* Notification Templates
* Notification History
* Scheduled Notifications

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

Please create an Issue or submit a Pull Request.

---

## Support

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.

---

## License

This module is released under the **LGPL-3** License.
