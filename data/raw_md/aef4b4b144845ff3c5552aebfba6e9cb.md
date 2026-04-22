---
id: 'aef4b4b144845ff3c5552aebfba6e9cb'
title: 'Public Release Note'
url: 'https://knowledge.intershop.com/kb/index.php/Display/Q27741'
scraped_at: '2026-04-21T05:40:23.141489+00:00'
---
Welcome to the Intershop Computop Service Connector. The service connector adds Computop payment methods to your Intershop installation.

This document provides important product information, including version information and dependencies. It also outlines the basic setup and configuration steps.

This delivery and the accompanying documentation are valid for the following combinations of software versions:

| Intershop | Computop Service Connector |
|---|---|
7.6.2.5+ | 4.5.1 |
7.7.5.17+ 7.8.4.0+ 7.9.4.5+ 7.10.15.3 - 7.10.30.x (Tomcat 7) | 4.7.2 |

Computop Connector version 5.0.0 features the same functionality as Computop Connector 4.7.2 to facilitate migration from ICM 7.10.30 - to 7.10.31+.

The package includes the following cartridges:

The Computop Service Connector 4.5 is based on the new Payment API introduced in IS 7.6.

The Computop Service Connector can be used for the following application types:

| Application Type | Application Type ID | Description |
|---|---|---|
| B2C WebShop | `intershop.B2CResponsive` | Business to Consumer Channel |
| SMB WebShop | `intershop.SMBResponsive` | Business to Business Channel |

This section outlines the basic setup and configuration steps, including

Note

Managing and deploying the Computop Service Connector requires a continuous integration environment set up and configured as described in [Cookbook - Setup CI Infrastructure](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1822571078/Cookbook+-+Setup+CI+Infrastructure).

The package is available via Intershop's Public Nexus.

To add the Computop Service Connector into your Intershop 7 system, there are two options:

Incorporating the cartridge into an already existing assembly in the *build.gradle* file of the assembly. To do so, add:

cartridges { def computopPaymentProvider = [ 'ac_payment_computop' ] include (*(computopPaymentProvider.collect {"com.intershop.services.payment_computop:$it:4.7.2"}), in: [development, test, production]) ... order = listFromAssembly(<yourAssembly>) + computopPaymentProvider }

