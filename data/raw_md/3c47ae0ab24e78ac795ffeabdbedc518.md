---
id: '3c47ae0ab24e78ac795ffeabdbedc518'
title: 'ISML Tag'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2473A0'
scraped_at: '2026-04-21T05:41:12.164592+00:00'
---
`<ISPLACEMENT>`

is used to mark content within an ISML template that will be aggregated and moved to the according `<ISPLACEHOLDER>`

spots by the Web Adapter post-processing.

<ISPLACEMENT placeholderid = "( <String> | <ISML expression> )" > <String, HTML, ISML subset> </ISPLACEMENT>

Note

As ISML subset within <ISPLACEMENT>, the following ISML tags are allowed exclusively:

`<isprint>`

, `<isif>`

, `<isset>`

, `<isloop>`

, `<isnext>`

and `<isbreak>`

.

Use the `<ISPLACEMENT>`

tag to define a CSS reference that will be aggregated at the matching `<ISPLACEHOLDER>`

tag.

<ISPLACEMENT placeholderid="CSS"> <link rel="stylesheet" type="text/css" href="/css/shop.css" /> </ISPLACEMENT> <ISPLACEMENT placeholderid="CSS"> <link rel="stylesheet" type="text/css" href="/css/slider.css" /> </ISPLACEMENT>

Use the <ISPLACEMENT> tag to define content for the meta tag for keywords that will

be aggregated at the matching <ISPLACEHOLDER> tag.

<ISPLACEMENT name="keywords">Shirts</ISPLACEMENT> <ISPLACEMENT name="keywords"> <isprint value="#Product:Name#"> </ISPLACEMENT>

`placeholderid`

`placeholderid = string | ISML expression`


Specifies the ID of the placeholder this entry belongs to. The Web Adapters post-processing will insert the aggregated content of all `<ISPLACEMENT>`

tags with that placeholderid at the matching `<ISPLACEHOLDER>`

spot.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.