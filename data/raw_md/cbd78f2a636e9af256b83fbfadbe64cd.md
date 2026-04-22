---
id: 'cbd78f2a636e9af256b83fbfadbe64cd'
title: 'Reference - IOM REST API'
url: 'https://knowledge.intershop.com/kb/index.php/Display/3M0702'
scraped_at: '2026-04-21T05:38:21.136857+00:00'
---
This reference is intended for developers and lists available endpoints of the IOM Reservation REST API.

URI | servlets/services/reservation/<resvId> |
|---|---|
Http Method | GET |
Short Description | Used to get a stock reservation. Usually called to check the validity of a stock reservation. |
Example Requests URL | |
| Example Requests | No Content |
HTTP Status Codes |
|
Description | The IOM enables shop systems to get stock reservations via HTTP GET requests via ID. This service supports only the content-type application/json. |
| Parameters | Path parameter resvId = ID of the requested stock reservation |

IOM supports "basic http authentication" only. Please configure your clients to use this authentication method. A very simple method to send REST requests on the command line can be realized using wget. The example also shows, how to configure this client to use "basic http authentication" (--auth-no-challenge).

wget -q -O- --auth-no-challenge --http-user=<user> --http-password='<password>' \ --method=get http://<hostname>/servlets/services/reservation/117

`oms.RightDefDO`

with ID = 124 and name "Reservation REST service") is assigned to the requesting user. The permission is a part of the class `bakery.persistence.dataobject.configuration.common.RightDefDO`

.Request data format | application/json | ||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Request related java object | n/a | ||||||||||||||||||||||||||
Request data example | No Content | ||||||||||||||||||||||||||
Response data format | application/json | ||||||||||||||||||||||||||
Response related java object | bakery.webservice.rest.v1.HttpResponse bakery.reservation.v2.ReservationResponse as "data" object | ||||||||||||||||||||||||||
| Response Attributes |
| ||||||||||||||||||||||||||
Response data example | { "errors": [ ], "statusCode": 200, "exceptions": [ ], "data": { "validUntil": "2016-01-06 15:05:30", "resvId": 118, "items": [ { "id": "First-Test", "qty": 3, "state": "reserved" }, { "id": "First-Test", "qty": 2, "state": "reserved" } ] } } | ||||||||||||||||||||||||||
| Response Code | 200 |

URI | servlets/services/reservation/<resvId> |
|---|---|
Http Method | PUT |
Short Description | Update a stock reservation. |
| Example Requests URL |
|

Example Requests

HTTP Status Codes

201 Created

Stock reservation suspenseful updated

400 Bad Request

There is no reservation in the OMS system for parameter resvId or in the case of a semantic or syntactic error.

401 Unauthorized

404 Not Found

500 Internal Server Error

Description

This `PUT`

method updates an existing stock reservation. Unlike the `POST`

method to create a new reservation, this method updates specific information of an existing stock reservation. You can update the validity of a reservation. You can remove already reserved products from a reservation or add other products (reservation items). Furthermore, the reserved quantity of an already reserved product can be changed.

If the reservation is already expired each product reservations will be removed and the OMS perform the creation of new reservation items like the POST method it does. At the response appears an exception with code 21004 and message " The reservation with id <resvId> has already expired".

This service only supports and accepts requests with content-type application/json.

IOM supports "basic http authentication" only. Please configure your clients to use this authentication method. A very simple method to send REST requests on the command line can be realized using wget. The example also shows, how to configure this client to use "basic http authentication" (--auth-no-challenge).

wget -q -O- --auth-no-challenge --http-user=<user> --http-password='<password>' \ --method=put --body-data='{"lifetime":60, "items":[{"id":"First-Test", "qty":7}]}' \ http://<hostname>/servlets/services/reservation/130

It is Important that the permission REST_RESERVATION (`oms.RightDefDO`

with ID = 124 and name "Reservation REST service") is assigned to the requesting user. The permission is a part of the class `bakery.persistence.dataobject.configuration.common.RightDefDO`

.

The user also needs the permission for the IOM shop instance which relates to the requested stock reservation.

To avoid overbooking of products the OMS checks the current inventory of the product before storing the reservation. The inventory check itself depends on stock reservations. For this reason the OMS uses database advisory locks to serialize the requests.

If it is not possible for a request to obtain all locks for the products to reverse within five seconds, the client gets a response with HTTP status code 500 and the following payload:

{ "data": null, "statusCode": 500, "errors": null, "exceptions": [{ "code": "500", "message": "bakery.util.exception.TechnicalException: Technical error while working on object 'ReservationPersistenceBean': Unable to update reservation. Cannot get the necessary database lock to perform a concurrent safe inventory check." }] }

