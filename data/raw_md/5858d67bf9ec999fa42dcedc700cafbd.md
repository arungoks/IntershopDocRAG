---
id: '5858d67bf9ec999fa42dcedc700cafbd'
title: 'Concept - Headless Application Type'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2965H9'
scraped_at: '2026-04-21T05:39:50.689212+00:00'
---
Info

This concept is valid from Intershop Commerce Management 7.10.21.0.

Starting from Intershop Commerce Management 7.10.21.0, the headless application type *intershop.REST* is available. It is intended to be the application type of choice for headless REST applications for the ICM storefront, like the [Intershop Progressive Web App](https://github.com/intershop/intershop-pwa).

As the importance of the ICM REST API increases and the PWA storefront client application matures, a dedicated headless REST application type is required that is completely independent of the Responsive Starter Store. There are two other types of Responsive Starter Store applications (*intershop.B2CResponsive* and *intershop.SMBResponsive, *see [Concept - Application Framework](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1917324476/Concept+-+Application+Framework)) that offer the B2C and B2B REST API, but they also include the complete storefront. This is unnecessary overhead for the PWA and other REST client applications.

The *intershop.REST* application type is basically independent of *a_responsive* or the Responsive Starter Store. In addition it overcomes the separation of B2C and B2B functionality in different application types as well and provides the complete ICM REST API functionality within one application type. It is defined in the standard ICM component sets (*commerce_management_b2c* and *commerce_management_b2x*) and is available without using *a_responsive*.

The following table explains the implementation details of the *intershop.REST* application type.

| Component Set | Cartridge | Note | |
|---|---|---|---|
| Intershop Commerce Management | f_business | as_headless | Definition of the intershop.REST application type which combines all B2C REST API functionality |
| app_sf_headless | Minimum needed code artifacts for a headless application type (e.g. Prefix pipeline, ApplicationCallInterface, Component Framework) | ||
| app_sf_headless_emails | ISML e-mail templates used by the REST API (that can link to a headless application outside the ICM) | ||
| f_b2b | as_headless_b2b | Extends the intershop.REST application type with the complete B2B REST API functionality | |
| app_sf_headless_emails_b2b | ISML e-mail templates used by the B2B REST API (that can link to a headless application outside the ICM) | ||
| Responsive Starter Store | a_responsive | app_sf_base_cm | Definition of a basic content model that is bound to intershop.REST |
| app_sf_pwa_cm | Cartridge for PWA-specific CMS artifacts (e.g. includes) | ||
| demo_... responsive_... | Demo data and configuration |

The combined cartridges show that the *intershop.REST* application type contains B2C and B2B functionality in one application type. Therefore the application type itself will not distinguish an application as B2C or B2B application. The idea is to control the used/wanted functionality via feature switches in the client application (deployment settings). The application type itself will provide the complete REST API functionality.

The main functionality of *intershop.REST* is defined and combined in *f_business* and *f_b2b* and available with the standard ICM assemblies *commerce_management_b2c* and *commerce_management_b2x*. Most of the REST API functionality should therefore work with *intershop.REST* out of the box if one of these ICM assemblies would be deployed. However, the Responsive Starter Store component set *a_responsive* is used to add additional functionality to the headless application type.

Another aspect of *a_responsive* is the configuration of the SolrCloud adapter that is used by the */products* REST API. Furthermore *a_responsive* already contains demo data that is used with the headless application type.

There are currently no plans for creating an additional set of components for a headless only storefront deployment, so everything was added to the existing storefront component set.

For a headless project without the Responsive Starter Store, this component set could be used as starting point where all obsolete cartridges (*app_sf_responsive_...*) and content (*demo_...*) must be removed. So *a_responsive* offers the base for a Responsive Starter Store project, a PWA project or even a hybrid scenario, see [Hybrid Approach](https://github.com/intershop/intershop-pwa/blob/develop/docs/concepts/hybrid-approach.md) in the PWA GitHub documentation. It should be adapted to the requirements of the customer project.

From a REST application perspective, *intershop.REST* is basically a combination of *intershop.B2CResponsive* and *intershop.SMBResponsive*. It provides all the REST resources the other two application types provide without the Responsive Starter Store artifacts that are not required for a headless storefront. The combination of the REST resources of the two previous application types is no problem since the B2B functionality just adds additional resources.

There is only one exception for the */customers* resource that has an implementation in B2C and a different one in B2B under the same resource name. Within the combined application type the B2B implementation would hide the B2C implementation and the handling of Private Customers would not work anymore. To solve this problem the B2C */customers* resource is mapped to */privatecustomers* and with this change *intershop.REST* provides all the REST API functionality of the other two application types.

The *intershop.REST* application type does not provide information on whether an application is a B2C or B2B application. There is no such distinction anymore. It is only a matter of how an application is used. For this purpose, the REST client must be configured using feature toggles to determine whether the client acts as a B2C or B2B client. If a project requires distinct B2C and B2B applications, the *intershop.REST* application type could be copied and reduced to only provide the B2C REST API.

The headless application type should be the first choice when a project implements a new headless client, e.g. the Intershop PWA. The Responsive Starter Store application types will be discontinued in the future and should not be used for such projects. Also *intershop.REST* gets rid of all the not needed ISML templates, pipelines, styles etc. but only contains the ICM REST API in a PWA tested manner.

Projects that follow the [Hybrid Approach](https://github.com/intershop/intershop-pwa/blob/develop/docs/concepts/hybrid-approach.md) where parts of the storefront are handled by the Responsive Starter Store and other parts are handled with the PWA still need to use *intershop.B2CResponsive* and *intershop.SMBResponsive* even in the PWA.

Starting with Intershop PWA version 0.23.0 we switched to the new headless application type. This switch required adjustments regarding the changes in the used CMS content model. Almost all other parts work as before. This is also due to the fact that the application type is not used in any way to define whether the PWA acts as a B2C or B2B storefront. This is only controlled by the PWA deployments enabled [feature toggles](https://github.com/intershop/intershop-pwa/blob/develop/docs/concepts/configuration.md#feature-toggles).

However, there were changes required for handling the different */customers* and */privatecustomers* REST resources: The */customers* resource is used to login the user. This works well for business and private customers with the B2B */customers* resource. Once logged in, different resources must be used for further calls, depending on whether the user is a business customer (*/customers*) or a private customer (*/privatecustomers*).

This distinction is currently made based on the presence of a `customer.companyName`

(business customer) or its absence (private customer). This does not decide whether it is a B2B or a B2C shop, it could even be a mixed customers shop. It is only required to determine how the REST calls for the currently logged in user should be handled. It has no influence on REST calls that are not based on the */customers* resource.

There is also some handling implemented that takes care of the PWA still being compatible with the other application types *intershop.B2CResponsive* and *intershop.SMBResponsive* in regards to the */customers* resource.

With the headless application type, the storefront application could be completely independent from ICM, i.e. the ICM server has no information on how the headless application can be called or through which URL it is accessible. However, this information is necessary for the ICM to generate e-mails that point to the correct storefront or to open the correct URL for a storefront preview. A planned Design View integration for the PWA requires this information as well.

Within Intershop Commerce Management it is possible to configure this information. The new *intershop.REST* application allows to set an *External Base URL (*`ExternalApplicationBaseURL)`

.

This setting can be found in Intershop Commerce Management below the *Applications Tab | <Your intershop.REST application>*:

This setting can be used to to generate links to this headless application in ISML templates with the new `pwaURL()`

ISML function.

#pwaURL('/home')#

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.