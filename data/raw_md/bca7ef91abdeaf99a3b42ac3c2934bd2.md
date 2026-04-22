---
id: 'bca7ef91abdeaf99a3b42ac3c2934bd2'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2P3573'
scraped_at: '2026-04-21T05:39:45.169448+00:00'
---
This concept describes business object replication. Business object replication is intended for quick and easy transfer of business objects from the editing system to one or more live systems (see [Usage](https://knowledge.intershop.com#Concept-BusinessObjectReplication-Usage)).

For the transfer of large amounts of data, [mass data replication](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1760888496/Concept+-+Mass+Data+Replication+valid+to+11) has to be used.

Business object replication works by creating transfer entities called "WebObjects" from business objects by the use of configurable WebObject *Providers* and transferring those WebObjects to the target system(s) via a SOAP WebService. On the target system(s), the objects are validated and merged into the target system's data (see [Background](https://knowledge.intershop.com#Concept-BusinessObjectReplication-Background)).

Business object replication is more commonly called "object replication" and may also be referred to as "partial replication".

Term | Description |
|---|---|
WebObject | the transfer entity containing all necessary information on the business object |
WebObject Provider | or |
Publish | Term used for object replication_ in the user interface |
Referenced Object | An object that is referenced by the replicated business object, but can exist independently |
Dependent Object | An object that belongs to the replicated business object, and cannot exist independently |
Dependent File | A file that belongs to a replicated business object |

Object replication is only available on systems that are marked as editing systems in a staging environment (see the administrator handbook of your Intershop 7 distribution).

A user will see the business object replication interface elements on listings and detail pages of supported business objects.

On a business object's detail view, the object can be replicated using the button Publish to Live System. After selecting a target cluster on the next page, a batch process will be created performing the actual replication.

In a listing, one or more objects can be selected and replicated using the button Publish to Live System. The listing also includes a column Published, listing the date(s) and time(s) of the last successful object replication(s) to the target system(s).

After starting the replication, the user is taken to the batch process overview page.

Note

Object replication can only **update** and **create** objects, not delete them.

Information for developers (e.g. on adding object replication support to additional business objects) can be found in the [Cookbook - Business Object Replication](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1773261291/Cookbook+-+Business+Object+Replication).

`WebObjectProvider`

( `WOProvider`

) is looked up that does the collecting of dependent objects and transforms it. This procedure is repeated for each dependent object too.`SearchWordProvider`

is used (if existent) to determine significant search words for invalidation of the page cache. The search words will only be invalidated on affected sites (because only sites have a page cache and not all sites display the affected object). For instance, if one of the ORMObjects is a product, files of the page cache that contain the UUID, SKU or name of the ProductPO are filed for invalidation for each site that displays the product.`ADProvider`

(if existent), affected domains for ORMObjects are determined. For instance, the affected domains for a product are the domain that owns the product and the domains the product is shared to.`LastPublishDate`

is written for each object. In this way, the user can see when the object was replicated (e.g. seen in Promotions).The following diagram shows the process for an example object `Sample`

with two referenced objects, `Other`

and `Another`

:

**(1)** When the publishing of a `Sample`

is started, the replication framework first resolves all references of the `Sample`

by means of the `SampleRefOOProvider`

(if there is one defined). This results in a `Set<Object>`

containing all referenced sample objects as well as the sample object itself. From the `Set`

an `Iterator`

is created within which, according to the `PublishOrder`

defined in `SampleRefOOProvider`

, the `Sample`

is the first/last element.

Now the elements of the iterator are replicated one by one in chunks of default size 15 where for each object the corresponding `<object_type>WOProvider`

is used.

**(2)** WebObjects for the referenced objects are created using the `ReferencedOtherWOProvider`

and the `ReferencedAnotherWOProvider`

, respectively.

**(3)** WebObjects for `Sample`

and its attributes are created by means of the `SampleWOProvider`

.

**(4)** The WebObjects are transferred to the live system.

**(5)** When receiving the objects, the `validate`

method of the matching providers will be called, where the referenced objects of `Sample`

are validated and merged before the `Sample`

web object itself. The validation itself depends on (i.e. is implemented in) the `WOProvider`

. The provider can also perform some actions depending on the outcome of the validation. If the validation fails, an error will be logged.

**(6)** Whenever the validation of a web object succeeds, the `merge`

method of the matching provider is called. This method is responsible for creating/updating business objects in the live system to match the transferred object.

For each ORMObject a SearchWordProvider is used (if existent) to determine significant SearchWords for invalidation of the PageCache.

The SearchWords will only be invalidated on affected sites (because only sites have a PageCache and not all sites display the affected object).

For example, if one of the ORMObjects is a product, files of the PageCache that contain the UUID, SKU or name of the ProductPO are filed for invalidation for each site that displays the product.

Using the specific `ADProvider`

(if existent), affected domains for ORMObjects are determined.

For instance, the affected domains for a product are the domain that owns the product and the domains the product is shared to.

Description | ORMObject | WoProvider | Published in 7.0 | Published in 7.1 |
|---|---|---|---|---|
Campaign and attribute values |
|
| ||
TargetGroup |
|
| ||
TargetGroup : UserGroupRoleAssignment |
|
| ||
TargetGroup : UserGroupInformation |
|
| ||
TargetGroup : UserGroup assignments |
|
| ||
UserGroupAssignment from campaign (childUserGroup) to all assigned promotions (parentUserGroup) |
|
| ||
UserGroupAssignment for all assigned Pagelets |
|
| ||
Referenced Pagelets |
| |||
Referenced Promotions |
|

The current campaign publishing is organized in such a way that promotions and pagelets assigned to a campaign are published before the campaign is published. So, if the final live side validation of the campaign fails, then the campaign itself is not published, whereas assigned promotions and pagelets at that moment are already updated. This requires post-processing for each assigned promotion and pagelet:

`UseCampaignTargetGroup`

flag to `false`

and disable the promotion. This procedure is complete because as soon as the promotion is published by means of the `ReferencedPromotionWOProvider`

, its `campaignUUID`

attribute is set to `null`

in order to avoid the situation of the referenced promotion being assigned to another - no longer supported - campaign on live side. Now, if the campaign to be published does already exist in the live system, then two cases have to be distinguished:`UseCampaignTargetGroup`

flag is `true`

and if the current campaign target group is no direct child of the promotion target group, make the current campaign's target group a direct child of the promotion's target group again.`UseCampaignTargetGroup`

flag is `false`

and if the current campaign's target group is a direct child of the promotion's target group, remove this direct child relation.`CAMPAIGN_`

/ `Promotion_`

. A pagelet that has no user group assignment must not be displayed in the storefront.Now assume that the campaign validation is successful. If the campaign did not exist in the live system before, then the assigned and published content is fine. Otherwise there may be a difference between former and new assigned pagelets that has to be dealt with. This is done as follows:

The promotion post-processing in case of successful campaign validation is straightforward: No longer valid assignments to other campaigns are removed and the new assignment to the campaign to be published is confirmed.

Description | ORMObject | WoProvider | Published in 7.0 | Published in 7.1 |
|---|---|---|---|---|
Pagelet |
|
| ||
Parent Pagelet (not published for pagelets referenced by promotions or campaigns) |
|
| ||
Slots |
|
| ||
Placeholders |
|
| ||
Placeholder definitions |
|
| ||
Pagelet user group assignments |
|
| ||
Assignments from pagelet to slot |
|
| ||
Pagelet ABTestGroup assignments |
|
| ||
Pagelet Promotion assignments |
|
|

Description | ORMObject | WOProvider | Published in 7.0 | Published in 7.1 |
|---|---|---|---|---|
Promotion and attribute values |
|
| ||
TargetGroup(s) |
|
| ||
TargetGroup : UserGroupRoleAssignment |
|
| ||
TargetGroup : UserGroupInformation |
|
| ||
TargetGroup : UserGroup assignments |
|
| ||
PromotionAttachments | Parameter |
| ||
Rebates |
|
| ||
Rebate: Condition "tree" |
|
| ||
Rebate: Actions |
|
| ||
Rebate: RebateFilterGroup assignments |
|
| ||
Rebate: RebateFilterGroups |
|
| ||
Rebate: RebateFilterGroups: assignment to RebateFilterObjects (catalogs or products) |
|
| ||
Budget |
|
| ||
Budget Periods |
|
| ||
Budget Account |
|
| ||
Promotion Application assignments |
|
| ||
PromotionCodeGroup assignments |
|
| ||
PageletAssignments |
|
| ||
PageletUserGroupAssignments |
|
| ||
Referenced Pagelets |
| |||
Referenced PromotionCodeGroups |
| |||
PromotionCodeGroup (for partial replication allowed size is configurable) |
|
| ||
PromotionCodeGroup: Applications |
|
| ||
PromotionCodeGroup: UserGroup/Affiliate assignments and redemption configuration |
|
|

In analogy to campaign publishing, the current promotion publishing is organized in such a way that pagelets assigned to a promotion are published before the promotion is published. So, if the final live side validation of the promotion fails, then the promotion itself is not published whereas assigned pagelets at that moment are already in the state "published". This requires a post-processing for each assigned pagelet which is done in the same way as for pagelets assigned to a campaign in the case of campaign validation failure.

The pagelet post-processing in case of successful promotion validation is the same as in case of successful campaign validation.

Business object replication is not meant for mass data. For replicating mass data, staging is used which copies content from the editing-database-scheme to the live-system database-scheme.

The replication is done by sending and receiving serialized objects via web services. If a huge object (with several megabytes) is sent, the web services could massively slow down.

If the user plans to replicate a lot of objects (e.g. 10000 products), these objects will be sent in several loops, 15 objects each loop (this value can be set by *staging.objects.chunksize* in *<enfinity>/share/system/config/cluster/staging.properties*) and the cache refresh is started when all objects have been sent and merged.

Remember that business object replication is only meant for emergency updates of a few objects.

If you want to replicate a lot of data, use the Mass Data Tasks menu.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.