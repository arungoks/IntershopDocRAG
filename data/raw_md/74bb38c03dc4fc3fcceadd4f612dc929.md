---
id: '74bb38c03dc4fc3fcceadd4f612dc929'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/308K57'
scraped_at: '2026-04-21T05:34:57.485525+00:00'
---
The Intershop Integration Hub is a platform for connecting different systems and applications in e-commerce projects. This document outlines the architecture, purpose, and features of the platform, as well as the business processes it covers.

The target audience for this document are developers working on Intershop implementation projects. The platform is meant to facilitate the exchange of orders, order history, inventory, customer data, prices, and product information, among other business objects.

The Intershop Integration Hub uses a low-code approach, meaning integration can be achieved without extensive programming. It provides a flexible and scalable solution for automating business processes, reducing manual effort, and improving efficiency. Features such as monitoring, logging, data mapping, and transformation are included to help manage integrations effectively.

This document provides an overview of the Intershop Integration Hub and its capabilities, aimed at helping developers understand the platform and make informed decisions on how to use it in their projects.

[https://community.simplifier.io/doc/current-release/integrate/connectors/](https://community.simplifier.io/doc/current-release/integrate/connectors/)

[https://community.simplifier.io/doc/current-release/integrate/business-objects/](https://community.simplifier.io/doc/current-release/integrate/business-objects/)

The Intershop Integration Hub fits well into a composable architecture as the low-code integration layer that connects the packaged business capabilities and the systems of record. The Intershop Integration Hub offers a range of connectors that allow for the integration of different systems and applications, without the need for custom code.

The Intershop Integration Hub is based on the low-code platform [Simplifier](https://simplifier.io/en/), operated by Intershop.

There are two typical integration scenarios between Intershop ICM/IOM and the Intershop Integration Hub.

Intershop calls the Integration Hub.

In this scenario, the Integration Hub has a business object configured that exposes its methods as REST API. This REST API is then called by Intershop ICM or IOM, for example, by a service adapter of the ICM Managed Service Framework.

The Integration Hub calls Intershop ICM or IOM.

In this scenario, the Intershop REST API is called by the Integration Hub. A business object configured in the Integration Hub controls the flow of data using business object script. The business object uses preconfigured connectors to easily connect to ICM/IOM or the systems of record.

The Intershop Integration Hub comes with a set of standardized connectors, most importantly REST, SOAP, SAP RFC, ODATA V2, CSV. These connectors can be easily configured and interactively tested.

Connectors can be generated automatically using the connector wizard for SAP, OpenAPI (Swagger) documentation for REST, or a SOAP WSDL.

Connectors do not contain any business logic, they basically just wrap the API calls, similar to Postman collections.

For more information see: [https://community.simplifier.io/doc/current-release/integrate/connectors/](https://community.simplifier.io/doc/current-release/integrate/connectors/).

The Integration Hub often relies on the *SAP Java Connector* (SAP JCo) for native SAP integrations.

As the SAP JCo has reached its end of life (EOL) for certain versions, SAP has moved to newer integration technologies, focusing on OData, RESTful APIs, and the *SAP Cloud Connector* for more secure and flexible integrations. These methods are also supported by the Intershop Integration Hub.

For SAP, the following login methods are supported:

|
|
|---|---|
Username or Alias | Uses only a username as credential |
Username and Password | Uses a username and password combination |
SAP Logon Ticket | Uses an SAP Logon Ticket as credential |
Token | Uses a generic token as credential |
OAuth 2.0 | Uses an OAuth 2.0 token as credential |
SAML 2.0 | Uses a SAML 2.0 assertion token as credential |
Certificate | Uses a certificate as credential |

*SAP Logon tickets* are included.

*The SAP Cloud Connector* is supported for secure access to on-premise SAP systems from the cloud. The Cloud Connector acts as a bridge, securely connecting the Integration Hub (in the cloud) to SAP backend systems without exposing the SAP system directly to the Internet.

To implement mapping or caching logic, the Intershop Integration Hub provides the concept of Business Objects. Business Objects can have functions (methods). Functions have input and output parametes. The function itself is implemented in so called Business Script which is a variation of JavaScript. Within the business script it is easily possible to call connectors and to handle the JSON responses. This approach is very flexible, so that even complex mapping or caching logic can be implemented quickly and efficiently.

Every business object function is automatically exposed as REST API and can be used externally.

For more information see: [https://community.simplifier.io/doc/current-release/integrate/business-objects/](https://community.simplifier.io/doc/current-release/integrate/business-objects/).

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.