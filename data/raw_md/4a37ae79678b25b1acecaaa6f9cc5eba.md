---
id: '4a37ae79678b25b1acecaaa6f9cc5eba'
title: 'Public Release Note'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2T9904'
scraped_at: '2026-04-21T05:40:23.873724+00:00'
---
Welcome to Intershop Order Management 3.5!

*Intershop Order Management* (IOM) is an application of the *Intershop Commerce Suite* (ICS) that is designed to combine omni-channel commerce processes into one system. It automates and streamlines the life cycle of orders and payments. IOM processes orders from multiple touch points (web shop, mobile shop, call center and more), allocates them to multiple fulfillment solutions (fulfillment centers, drop-ship distributors, physical stores and more), and tracks all order and payment transactions.

IOM offers a centralized platform for managing distributed inventory, order, invoice and payment life cycles, and provides call center functionality, enabling real-time visibility into customers' purchasing behavior, stock levels, payments, and more. As part of ICS, it utilizes the suite's transaction, PIM and merchandising features.

IOM offers the possibility to tailor your business models as flexible and free as you need and depict them in your e-commerce environment. The order management system adjusts the order processing for various sales channels and suppliers and can be seamlessly integrated with existing components of your IT environment.

| Term | Description |
|---|---|
| API | Application Programming Interface |
| Docker | An operating system-level virtualization software. Also see Kubernetes and Helm. |
| Helm | A package manager for |
| ICM | Abbreviation for Intershop Commerce Management |
| IOM | Abbreviation for Intershop Order Management |
| Kubernetes | An open-source system for automating deployment, scaling, and management of containerized applications. Also see |
| OMS | Abbreviation for Order Management System, the technical name of the IOM |
| OMT | Abbreviation for Order Management Tool , the graphical management tool of the IOM |
| REST | Representational State Transfer |

With the IOM Order REST API 2.2, IOM now supports creating change requests for an order in certain statuses using a REST API, see [Reference - IOM REST API - Order 2.2](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930415972/Reference+-+IOM+REST+API+-+Order+2.2).

See [Concept - IOM Order Change](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930423820/Concept+-+IOM+Order+Change) to get more insights for this first MVP. The [Cookbook - IOM Order Change](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930415246/Cookbook+-+IOM+Order+Change) explains selected use cases.

The following infrastructure components were updated:

IOM is now running in Wildfly 23.0.1.Final. Projects have to use the updated dependencies.

The IOM REST API Order 2.2 offers additional endpoints to:

The specification can be found in the delivery *doc/REST/ *or in the [Knowledge Base](https://knowledge.intershop.com/kb/?q1=API).

For more information also see [Reference - IOM REST API - Order 2.2](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930415972/Reference+-+IOM+REST+API+-+Order+2.2) and [Fixed Defects](https://knowledge.intershop.com#PublicReleaseNote-IntershopOrderManagement3.5-FixedDefects) below.

For installation instructions see:

Docker-images are available at:

Helm Charts are available at:

For a complete list of all interfaces please see [Overview - Intershop Order Management REST API](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1910440913/Overview+-+Intershop+Order+Management+REST+API) and [Overview - IOM Interfaces](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1811750501/Overview+-+IOM+Interfaces).

| ID | Title |
|---|---|
|

Also deprecated are:

get|setReturnPosTransmissionPropertyList() of ReturnPosTransmissionDO, use get|setPropertyList() instead

get|setReturnPosPropertyList() of ReturnPosDO, use get|setPropertyList() instead

get|setReturnItemPropertyList() of ReturnItemDO, use get|setPropertyList() instead

get|setReturnTransmissionPropertyList() of ReturnTransmissionDO, use get|setPropertyList() instead

get|setResponsePosTransmissionPropertyList() of ResponsePosTransmissionDO, use get|setPropertyList() instead

Shop2SupplierDO.getSupplierSupportsCOD(), use isSupplierSupportsCOD() instead

CommunicationDO.isActiveOMT(), use getActiveOMT() instead

get|setIsDoProcess(), set|getIsDoManualApprove() of PaymentActionApprovalDefDO, set|isDoProcess(), set|isDoManualApprove() instead

SupplierOrder.getOrderPosDOList(), use getOrderPosDOList instead

OrderDO.getBillingAddresses(), use getBillingAddress() instead

Please also see [Guide - IOM 3.5 Deprecations and Removals](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930409724/Guide+-+IOM+3.5+Deprecations+and+Removals) for more details about [IOM-11175](https://knowledge.intershop.com/kb/go.php/o/62988) - Deprecated obsolete classes and methods that are used by the already deprecated order state service

| ID | Title |
|---|---|
|

Possible database migration error due to a trigger definition

| ID | Title |
|---|---|
|

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.