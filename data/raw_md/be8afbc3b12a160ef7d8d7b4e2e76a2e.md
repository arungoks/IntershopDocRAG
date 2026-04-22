---
id: 'be8afbc3b12a160ef7d8d7b4e2e76a2e'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2V9875'
scraped_at: '2026-04-21T05:37:11.256404+00:00'
---
Some features that were marked as deprecated in older versions of Intershop Commerce Management have been removed in this release. These are mainly methods that are part of the CMS and have been deprecated since at least 7.4.

If there are any compile errors with customizations after migrating to 7.10.32, the replacements should be listed here.

Target Group: Customers / partners who migrate from **7.8 or lower to 7.10.32+**

| Deprecated Method | Deprecated since | Replacement |
|---|---|---|
`Iterator getSlotSubPageletAssignments(Domain domain)` | 7.0 | `getPageletAssignments(Domain domain)` |
`Iterator getSortedSlotSubPageletAssignments(Domain domain)` | 7.0 |
|
` Iterator getSortedSlotSubPageletAssignments()` | 7.0 |
|
`Iterator getSubPagelets(Domain domain, Boolean staticContext)` | 7.0 | `getPagelets(Domain domain).iterator()` |
`Iterator getSubPagelets(Date date, Boolean staticContext)` | 7.0 |
|
`Iterator getSubPagelets(Date date, Domain domain, Boolean staticContext)` | 7.0 | `getPagelets(Date date, Domain domain)` |
`Iterator getSubPagelets(Boolean staticContext)` | 7.0 | `getPagelets()` |
`boolean isHidden(Domain domain)` | 7.8 | Replaced by Overriding Placeholder Concept |
`void setHidden(boolean hiddenFlag, Domain domain)` | 7.8 | Replaced by Overriding Placeholder Concept |
`void setReadOnly(boolean readOnlyFlag, Domain domain)` | 7.8 | Replaced by Overriding Placeholder Concept |
`boolean isReadOnly(Domain domain)` | 7.8 | Replaced by Overriding Placeholder Concept |
`boolean isHideable()` | 7.8 | Replaced by Overriding Placeholder Concept |
`void setHideable(boolean aFlag)` | 7.8 | Replaced by Overriding Placeholder Concept |

| Deprecated Method | Deprecated since | Replacement |
|---|---|---|
`void disableSorting()` | 7.0 | No replacement, since the functionality is removed since 7.0 |
`void enableSorting()` | 7.0 | No replacement, since the functionality is removed since 7.0 |
`boolean isSortingEnabled()` | 7.0 | No replacement, since the functionality is removed since 7.0 |

| Deprecated Method | Deprecated since | Replacement |
|---|---|---|
`boolean hasParent(Domain domain)` | 7.2 | `boolean hasParent(Domain domain, PageletModelRepository pmr)` |
`PageletEntryPoint getParentPageletEntryPoint(Domain domain)` | 7.2 | `PageletEntryPoint getParentPageletEntryPoint(Domain domain, PageletModelRepository pmr)` |
`boolean hasSubPageletEntryPoints(Domain domain)` | 7.2 | `boolean hasSubPageletEntryPoints(Domain domain, PageletModelRepository pmr)` |
`Collection getSubPageletEntryPoints(Domain domain)` | 7.2 | `Collection getSubPageletEntryPoints(Domain domain, PageletModelRepository pmr)` |

| Deprecated Method | Deprecated since | Replacement |
|---|---|---|
| 7.2 | getTo |
| 7.2 | getFrom or getPagelet |

| Deprecated Method | Deprecated since | Replacement |
|---|---|---|
`ContextObjectRelation getContextObjectRelation()` | 7.2 | `getModelElement().getContextObjectRelation()` |

`UpdateSlotVisibility`

was removed without replacement.`onEdit`

is no longer a property of the `PageletDefinition`

, since this functionality was not used since 7.4The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.