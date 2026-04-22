---
id: '0b8ab76438ecdecf12ac6dcea5f79ed6'
title: 'Public Release Note'
url: 'https://knowledge.intershop.com/kb/index.php/Display/29135S'
scraped_at: '2026-04-21T05:40:10.822200+00:00'
---
Welcome to the Intershop Concardis Service Connector. The service connector adds Concardis payment methods to your Intershop installation.

This document provides important product information, including version information and dependencies. It also outlines the basic setup and configuration steps.

This delivery and the accompanying documentation are valid for the following combinations of software versions:

| Intershop | Supported Application Types | PWA* | Concardis Service Connector |
|---|---|---|---|
| 7.10.15.3 | intershop.SMB, intershop.B2C | 0.17.0+ | 1.1.5 |
| 7.10.16.6 | intershop.SMB, intershop.B2C | 0.17.0+ | 1.3.0+ |
| 7.10.16.6+ | intershop.SMB, intershop.B2C | 0.20.0+ | 1.7.0+ |
| 7.10.16.6+ | intershop.SMB, intershop.B2C | 0.20.0+ | 1.9.0+ |
| 7.10.17.0+ | intershop.SMB, intershop.B2C, | 0.20.0 - 0.23.0 | 1.10.8+ |
7.10.26.2-LTS - 7.10.30.x (Tomcat 7) | intershop.SMB, intershop.B2C, intershop.REST | 0.26.0 - 0.31.0 | 1.11.7+ |

