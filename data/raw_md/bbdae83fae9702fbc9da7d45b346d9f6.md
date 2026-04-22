---
id: 'bbdae83fae9702fbc9da7d45b346d9f6'
title: 'Support Article'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2S9383'
scraped_at: '2026-04-21T05:35:51.370005+00:00'
---
Starting with Google Chrome 80, no third-party cookie will be sent to another page if the cookie does not have the `SameSite`

flag. Usually, this is not an issue for Intershop 7, but there are two special cases that are affected by the Chrome policy: Punchout and some payment methods.

In the following article `SameSite=None`

is used to solve issues. However, using `None`

is only an example. Please rather use `Strict`

or `Lax`

instead to avoid completely disabling the `SameSite`

security feature.

Intershop 7 has an OCI Punchout feature in the B2B storefront. When changing to the external system, an HTML frame and the SID cookie are used to track the Intershop session.

This usually works well. However, with the new Chrome 80 change, cookies such as the SID cookie are not transferred to the external site. This means that the Intershop session is lost and Punchout does no longer work.

To pass the SID cookie to the external system, a `SameSite=None`

attribute must be added. Additionally, the same cookie must be set to `Secure`

.

It is easily possible to set the cookie attributes in the global *webadapter.properties* (in *$IS_Share/system/config/cluster*). The property `session.SIDCookie`

must be adapted, for example:

session.SIDCookie=Set-Cookie: sid=%v; Path=/; Version=1; HttpOnly; SameSite=None; Secure

A restart is not necessary, Punchout within a frame now works as before Chrome 80.

Please note the remarks below.

The same behavior occurs along with some payment providers when using *Redirect before/after Checkout. *Usually, it is enough to do the same configuration change as above, setting the *SameSite* attribute and the *Secure* flag:

session.SIDCookie=Set-Cookie: sid=%v; Path=/; Version=1; HttpOnly; SameSite=None; Secure

It might be possible that different payment providers need to set additional cookies with the `SameSite`

attribute. In this case Apaches *mod_header* can be used, example:

Header edit Set-Cookie ^(SecureSessionID.*)$ $1;SameSite=None;Secure

or for ICM versions starting with 7.10.38.15:

Header edit Set-Cookie ^(__Host-SecureSessionID.*)$ $1;SameSite=None;Secure

In this example the SecureSessionID cookie is also set accordingly.

Later Intershop versions will be able to set the cookie attributes for other cookies individually as well.

Please see the remarks below.

As already mentioned, in addition to the SameSite attribute, the Secure flag must also be set for the SID. This results in a major implication: The SID cookie is only transferred from the browser back to the Intershop application if the connection is secured via https.

If this is not the case, the session and all session-related information such as login status or shopping cart are lost. This means that when using Punchout or some payment providers, the entire store must be secured with https.

When using Punchout and the Intershop storefront is displayed in a frame, the default cookie test might fail and a message like the following might be displayed:*It appears that your browser has cookies disabled.*

* *In this case, the test cookie must also be set to

`SameSite=None; Secure`

in the template:Therefore, change the following line:

document.cookie = name + '=;';

to:

if(location.protocol == 'https:') { document.cookie = name + '=; Secure; SameSite=None;'; } else { document.cookie = name + '=;'; }

There are browsers that do not handle the `SameSite`

attribute correctly. In particular, Safari on iOS 12 or Mac OS 10.14 treats `SameSite=none`

as `SameSite=strict`

, which has the opposite meaning. So, setting `SameSite=none`

results in a working Punchout resp. payment process for all browsers except these Safari versions. For more information, refer to: [https://itnext.io/user-agent-sniffing-only-way-to-deal-with-upcoming-samesite-cookie-changes-6f79a18e541](https://itnext.io/user-agent-sniffing-only-way-to-deal-with-upcoming-samesite-cookie-changes-6f79a18e541).

The solution would be not to set `SameSite=none`

for those Safari versions. Here is an example of an Apache configuration that sets the `SameSite=none`

only for the unaffected versions:

<If "%{HTTP_USER_AGENT} !~ /(iPhone; CPU iPhone OS 1[0-3]|iPad; CPU OS 1[0-3]|iPod touch; CPU iPhone OS 1[0-3]|Macintosh; Intel Mac OS X.*Version\x2F1[0-3].*Safari|Macintosh;.*Mac OS X 10_14.* AppleWebKit.*Version\x2F1[0-3].*Safari)/i"> Header edit Set-Cookie ^(.*)$ $1;SameSite=None;Secure </If>

More information about compatibilities can be found here:

[https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite#browser_compatibility](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite#browser_compatibility)

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.