---
id: '7a45f133a9b36a42ced74eaeb4fdbbea'
title: 'Job'
url: 'https://knowledge.intershop.com/kb/index.php/Display/29U503'
scraped_at: '2026-04-21T05:40:45.954315+00:00'
---
Name | Run Cache Refresh |
|---|---|
Domain | SMC |
Job Dependencies | none |
AcquiredResources | none |
Cartridge | smc |
Pipeline | DevelopmentHelpers-RunRefreshCache |
Affected Domain Objects | The ORM cache of each business object is cleared. |
Affected Tables | Only memory |
Stored Procedure | none |
Default State | Disabled |
Is Site Specific | False |
Edit State | Disabled |
Live State | Disabled |
Description | Forces the execution of the RefreshCache pipelet. This invalidates the whole ORM cache. |
Scheduling | On demand. |
What Happens Switched Off | ORM cache is not touched or partly cleared. |
Trouble Shooting | |
Comments |

Product Version | 7.0 |
|---|---|
Product To Version | |
| Status |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.