For details about adding components to an assembly, see [Recipe: Add Cartridges to an Assembly](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1788155636#Cookbook-GradleAssemblyTools(validto7.8)-AddCartridgestoanAssembly).

For details about managing assembly artifacts, see:

Before deploying the new assembly to a test or production environment, you may have to adjust some file-based configurations required by the Computop Service Connector.

The Computop Service Connector requires the following settings:

| Property | Description | Value |
|---|---|---|
| intershop.payment.computop.paygate | The base URL to the Computop paygate | Default value is
|

intershop.payment.COMPUTOP_CREDITCARD.success_pipeline

intershop.payment.COMPUTOP_CREDITCARD.success_b2b_pipeline

intershop.payment.COMPUTOP_CREDITCARD.failure_pipeline

intershop.payment.COMPUTOP_CREDITCARD.failure_b2b_pipeline

intershop.payment.COMPUTOP_ALIPAY.success_pipeline

ComputopPayPalRedirect-Notify

intershop.payment.COMPUTOP_CHINAPAY.success_pipeline

According to [Recipe: Change Deployed File Content With Filters](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1823702670/Cookbook+-+Deployment+Tools+ICM+7.8#Cookbook-DeploymentToolsICM7.8-ApplyContentFilter) this setting has to be overridden within *<IS_SHARE>/system/config/cartridges/ac_payment_computop.properties*.

For details about adding new configuration files, see [Recipe: Deploy Custom Files](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1823702670/Cookbook+-+Deployment+Tools+ICM+7.8#Cookbook-DeploymentToolsICM7.8-DeployCustomFiles).

After creating and appropriately configuring the assembly, you must deploy it to the intended target environment.

For details about deploying an assembly, see [Recipe: Run the Deployment (Initial Installation / Upgrade / Downgrade)](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1823702670/Cookbook+-+Deployment+Tools+ICM+7.8#Cookbook-DeploymentToolsICM7.8-Run-the-Deployment).

Note

The Computop Service Connector requires additional post-deployment configuration steps. For details, refer to [Configuration](https://knowledge.intershop.com#PublicReleaseNote-ComputopServiceConnector4-Configuration).

Since version 4.4.1 of the connector it is possible to modify the values of some of the parameters sent to Computop. Those parameters are `TransID, RefNr, PayID`

and `ReqID.`


To provide custom values of those parameters in one of the payment methods (e.g., Alipay):

Create a new class:

public class CustomAlipayRequestParamsProvider implements Function<RequestParamContext, String> { @Override public String apply(RequestParamContext paramContext) { switch(paramContext.getParamName()) { case "RefNr": ... ... default: return null; } } }

You retrieve the parameter name from the `RequestParamContext`

class. This class also provides the current `Payable`

and `PaymentContext`

objects, which could help you generate a value for the parameter.

If you wish to provide values only for a subset of the 4 supported parameters, return null for the rest - this way the default to the connector value will be used.

Bind your class in a custom Guice Module. In this case something like this:

bind(new TypeLiteral<Function<RequestParamContext, String>>() { }).annotatedWith(AlipayRequestParamsProvidier.class.getAnnotation(Named.class)) .to(CustomAlipayRequestParamsProvider.class).in(Singleton.class);

Define this custom Guice Module as `global.overrideModules`

in the associated resources file as described in [Concept - Dependency Injection and ObjectGraphs](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1774817917/Concept+-+Dependency+Injection+and+ObjectGraphs).

This section outlines the required post-deployment configuration steps, including

Adjust your firewall settings to allow bidirectional HTTP and HTTPS traffic between the Intershop 7 and Computop systems.

The Computop Service Connector requires some post-deployment configurations in the Organization Management application and in the Commerce Management application.

For details about enabling a payment service, see - [Recipe: Enable a Payment Service](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1811743798#Cookbook-Payment(validto7.7)-Recipe-EnableaPaymentService).

| Explanation | Image |
|---|---|
Log in to Organization Management. 1. Navigate to 2. Select the name of the organization. | |
3. Go to the 4. Click | |
5. Select the checkboxes of the new payment methods 6. Click |

| Explanation | Image |
|---|---|
Log in to Commerce Management. 1. Select the Organization/Channel. 2. Go to | |
3. Click New. | |
4. Select the 5. Click | |
6. Enter a Payment Service Name. 7. Enter "Service ID". 8. Select the checkbox for 9. Select the checkbox for 10. Click | |
11. Enter all Computop general settings. 12. Enter all logging settings. 13. Enter all monitoring settings. 14. Click | |
15. Select the (When setting up in the organization area, the service 16. Click |

The table below lists Computop-specific settings for configuring the payment service.

| Name | Payment Service | Description |
|---|---|---|
| Merchant ID | All | The merchant account's merchant ID as provided by Computop |
| Merchant Code | All | The merchant account's merchant code as provided by Computop |
| HMAC Code | All | The merchant account's HMAC code as provided by Computop |
| Capture | Credit Card, PayPal Standard | Capture mode (Manual, Auto, Timed). Timed is only available for Credit Card. If you use "Timed", you must set a "Capture Time in Minutes". |
| Capture Time in Minutes | Credit Card | When using Timed Capture, you may specify a delay in minutes after which the payment is captured |
| Zones | Credit Card | This describes the mode to validate clients (permit all, permit selected, forbid selected). If you use "permit selected" or "forbid selected", you must also set "Zone List (ISO 3166 Area Codes)" as a comma-separated list. |
| IP Zones | Credit Card | This describes the mode to validate client IPs (permit all, permit selected, forbid selected). If you use "permit selected" or "forbid selected", you must also set "IP Zone List (ISO 3166 Area Codes)" as a comma-separated list. |
| Storefront Name | All | This name is displayed in the storefront. |
| Order Description | All | This description will be submitted to Computop. |
| XSLT Template Path | Credit Card | Path to an XSLT template on the Computop server. |
| PCN | Credit Card | Store Pseudo Card Number generated by Computop at customer's profile. |

Note

Configuring payment methods in a sales channel requires the access privilege *Payment Manager* for this channel.

| Explanation | Image |
|---|---|
Enable the payment method for the channel. Log in to Commerce Management. 1. Select the context selection box. 2. Select the sales channel. | |
3. Go to 4. Go to | |
5. Click New. | |
6. Enter "Payment Method ID". 7. Select the Configuration Type. (This was created in the section 8. Click | |
9. Go to the 10. Select the checkboxes of all applications 11. Click | |
12. Go to the 13. Define taxation class, currency, minimum order value, amount 14. Click | |
15. Go to the 16. Enable the target customer segments. 17. Click | |
18. Go to the 19. Select the currency-dependent availability and the payment currency. 20. Click |

The Computop Service connector provides English and German localization files for payment-specific input field labels, error messages etc.

You can find the existing localization files here: *<IS.INSTANCE.SHARE>/system/cartridges/ac_payment_computop/release/localizations.*

For details about localization, see:

The Computop service connector adds the following payment methods to your Intershop 7 system:

| Name | Description | Payment Management Options |
|---|---|---|
Alipay | Payment with Alipay via Computop | Capturing Authorization Cancel** Refund |
Credit Card | Payment with credit card via Computop | Capture* Cancel* Refund |
| ChinaPay | Payment with ChinaPay via Computop | Capturing Authorization |
| Direct Debit | Payment with Direct Debit via Computop | Authorize Capture* Cancel* Refund |
| giropay | Payment with giropay via Computop | Capturing Authorization Refund |
PayPal Standard | Payment with PayPal via Computop | Capture* Cancel* Refund |
| PayPal Express | Payment with PayPal Express via Computop | Capture* Cancel* Refund |

* only available if the corresponding payment method's Capture Mode is set to "manual" or "timed".

** Alipay Cancel is only available to the customer in the storefront and actually executes a full refund.

| Operation | Description |
|---|---|
| Capture | Request for settling the payment |
| Cancel | Request for abandoning a payment settlement |
| Refund | Option to return (parts of) the captured amount |

The following table describes transmitted data by the Computop Service Connector from ICM to Computop during the payment process:

| Description | Payone Payment Methods | |||||||
|---|---|---|---|---|---|---|---|---|
| Paypal Standard | Paypal Express | Giropay | Credit Card | Direct Debit | Alipay | Chinapay | ||
| Amount | The amount for the transaction | |||||||
| Currency | currency code e.g. EUR/USD | |||||||
| Order Number | Order reference generated by merchant | |||||||
| Order Desc | Order description | |||||||
| Address | Invoice and shipping address details provided by the user (value is optional and configurable at back office) | |||||||
| Order ID | Order reference generated by the merchant ICM | |||||||
| Customer Info | Buyer related data B2C: firstname, lastname and e-mail B2B: company name and e-mail | |||||||
| Credit Card details | Credit card brand, Credit card expiry Sensitive data is handled via PayGate iframes only and is never stored at the merchant. | |||||||
| language (locale Code) | Language indicator to specify the language that should be presented to the customer | |||||||
| IBAN | International bank account number | |||||||
| BIC | Bank identifier code to be used for payment | |||||||
| accOwner | Account owner | |||||||
| accBank | Account bank | |||||||
| refNr | Reference number for direct debit transaction | |||||||
| dtOfSgntr | Date of signature |

| Symbol | Description |
|---|---|
| Transmitted | |
| Not Transmitted | |
| Optional - Back Office Configurable |

PayPal is not available for baskets with multiple shipping buckets.

Please be aware that Computop Credit Card uses redirect after checkout. Intershop's current demo shop inSPIRED does not support a redirect after checkout if an order approval service in channel type `intershop.SMBResponsive`

is enabled.

The IP Zones feature requires an IPv4 address on the customer's side. In case the customer has an IPv6 address, the payment method Credit Card will not be displayed on the payment page.

Scheduled timed captures (with delay), which were not yet processed when the server was shut down for some reason, will not be captured automatically. These payments must be captured manually.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.