---
id: 'fa65cfd6f694d5dcfa9cc4994eeafe5f'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2854Q3'
scraped_at: '2026-04-21T05:40:56.599134+00:00'
---
In previous ICM versions, the email addresses of sender and receiver for quote notifications were hard-coded in the pipeline `ProcessQuoteRequestNotifications`

(*app_sf_responsive_b2b*).

The pipeline `ProcessQuoteNotificationsExtension`

also used the *from* email address which is now fixed. Now the email addresses can be configured in a common way.

The email addresses can be configured in a common way by using the following application preferences:

`QuoteNotificationEmailFrom`

`QuoteNotificationEmailTo`

The default value for the preference definition can be configured via DBInit in the properties file *com.intershop.application.responsive.webshop.b2b.dbinit.data.preference.PreferenceDefinitions.properties* (cartridge: *app_sf_responsive_b2b*).

# # Quote Notification Preferences # QuoteNotificationEmailFrom=ChannelPreferences;3;;true;info@test.intershop.de;false QuoteNotificationEmailTo=ChannelPreferences;3;;true;info@test.intershop.de;false

The values can also be configured per channel via domain preferences.

[IS-22126](https://knowledge.intershop.com/kb/go.php/o/38344) - Wrong MailFrom ParameterBinding in ProcessQuoteNotificationsExtension.pipeline

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.