---
id: '4ee67d38e3bae20185e8bfd3f6bf4baf'
title: 'Public Release Note'
url: 'https://knowledge.intershop.com/kb/index.php/Display/31125F'
scraped_at: '2026-04-21T05:34:20.564734+00:00'
---
#### Credit Card iFrame Styles

For the configuration of the styles, the credit card payment method can be adjusted with the following properties:

| Property | Values | Description |
|---|
| payment.payone.creditcard.<field>.size | Positive number | Determines the size of the input field. Default = 4 |
| payment.payone.creditcard.<field>.maxlength | Positive number | Determines the length of the input field. Default = 4 |
| payment.payone.creditcard.<field>.width | String | Determines the width of the iframe that holds the field. The unit of the width has to be specified the same way as it would be specified in a CSS style (e.g., 60px). |
| payment.payone.creditcard.defaultStyle.height | String | Determines the height of the iframe that holds the field. The unit of the height has to be specified the same way as it would be specified in a CSS style, Default = 34px |
| payment.payone.creditcard.defaultStyle.width | String | Determines the width of the iframe that holds the field. The unit of the width has to be specified the same way as it would be specified in a CSS style. Default = 250px |
| payment.payone.creditcard.defaultStyle.input | String | Default CSS style to be used with text fields. |
| payment.payone.creditcard.defaultStyle.select | String | Default CSS style to be used with select fields. |

<field> identifies which PAYONE credit card field is affected by the property. Supported values are cardtypes, cardnumber, cardcvc2, cardexpiremonth, cardexpireyear, e.g., payment.payone.creditcard.cardcvc2.width.

#### Supported Countries

For each payment method a list of supported countries can be defined. A comma-separated list of ISO 3166 ALPHA 2 country codes (also see PAYONE API documentation) is valid. The value '*' can be used if there is no restriction.

| Property | Default |
|---|
intershop.payment.Payone_Sofort.countries | AT,DE,CH,NL |
intershop.payment.Payone_IDeal.countries | NL |
intershop.payment.Payone_PostFinance_Card.countries | CH |
intershop.payment.Payone_PayPal.countries | * |
intershop.payment.Payone_Invoice.countries | * |
| intershop.payment.Payone_CreditCard.countries | * |

See [Supported Countries and Currencies](#PublicReleaseNote-PAYONEServiceConnector7-SupportedCurrencies) for further information about payment method specifics.

The PAYONE Service Connector provides English and German localization for payment-specific input field labels, error messages, etc.

You can overwrite the existing localizations in the back office within your custom cartridge*.*

The following table describes transmitted data by the PAYONE Service Connector from ICM to PAYONE during the payment process:

The PAYONE payment service requires a gross-based price and tax calculation. That is, the price type and the price display must be set to *gross*, and a gross-based taxation service must be enabled.

Most of the payment methods included in this package are specific for certain countries or currencies.

The length of e-mail addresses is limited to 50 characters on PAYONE side. Only 48 of these characters are usable, because the at sign (@) is being replaced by escape characters.