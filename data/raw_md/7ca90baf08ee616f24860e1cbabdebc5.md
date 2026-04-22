---
id: '7ca90baf08ee616f24860e1cbabdebc5'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/B28938'
scraped_at: '2026-04-21T05:37:49.559142+00:00'
---
Intershop Order Management (IOM) has the ability to configure approval processes in order to interrupt the overall processes, e.g., the *Order Business Processes*, for various reasons (e.g., authorization, fraud prevention, etc.). This document describes the basic concepts of approvals within the IOM. The target audience are consultants and developers.

| Term | Description |
|---|---|
| IOM | The abbreviation for Intershop Order Management |
| OMS | The abbreviation for Order Management System, the technical name of the IOM |
| OMT | The abbreviation for Order Management Tool, the graphical management tool of the IOM |
| Return request | Also return announcement, a request from a customer to the seller for sending back products of a previously delivered order |
| RMA | The abbreviation for Return Merchandise Authorization or Return Material Authorization |

The *RMA Approval Process* is able to interrupt the *Return Request Business Process* for the reason of authorization. If approval is required it can be accepted or rejected, and finally can be exported to a 3rd party system.

If necessary, the return request keeps in a `DO_APPROVE`

state, until it is approved or rejected by a user in the OMT or by a 3rd party system with the help of the IOM REST API - RMA, see [Overview - Intershop Order Management REST API](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1910440913/Overview+-+Intershop+Order+Management+REST+API).

By default, all return requests will be exported in the [Transmit a Return Request](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1859666021/Concept+-+IOM+RMA+Business+Process#Concept-IOMRMABusinessProcess-thetransmit-a-return-request) process. In order to prevent rejected return request from being exported, the export could be configured. For further details, see [Reference - IOM ImpEx Export RMA](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1854902670/Reference+-+IOM+ImpEx+Export+RMA).

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.