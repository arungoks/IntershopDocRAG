---
id: 'af3621cf9e19ccb76681acbeabf1d1d6'
title: 'Public Release Note'
url: 'https://knowledge.intershop.com/kb/index.php/Display/29973K'
scraped_at: '2026-04-21T05:37:38.537165+00:00'
---
Welcome to devenv-4-iom 1.2.

Devenv-4-iom is a toolset that supports different kinds of development tasks along with IOM docker images.

Intershop tries to provide best possible backward compatibility to older versions of IOM. Please use the newest version of devenv-4-iom, that is compatible with the IOM version you are using.

| devenv-4-iom \ IOM | 3.0 | 3.1 | 3.2 | 3.3 | 3.4 | 3.5 | 3.6 |
|---|---|---|---|---|---|---|---|
| 1.2.X | |||||||
| 1.1.2.0 | x | ||||||
| 1.1.1.0 | x | x | x | x | |||
| 1.1.0.0 | x | x | x | x | |||
| 1.0.0.0 | x | x | x | x | x |

x) Not supported

| Term | Description |
|---|---|
| Docker | An OS-level virtualization software. |
| Helm | A package manager for Kubernetes. |
| IOM | The abbreviation for Intershop Order Management. |
| Kubernetes | An open-source system for automating deployment, scaling, and management of containerized applications. |

A new property OMS_LOG_REST_IDS was added. It can hold a list of comma-separated operationIds. For any operationId listed here, corresponding REST requests/responses are logged into a debug message. OperationIds are part of the YAML specification of IOM REST interfaces. Also see [Guide - IOM REST-Logging](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1944634421/Guide+-+IOM+REST-Logging).

Example:

`OMS_LOG_REST_IDS=createOrder,createOrderResponse,createDispatch,createReturn`


The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.