* Please see [PWA releases](https://github.com/intershop/intershop-pwa/releases) documentation for details.

** Feature of ICM 7.10.21.0

Concardis Connector version 2.0.0 (see [Public Release Note - Concardis Service Connector 2](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1943835607/Public+Release+Note+-+Concardis+Service+Connector+2)) features the same functionality as Concardis Connector 1.11.7 to facilitate migration from ICM 7.10.30- to 7.10.31+.

The next table provides information about the cartridges included in the package. Not all of these cartridges are required.

| Cartridge | Description | Required |
|---|---|---|
ac_payment_concardis | Includes all base functionality and business logic which is used. | |
as_responsive_concardis | Enables the Concardis payment connector for the following application types:
The cartridge is optional, can be downloaded separately from Intershop Product Calendar and may be included if the project uses the responsive starter store. Unzip the file to your multi-project folder next to your responsive source files. This step can be skipped if the custom project does not support these application types or Concardis is not required in these application types. | |
app_sf_responsive_concardis | Includes some additional functionality which is relevant for the responsive storefront reference application only, e.g., the integration of the hosted payment pages of the credit card. The cartridge is optional, can be downloaded separately from Intershop Product Calendar and may be included in case the project is based on the responsive storefront reference application. Unzip the file to your multi-project folder next to your responsive source files. The referenced cartridge |

The Concardis Service Connector is based on the new Payment API introduced in IS 7.6.

The Concardis Service Connector can be used for the following application types:

| Application Type | Application Type ID | Description |
|---|---|---|
| B2C WebShop | `intershop.B2CResponsive` | Business to Consumer Channel |
| SMB WebShop | `intershop.SMBResponsive` | Business to Business Channel |
| Progressive Web App | `intershop.REST` | Business to Customer and Business Channel via REST API (only available with ICM 7.10.21 and later) |

Documentation for Concardis error messages and possible sources of the errors is available here:

[https://docs.payengine.de/buildyourown/restdoc/errors](https://docs.payengine.de/buildyourown/restdoc/errors)

Documentation for the REST API can be found here:

[https://docs.payengine.de/buildyourown/restdoc/providercodes](https://docs.payengine.de/buildyourown/restdoc/providercodes)

For information on setup, customization and configuration, please refer to [Guide - Setup Concardis Service Connector](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1925235487/Guide+-+Setup+Concardis+Service+Connector).

The Concardis Service Connector adds the following payment methods to your Intershop 7 system:

| Payment Method Type | Payment Method | Auto Capture | Manual Capture* | Cancel* | Reduce* | Refund |
|---|---|---|---|---|---|---|
| Credit Card | Credit Card Payment supported by Concardis e.g.:
Includes 3DS 2.0 support. | |||||
| Online Payment | Alipay | |||||
| Bancontact | ||||||
| EPS | ||||||
| Giropay | ||||||
| iDEAL | ||||||
| PayPal | ||||||
| SEPA Direct Debit | ||||||
| Sofort | ||||||
| WeChat Pay |

* only available if the corresponding payment method's Capture Mode is set to *manual*. Concardis reserves the authorized amount for a standard duration of 5 days. Afterwards a manual capture fails (error code 21).

The merchant can negotiate a different duration time with Concardis.

The following table lists all options that are available for payment transactions.

| Operation | Description |
|---|---|
| Capture | Request for settling the payment. This action is only available if the corresponding payment method's Capture Mode is set to manual. |
| Cancel | Request for abandoning a payment settlement. This action is only available if the corresponding payment method's Capture Mode is set to manual. |
| Refund | Option to return (parts of) the captured amount. This action is only available if the corresponding payment transaction was captured before. |
| Reduce | Request for reducing the authorized payment amount partially. This action is only available if the corresponding payment method's Capture Mode is set to manual. |

The connector provides two options for manual synchronization of the payment states between Concardis and Intershop Commerce Management:

When a payment status was successfully synchronized with Concardis, the status is updated in ICM. Afterwards the order status is updated. In case the payment on Concardis side was successful, the order creation is continued at the point where it was broken. For failed payments the order is set to "PAYMENT_CANCELLED".

Orders which are pending on both sides (Concardis and ISH) cannot be fixed with that approach. In these cases there are abandoned baskets.

To enable a periodic check if payments need to be synchronized, you have to configure a job in the SMC. Calling the startnode `Start`

of pipeline `SynchronizeConcardisPaymentsJob`

can be started manually or run regularly.

In the *Attributes* tab you can define after which time in the pending state (`PendingSinceMins`

in minutes) a redirecting payment should be considered by the synchronization job and a status update from Concardis should be triggered.

The default value for the parameter `PendingSinceMins`

is 30 minutes.

For each order the administrator identified that it has an invalid state (payment status differs from Concardis), he has to copy the `orderID`

from the Intershop Commerce Management URL (see screenshot below).

To trigger the synchronization call to Concardis, the administrator has to perform a REST request to the (temporary) API endpoint: */INTERSHOP/rest/WFS/inSPIRED-Site/inTRONICS/payment/concardis/synchronizations.* The base URL is the same as in the ICM. In this example it is: */INTERSHOP/rest/WFS/inSPIRED-Site/inTRONICS.* Please use your own host and URL here.

**Example call:**

curl -X POST \ http://<server>/<base-url>/payment/concardis/synchronizations \ -u <order_manager>:<password> \ -H 'Accept: text/plain' \ -H 'Content-Type: application/json' \ -H 'cache-control: no-cache' \ -d '{"orderId" : "jfYKAB2_wIMAAAFuFd0.wqdp"}'

Alternatively, you can use the attached collection in the REST client Postman: Synchronize.postman_collection.json

All variables have to be replaced with data that is valid for your system. Instead of the user parameter an authorization header can be used for getting access to the endpoint. The administrator must have permissions to manage orders. This can be checked here:

The following table describes transmitted data by the Concardis Service Connector from ICM to Concardis during the payment process:

| Description | Concardis Payment Methods | ||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
| Alipay | Bancontact | Credit Card | Direct Debit | EPS | GiroPay | Paypal | Sofort | Ideal | |||
| Initial amount | Amount for the transaction | ||||||||||
| Currency details | Currency code e.g. EUR/USD | ||||||||||
| Customer Id | Customer e-mail and customer ID | ||||||||||
| Merchant order id | Order reference generated by the merchant | ||||||||||
| Channel | Terminal used at time of order (MOTO: Mobile phone, ECOM: PC) | ||||||||||
| Redirect URLs | Application URL for receiving callback response from Paygate | ||||||||||
| Notification URN | Application URN for receiving transaction notifications from Paygate | ||||||||||
| Address details | Invoice and shipping address details | ||||||||||
| Line items details | Details regarding product, shipping, discount, tax, gift card | ||||||||||
| Payment instrument Id | Tokenized identifier for customer account that can be stored and used for future transactions. | ||||||||||
| Credit card details | Card number, CVC, expiry date. Sensitive data is handled via PayGate iframes only and is never stored at the merchant. | ||||||||||
| 3-D Secure version | Credit card 3-D Secure version 1.0/2.0 | ||||||||||
| Browser information | Browser details like javaEnabled, language, colorDepth, timezone, screenHeight, screenWidth, windowSize | ||||||||||
| Account holder name | Name of the account holder | ||||||||||
| IBAN | International Bank Account Number | ||||||||||
| BIC | Bank Identifier Code | ||||||||||
| Direct debit type | One time payment (single) Stored account (first/recurring) |

Please be aware that Concardis Credit Card 3D Secure uses redirect after checkout. Intershop's current demo shop inSPIRED does not support a redirect after checkout if an order approval service in channel type `intershop.SMBResponsive`

is enabled.

REST support for redirect after checkout is available starting with ICM 7.10.13.4 release.

Starting from ICM 7.10.21, a new application type *Progressive Web App* is available and enabled for use with PWA 0.23.0 by default.

The new application type is not yet supported by the connector 1.10.x. Usage may lead to faulty handling in the PWA when using Credit Card or Direct Debit. To restore the old handling, the previous used application type has to be enabled again. To achieve this , the PWA 0.23.0 entry

icmApplication: 'rest'

in the PWA file `environment.ts`

has to be set back to

icmApplication: '-'

The new headless application type will be supported out of the box with Concardis version 1.11 and higher in combination with PWA 0.25.0++.

PWA 0.24.0 and Concardis 1.10 are not compatible at all due to different feature set development states.

Please be aware that partial capturing is only possible on Concardis side. Since the ICM only supports full capture in the commerce management, the refunds started from there cannot handle the fragmentation of the transactions. In case partial capturing via Concardis Merchant Interface is used, the refunding also has to be done there. The notifications will send updates to the ICM. If this is not considered and tried to refund an amount greater than the captured amount, the transaction goes into the final state "REFUND_FAILED".

It is important not to mix the types of the Concardis environment (*Live*/*Sandbox*). We recommend using the *Sandbox* environment in the testing system and the *Live* environment in the production system.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.