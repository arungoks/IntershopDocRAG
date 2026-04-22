---
id: 'dc292106aad6c68df5fd3dd8f4bde04c'
title: 'Guide - Intershop PWA'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2958A4'
scraped_at: '2026-04-21T05:40:44.673719+00:00'
---
The ICM provides a big variety of different REST resources managed by various teams and services.

As the maturity of resources varies, so does the format of HTTP errors provided by those endpoints.

The classic error response was submitted via HTTP headers and slowly the new format of providing even localized messages in the body of an error is being implemented.

For the PWA this means that potentially every service and component managing a different resource has to handle different formats.

In version 0.23 of the PWA we refactored the error handling to provide a consistent simplified format for all HTTP errors throughout the application.

Most of the work is done by the [HttpInterceptor](https://angular.io/api/common/http/HttpInterceptor) [ICMErrorMapperInterceptor](https://raw.githubusercontent.com/intershop/intershop-pwa/develop/src/app/core/interceptors/icm-error-mapper.interceptor.ts).

It converts responses with `error-key`

headers, responses with `errors`

body and also provides a fallback mapping for errors not matching this format.

💡 Mapping the

[HttpErrorResponse]is mandatory as the object itself is not serializable and should therefore not be pushed into the[State Management]!

If necessary, you can provide a custom [SPECIAL_HTTP_ERROR_HANDLER](https://raw.githubusercontent.com/intershop/intershop-pwa/develop/src/app/core/interceptors/icm-error-mapper.interceptor.ts) for a specific use case.

All custom mappers should be provided in the [ConfigurationModule](https://raw.githubusercontent.com/intershop/intershop-pwa/develop/src/app/core/configuration.module.ts).

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.