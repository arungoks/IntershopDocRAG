---
id: '27edc1ba76424cbf3c7cb9e9fec1fb99'
title: 'Job'
url: 'https://knowledge.intershop.com/kb/index.php/Display/294T81'
scraped_at: '2026-04-21T05:36:31.487259+00:00'
---
Name | Disable Inactive Users |
|---|---|
Domain | SLDSystem |
Job Dependencies | none |
AcquiredResources | none |
Cartridge | sld_system_app |
Pipeline | DisableInactiveUsersJob-Start |
Affected Domain Objects | User |
Affected Tables | basiccredentials |
Stored Procedure | |
Default State | Enabled |
Is Site Specific | False |
Edit State | Globally Enabled |
Live State | Globally Enabled |
Description | Disables back office users that have not logged in for a longer time. E-mails are sent before they are actually disabled. |
Scheduling | It is suggested to run at least once per day. Preferred stating time is when the site usage is slow, usually at night. |
What Happens Switched Off | Inactive back office users are not disabled. |
Trouble Shooting | The execution of this job will alter the field {code Optional it could be narrow by some credentials parameters. {code update basiccredentials set disabledflag = 0 where lastloggedin < :date; |
Comments | This is job is required for PA-DSS/PCI-DSS compliance. It disables back office users which have not logged in for a given time frame. By default, this time is set to 0 days, which means that no users will be disabled (Preference: InactivityPeriod). |

Product Version | 7.0 |
|---|---|
Product To Version | |
| Status |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.