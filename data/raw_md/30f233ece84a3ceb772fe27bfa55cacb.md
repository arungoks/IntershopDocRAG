---
id: '30f233ece84a3ceb772fe27bfa55cacb'
title: 'Server Groups'
url: 'https://knowledge.intershop.com/kb/index.php/Display/K33661'
scraped_at: '2026-04-21T05:31:03.590220+00:00'
---
# Server Groups

In an Intershop Commerce Management deployment with multiple application servers, you can assign a single application server to a certain server group, in a default installation, for example, `WFS`

for Web front requests or `BOS`

for back end requests.

To distribute requests to the Web front applications, Intershop Organization Management allows for associating single sites to a specific server group.

To assign an application to a specific server group:

-
In the navigation bar, select Site Management.
A list of available sites is displayed.
-
Click the name of the site you intend to edit.
The Site Settings page is displayed.
-
Specify a server group in the corresponding field.
Note:Make sure the server group is defined in the Web Adapter properties, and at least one application server is assigned to this server group.
- Click Apply to save your settings. Otherwise, click Reset to discard your changes.

For information about configuring server groups in the Web Adapter and for information about assigning application servers to server groups, refer to [Guide - Web Adapter Settings](https://knowledge.intershop.com/kb/index.php/Display/27984R) in the Intershop Knowledge Base.