---
id: 'da9b144b2dcb2bc93d2e63c09fbccd28'
title: 'Job'
url: 'https://knowledge.intershop.com/kb/index.php/Display/29475F'
scraped_at: '2026-04-21T05:39:02.621115+00:00'
---
Name | CleanUp |
|---|---|
Domain | root |
Job Dependencies | none |
AcquiredResources | none; can be extended via cartridge specific pipeline 'CleanUpPipeline' |
Cartridge | core |
Pipeline | CleanUp-Job |
| Parameter |
|
Affected Domain Objects | |
Affected Tables |
|
Stored Procedure |
sp_deleteReplicationProcesses sp_deleteCacheClearKeyBatchCtn (since 7.4.0.0)
|
Default State | Enabled |
Is Site Specific | False |
Edit State | Globally Enabled |
Live State | Locally Enabled |
Description | Removes expired pagecache database entries, old processes, expired instance resources. Since IS 7.4.0.0 it also removes expired batch cache clear containers and sync message responses . |
Scheduling | |
What Happens Switched Off | |
Trouble Shooting | |
Comments |

Product Version | 7.0 |
|---|---|
Product To Version | |
| Status |
|

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.