Request data format | application/json | |||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Request related java object | bakery.v2.reservation.ReservationRequestImpl | |||||||||||||||||||||||||||||||
| Request Attributes |
| |||||||||||||||||||||||||||||||
| Request data example | { "lifetime": 180, "items": [ { "id": "First-Test", "qty": 7 } ] } | |||||||||||||||||||||||||||||||
Response data format | application/json | |||||||||||||||||||||||||||||||
Response related java object | bakery.webservice.rest.v1.HttpResponse bakery.reservation.v2.ReservationResponse as "data" object | |||||||||||||||||||||||||||||||
| Response Attributes |
| |||||||||||||||||||||||||||||||
Response Attribute Errors |
HTTP status code = 400 | |||||||||||||||||||||||||||||||
| Response Attribute Exceptions |
| |||||||||||||||||||||||||||||||
Response data example | { "data": { "validUntil": "2016-01-07 14:29:32", "resvId": 130, "items": [ { "id": "First-Test", "qty": 7, "state": "reserved" } ] }, "statusCode": 201, "errors": [ ], "exceptions": [ ] } | |||||||||||||||||||||||||||||||
| Response Code | 201 |

URI | servlets/services/reservation/<shopId> |
|---|---|
Http Method | POST |
Short Description | Create a stock reservation. |
| Example Requests URL |
|

Example Requests

HTTP Status Codes

201 Created

400 Bad Request

401 Unauthorized

404 Not Found

500 Internal Server Error

Description

This service creates stock reservations for a given OMS shop instance. A stock reservation is a list of reserved products with the appropriate amount. Each stock reservation has a validity which can be set by the field `lifetime`

at the request payload.

The response provides a status code 201 on success with the reserved products, the state of the reservation and a unique reservation reference ID.

This service only supports and accepts requests with content-type application/json.

`shopId`

= ID of the OMS shop instance - Example = 10010IOM supports "basic http authentication" only. Please configure your clients to use this authentication method. A very simple method to send REST requests on the command line can be realized using wget. The example also shows, how to configure this client to use "basic http authentication" (--auth-no-challenge).

wget -q -O- --auth-no-challenge --http-user=<user> --http-password='<password>' \ --method=post --post-data='{"lifetime":180, "type":"COMPLETE", "items":[{"id":"First-Test", "qty":"2"}]}' \ http://<hostname>/servlets/services/reservation/10010

`oms.RightDefDO`

with ID = 124 and name "Reservation REST service") is assigned to the requesting user. The permission is a part of the class `bakery.persistence.dataobject.configuration.common.RightDefDO`

.The user also needs the permission for the OMS shop instance which relates to the requested stock reservation.

Concurrency

To avoid overbooking of products the OMS checks the current inventory of the product before storing the reservation. The inventory check itself depends on stock reservations. For this reason the OMS uses database advisory locks to serialize the requests.

If it is not possible for a request to obtain all locks for the products to reverse within five seconds, the client gets a response with HTTP status code 500 and the following payload:

JSON

Request data format | application/json | |||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Request related java object | bakery.v2.reservation.ReservationRequestImpl | |||||||||||||||||||||||||||||||
Request Attributes |
| |||||||||||||||||||||||||||||||
Request data example | ||||||||||||||||||||||||||||||||
Response data format | application/json | |||||||||||||||||||||||||||||||
Response related java object | bakery.webservice.rest.v1.HttpResponse bakery.reservation.v2.ReservationResponse as "data" object | |||||||||||||||||||||||||||||||
Response Attributes |
| |||||||||||||||||||||||||||||||
Response AttributeErrors |
HTTP status code= 400 | |||||||||||||||||||||||||||||||
Response AttributeExceptions |
HTTP status code= 400 | |||||||||||||||||||||||||||||||
Response data example | { "data": { "validUntil": "2016-01-07 15:03:36", "resvId": 119, "items": [ { "id": "First-Test", "qty": 2, "state": "reserved" } ] }, "statusCode": 201, "errors": [ ], "exceptions": [ ] } | |||||||||||||||||||||||||||||||
Response Code | 201 |

URI | servlets/services/reservation/<resvId> |
|---|---|
Http Method | DELETE |
Short Description | Remove a stock reservation. |
Query Parameters | none |
Example Requests |
|

HTTP Status Codes

400 Bad Request

there is no reservation in the OMS system for parameter resvId

401 Unauthorized

404 Not Found

500 Internal Server Error

Description

Remove Stock Reservation - API

Used by shop systems to delete an existing stock reservation from the IOM system.

IOM supports "basic http authentication" only. Please configure your clients to use this authentication method. A very simple method to send REST requests on the command line can be realized using wget. The example also shows, how to configure this client to use "basic http authentication" (--auth-no-challenge).

wget -q -O- --auth-no-challenge --http-user=<user> --http-password='<password>' \ --method=delete http://<hostname>/servlets/services/reservation/115

`oms.RightDefDO`

with ID = 124 and name "Reservation REST service") is assigned to the requesting user. The permission is a part of the class `bakery.persistence.dataobject.configuration.common.RightDefDO`

.JSON

Request data format | No Content |
|---|---|
Request related java object | n/a |
Request data example | n/a |
Response data format | No Content |
Response related java object | n/a |
Response data example | n/a |
| Response Code | 204 |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.