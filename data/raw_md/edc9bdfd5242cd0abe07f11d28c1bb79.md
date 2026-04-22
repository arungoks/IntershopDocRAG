---
id: 'edc9bdfd5242cd0abe07f11d28c1bb79'
title: 'Announcement - Solr 4'
url: 'https://knowledge.intershop.com/kb/index.php/Display/29Y888'
scraped_at: '2026-04-21T05:39:46.551363+00:00'
---
The Intershop Commerce Management (ICM) 7.10.31.0 release contains a Tomcat 9 update that affects all projects migrating to this version. In particular, it affects projects still using Solr 4, which is supported by Intershop only until the end of the year (see [Announcement - End of Maintenance of Solr 4](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930407436/Announcement+-+End+of+Maintenance+of+Solr+4)).

Currently, Solr 4 in ICM is running on its own Tomcat 7. However, this "inner Tomcat" is removed with the Tomcat 9 update in ICM 7.10.31. In order to have a functioning Solr, project adaptions are necessary and a compatible ICM version must be used for the migration.

In case your project is still using Solr 4 and you are planning an ICM migration in the near future, this document shows your options. If your project already uses SolrCloud 8, you can stop reading here.

**Note: SolrCloud 6**

Intershop provides an adapter to use SolrCloud 6. Even though SolrCloud 6 is already a "cloud version", the corresponding adapter would require a new release to be compatible with the Tomcat 9 update.

Since this adapter has already reached the "end-of-life" status in 2020, *there will be no new release* for this adapter anymore.

Consequently this means, if your project is using SolrCloud 6, the following two options apply to you as well!

If you are planning an ICM update to ICM 7.10.31+, we recommend updating the search service as well.

For Intershop Commerce Platform (previously known as CaaS) customers, Intershop provides the necessary SolrCloud 8 cluster.

If you choose this option, you can migrate to any ICM 7.10.31+ version.

The following steps have to be performed:

A combined update of SolrCloud and ICM provides you with a future-proof solution that is also compatible with future ICM updates after 7.10.31.

However, the Solr migration will cause an additional effort.

These are the advantages of doing the update during the ICM migration:

For further information, refer to: [Announcement - End of Maintenance of Solr 4](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1930407436/Announcement+-+End+of+Maintenance+of+Solr+4)

This might be considered as a disadvantage:

If you want to stay on a current version, get critical bug fixes, but continue to use Solr4, you can migrate to ICM 7.10.26-LTS. The Long Term Support (LTS) release gets hotfixes until the end of December 2021, so you have more time for the SolrCloud 8 migration.

The following steps need to be done:

This solution gives you more time for SolrCloud migration. However, SolrCloud migration is only postponed and becomes mandatory when you want to update to a future LTS version (e.g. 7.10.32-LTS).

This is the advantages of staying on the LTS releases:

This should be considered :

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.