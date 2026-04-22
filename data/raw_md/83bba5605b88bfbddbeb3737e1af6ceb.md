---
id: '83bba5605b88bfbddbeb3737e1af6ceb'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/3117P5'
scraped_at: '2026-04-21T05:29:40.522867+00:00'
---
This document describes ICM versioning approach in the context of release compatibility.

ICM 11+ versioning follows the compatibility aspect only. The transition from ICM 11 to ICM 12 is similar to upgrading from a larger patch step of ICM7.10.

ICM uses semantic versioning (v2). For more information, refer to [https://semver.org](https://semver.org).

Major - contains breaking changes - Going forward to this release **can** break a customization (it does not matter how high the probability is).

Minor - contains additional functionality - Going forward to this release **should not** break a customization. Going back from this release **can** break the customization.

Patch - contains fixed functionality - Going forward and backward to this release **should not** break a customization.

Suffix - optional part of the version number to provide additional information for usage (such as -dev) .

"Functionality" means any kind of functionality, not only features. With a minor release, a new Java method can be introduced. Using this new method will break the going back path for the customization.

DBPrepare (formerly DBMigrate) compatibility is similar. If a customization breaks with a change, this change should be part of a major version. Adding new tables or columns is tracked with a minor version increment.

Third party library updates are tracked at the same level as the library update. If a minor or patch release produces breaks in the standard product, the update is postponed until the next major release.

ICM 11 introduces a new [customization concept](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/48444277617/Overview+-+Customization+-+Development+Process+-+ICM+11). Each release of a customization has its own version number. It is not necessary to create releases for customization for each ICM release anymore. But it is recommended to test customization at least for each minor release. The [ICM 11 releases page](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/48544023888/Reference+-+ICM+11+Release+Versions) provides an overview of ICM and customization release numbers. Standard customization also follows semantic versioning.

Up to ICM 7.10, new product versions were determined by marketing, product increment (effort), and compatibility considerations. ICM 7.10 has evolved from a standard GA release to a generation of ICM versions.

A product version of Intershop Commerce Management has 4 digits, e.g. 7.6.3.14.

The four positions have the following meaning:

Generation (e.g. 7) – New product generation (marketing driven)

GA (e.g. 6) – Public release with new functionality

Deprecation is allowed (two minor versions minimum)

APIs can be broken, but must be documented

Patch (e.g. 3) – May contain bug fixes or new features

Product Acceptance- and Performance Tests are performed

(Exceptions minor updates must be approved by product steering)

Minor updates of third party libraries

APIs can be broken, but must be documented

Hotfix (e.g. 14) – Bug fixes or features shipped to the customer as soon as possible

Contains all previous hotfixes

Only non-API breaking features can be released

No minor updates are allowed

Patch updates of third party libraries

The product is technically defined by a version of an assembly. The product version number is the version number of the assembly (Intershop7). This assembly contains dependency declarations (including versions) of components. These components can follow their own version schema.

The following table shows the relation between component version and product version.

For example, a new major version of a component (e.g., f_business) results in a new patch version of the product.

Component | Product | Customer Expectation |
|---|---|---|
- | Generation (7) | |
- | GA (10) | |
Major | Patch | dbmigrate or migration of customization necessary |
Minor | Hotfix | new functionality without migration of customization |
Patch | Hotfix | code patches without migration of customization |
Suffix | -LTS -dev1 | suffix for Long Term Support or development version |

Components are bundled in component sets, similar to multi-projects.

Component sets follow their own life cycle, starting with version 1.0.0. In the binary repository, these sets have their own group, for example:

com.intershop.platform:core:1.0.0

The source code of one or more **components** may remain unchanged after some changes have been made to the source code (including dependencies) of the **component set**. Nevertheless, the version number is incremented for both the changed and unchanged components, because a component is part of a larger group of components that share the version.

The versioning is based on the semantic versioning concept ([http://semver.org/](http://semver.org/)).

Example: com.intershop.platform:bc_service:10.0.4

Goal:

Remove deprecated methods, classes

Rework features

Introduce new features with database changes

You can:

Introduce any changes

Example:

**10**.0.4

Please consolidate major updates, so that partners do not have to migrate their customizations with each release.

Goal:

Add new functionality without breaking the existing customization

Backward compatible (existing implementations are still working)

Deployment can do rolling update (means older versions may run in parallel)

Migration of customization is mostly not necessary (only in edge cases), e.g.:

Test cases require new mocks (used via DI)

Existing private/protected methods, members could reduce the visibility of new introduced methods/members

You can:

Patch and minor level updates of libraries (or underlying component sets)

Add new dependencies

Add APIs

Deprecate APIs

You cannot:

Remove API

Add abstract methods (e.g., interfaces)

Introduce DBMigrate

Example:

10.**0**.4

Goal:

Implementations will work against all patches of a minor version

Customization layer can jump forward or backward without problems

No migration of customization necessary

Deployment can do rolling update (means older versions may run in parallel)

You can:

Fix behavior

Add documentation for API

Patch level updates of libraries (or underlying component sets)

Add classes or interfaces to "internal" packages

Deprecate classes or interfaces in "internal" packages

You cannot:

Touch APIs (except documentation)

Add or remove parts of API

Deprecate APIs

Introduce DBMigration

Add injection of members

You should not:

Remove internal classes or interfaces (may be used in projects)

Example:

10.0.**4**

Goal:

Provide fixes with minimal code impact to the patch, in case the following patch was released before

You can:

Fix behavior

Add documentation regarding the fixed behavior

Example:

10.0.4**-SP1**

REST API

Java API

Managed Service APIs

REST API is independent of component versioning. REST API uses semantic versioning when the REST API definition (extractable from OpenAPI definition) has been modified.

MAJOR - API breaks (e.g. removed resources)

MINOR - new resource

PATCH - documentation changes (optional)

Completely independent components can be implemented in a single project build. These components are collected in a special group named "com.intershop.common", e.g.:

com.intershop.common:encryption:1.1.0

A component set can define an API as well. This is a common approach if there is no default implementation, see `javax.inject:javax.inject:1`

at [http://mvnrepository.com/artifact/javax.inject/javax.inject/1](http://mvnrepository.com/artifact/javax.inject/javax.inject/1). This approach is used for "Service API", so modification of this type of API can be separated.

Managed service interfaces are located in components. The API of a component contains such interfaces. Therefore, the component version declares major, minor changes of that API too.

f_api is a separate API component set. This component set can contain multiple service interfaces. The product can also support multiple versions of an API.

So, the package contains the major version number of that package too. This component set con contain, for example:

com.intershop.api.data.common.v1

com.intershop.api.data.common.v2

com.intershop.api.service.payment.v1

com.intershop.api.service.taxation.v2

Under some circumstances, service interfaces are marked with a @BETA annotation. This means, this interface is marked as possibly unstable. Incompatible changes to such interfaces must be marked with a new MAJOR version of the component set (semantic version), but it is not necessary to create a new package with the new major version.

Extension | Description | Goal |
|---|---|---|
-LTS | long term support release | The release contains bugfixes or security fixes only - customer/partner should use the newest -LTS release for production environment. Starting from ICM 12, LTS is no longer in use. |
-dev | development release | Internal development integration tests - stick to a specific commit. |
-rc | release candidate | Implementation partner can use it for project start or first customer shipment. |
(no) | public release | General availability for all customers and implementation partners. |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.