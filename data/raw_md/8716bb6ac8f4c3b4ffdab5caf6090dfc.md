---
id: '8716bb6ac8f4c3b4ffdab5caf6090dfc'
title: 'ISML Custom Tag'
url: 'https://knowledge.intershop.com/kb/index.php/Display/27759N'
scraped_at: '2026-04-21T05:41:28.683234+00:00'
---
Pagelets derived from a pagelet definition with the page flag set to `false`

(component), can be rendered directly by using the `<ISPAGELETASSIGNMENT>`

tag if one has a pagelet assignment instead of a pagelet.

Note

**Intershop Commerce Suite 7.7 required!**

To use the ISML Custom Tag <ISPAGELETASSIGNMENT> Intershop Commerce Suite 7.7 or later is required.

This custom tag provides similar functionality as [ISML Custom Tag - ISPAGELET](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1775690232/ISML+Custom+Tag+-+ISPAGELET). But while <ISPAGELET> directly renders the given pagelet, `<ISPAGELETASSIGNMENT>`

takes the pagelet from the given pagelet assignment. Rendering with `<ISPAGELETASSIGNMENT>`

will provide additional editing information for the Design View, e.g., Drag-And-Drop handles for the assignments positioning. Also the determination whether a pagelet assignment is directly to a slot or to a placeholder is only possible if a pagelet assignment is used instead of the pagelet.

Starting with Intershop 7.7 the [ISML Custom Tag - ISSLOTITERATOR](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1775690292/ISML+Custom+Tag+-+ISSLOTITERATOR) provides additional functionality that can return pagelet assignments instead of pagelets. This can then be used as input for `<ISPAGELETASSIGNMENT>`

.

<ispageletassignment ( PageletAssignment = "( {ISML expression} )" )>

The call parameters as required by the definition of the pagelet are mapped automatically from the currently active dictionary of the environment in which the module is embedded to the execution environment of the module. The render

template of the pagelet is either included locally, when the flag `remoteInclude`

of the pagelet definition is set to `false`

, or as Web Adapter include, when the flag is set to `true`

.

<iscontent type="text/html" charset="UTF-8" compact="true"> <isif condition="#isDefined(SlotPageletAssignment)#"> <ispageletassignment PageletAssignment="#SlotPageletAssignment#"> </isif>

`<`

is a strict module and has only one parameter, `ISPAGELETASSIGNMENT`

>`PageletAssignment`

.

`PageletAssignment`

The pagelet assignment whose assigned pagelet should be rendered.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.