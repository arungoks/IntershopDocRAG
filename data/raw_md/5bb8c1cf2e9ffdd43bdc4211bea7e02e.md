---
id: '5bb8c1cf2e9ffdd43bdc4211bea7e02e'
title: 'ISML Function'
url: 'https://knowledge.intershop.com/kb/index.php/Display/247U81'
scraped_at: '2026-04-21T05:41:23.151023+00:00'
---
The ISML function `hasNext()`

allows you to check whether the iterator instance currently used in a loop contains any elements. This is useful, for example, in case the last loop element requires special treatment.

hasNext( <loop iterator identifier> )

<ISLOOP iterator="foo"> ... <ISIF condition="#hasNext(foo)#"> ... (do something except for last line) </ISIF> ... </ISLOOP>

Note

If an alias name has been defined for the iterator, this alias has to be used for `hasNext()`

as well.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.