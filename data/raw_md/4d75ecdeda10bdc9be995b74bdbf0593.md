---
id: '4d75ecdeda10bdc9be995b74bdbf0593'
title: 'Job'
url: 'https://knowledge.intershop.com/kb/index.php/Display/N29506'
scraped_at: '2026-04-21T05:40:47.104021+00:00'
---
Name | REPORT_TransferData |
|---|---|
Domain | root |
Job Dependencies | REPORT_* jobs must be run first (to collect the data) |
AcquiredResources | ReportingRepository_Root, ReportingRepository_* (reporting repository sub directories) |
Cartridge | report |
Pipeline | SSHTransfer-Start |
Affected Domain Objects | |
Affected Tables | |
Stored Procedure | |
Default State | Disabled |
Is Site Specific | False |
Edit State | Globally Enabled |
Live State | Globally Enabled |
Description | Transfers the reporting repository to the Customer Information Center. |
Scheduling | |
What Happens Switched Off | |
Trouble Shooting | CIC does not get any data for the analyzation. |
Comments | This is only the transfer - the data collection is handled by the other REPORT_* jobs. See also |

Product Version | 7.0 |
|---|---|
Product To Version | |
| Status |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.