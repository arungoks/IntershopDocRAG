---
id: 'e26cfecfbfe29c334079cefbf7e8bed2'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2728F6'
scraped_at: '2026-04-21T05:39:29.117814+00:00'
---
Intershop Order Management (IOM) uses Representational State Transfer (REST)**. **The present concept gives some basic information about the IOM's REST service handling.

This concept is primarily intended for all developers implementing a project or working with the core product of IOM.

IOM supports *basic http authentication* only. Please configure your clients to use this authentication method. A very simple method to send REST requests on the command line can be realized using `wget`

. The example also shows, how to configure this client to use *basic http authentication* (`--auth-no-challenge`

).

wget -q -O- --auth-no-challenge --http-user=<user> --http-password='<password>' \ http://<hostname>/<REST URL>

Allowed HTTP Requests

The following requests show the general existing HTTP requests. Not all requests are required for each service.

`POST`

- Creates or updates a resource

`PUT`

- Updates a resource

`GET`

- Retrieves a resource or list of resources

`DELETE`

- Delete a resource

`200 `

OK - The request was successful.

`201 `

Created - The request was successful and a resource was created.

`204 `

No Content - The request was successful but there is no representation to return (that is, the response is empty).

`400 `

Bad Request - The request could not be understood or was missing required parameters.

`401 `

Unauthorized - Authentication failed or user does not have permissions for the requested operation.

`403 `

Forbidden - Access denied.

`404 `

Not Found - Resource was not found.

`405 `

Method Not Allowed - Requested method is not supported for the specified resource.

`503 `

Service Unavailable - The service is temporary unavailable (e.g., due to scheduled platform maintenance). Try again later.

All API responses will be returned by the following JSON envelope. Errors, and exceptions are only present if they occur:

{ "data": { "validUntil": "2014-12-19 11:25:00", "resvId": "sdfdk43ß445lksld0394", "items": [ { "id": "BDJs-3432", "qty": 2, "state": "reserved" }, { "id": "AFEz-5562", "qty": 1, "state": "reserved" } ] }, "errors": [], "exceptions": [] }

The `data`

section contains the resource object for a success, typically a status code 200.

The `errors `

section contains validation errors when a request fails. On a success, this data is empty.

"errors": [ { "message": "The value must be an integer", "sourceField": "qty" }, { "message": "The reservation type is invalid", "sourceField": "type" }, { "message": "required", "sourceField": "shop" }, ]

The `exceptions `

section contains exceptions that are thrown when a request fails due to an invalid request or code error. On a success, this data is empty.

"exceptions": [ { "code": "20001", "message": "The requested id BDJs-3432 was not found " }, { "code": "20002", "message": "The requested shop 1 was not found " } ]

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.