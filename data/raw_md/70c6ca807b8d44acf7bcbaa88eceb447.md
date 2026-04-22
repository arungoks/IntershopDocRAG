---
id: '70c6ca807b8d44acf7bcbaa88eceb447'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/28164T'
scraped_at: '2026-04-21T05:37:31.441721+00:00'
---
This document discusses steps to migrate an Intershop storefront that is not yet based on the Responsive Starter Store (introduced with Intershop 7.6) to a storefront based on the Responsive Starter Store. These are manual migration steps and there cannot be an automated process for this.

While the [Guide - 7.6 Migration to Responsive Starter Store](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1812646147/Guide+-+7.6+Migration+to+Responsive+Starter+Store) describes the migration steps that are necessary to migrate an Intershop 7.5 PrimeTech based storefront to the Responsive Starter Store in a more specific way, this guide is intended to describe the more general steps, which are necessary to migrate to the Responsive Starter Store from a base that is - concerning the content model and the storefront functionality and source code - not as close as the Intershop 7.5 PrimeTech storefront.

Migration in the context of this document means, what needs to be done to get a Responsive Starter Store storefront running on top of an updated customer project that was migrated to a current Intershop version. This does not mean that the customer's customized storefront is fully migrated to a customized version of the Responsive Starter Store.

`"ant export"`

).[Remove the custom storefront cartridges / storefront content.](https://knowledge.intershop.com#Guide-MigrationtotheResponsiveStarterStore-RemovetheCustomStorefrontCartridges)

[Adapt the migrated content to the new Responsive Starter Store's styling and structure.](https://knowledge.intershop.com#Guide-MigrationtotheResponsiveStarterStore-FittheMigratedContenttotheNewResponsiveStarterStoreStylingandStructure)

Since it is not possible to migrate the CMS content of older or highly customized content models automatically to the content of the Responsive Starter Store, it is necessary to export the current content. So it can be at least partially migrated and re-imported later on.

For that reason:

Export all CMS content of all organizations, channels and applications, preferably as ZIP export.

The exports can be done in the Intershop Commerce Management application. The ZIPs need to be downloaded from the server and saved for further processing.

The content of these ZIP files will than be the base for manual transformations and might be partially re-imported into the new Responsive Starter Store content.

The older CMS content is not compatible to the content model of the Responsive Starter Store. Thus it is best to completely remove the old content from the database. Use the white-label store content of the Responsive Starter Store and develop your content model from scratch. Parts of the older CMS content might be migrated and imported afterwards. For that we have the ImpEx files of the [backup](https://knowledge.intershop.com#Guide-MigrationtotheResponsiveStarterStore-ExportBackup) before.

The Intershop Commerce Management already provides procedures the can be used to completely delete the CMS content for a given domain.

set echo on set verify on define dn = &1 begin sp_deleteMarketingPAByDomain(domainid('&dn')); sp_deletePEPAByDomain(domainid('&dn')); sp_deletePageletsByDomain(domainid('&dn')); end; / commit; exit

The attached [remove_content.sql](https://knowledge.intershop.com/kb/index.php/Deliver/DOC/28164T/remove-content.sql) can be used together with a command line script to remove all CMS content data from the database.

sqlplus USER/PASSWORD@ISSERVER.world @remove_content.sql inSPIRED-inTRONICS-b2c-responsive

Note

This procedure needs to be repeated for each domain that contains CMS content.

After removing the old storefront content the storefront can later be reinitialized with the white-label store content of the Responsive Starter Store.

Alternative way of removing your old CMS content from the database

In case removing the CMS content via stored procedures is not the way to go, there is an alternative way of getting rid of the old, invalid content from the database This step fits best after migrating the project data and before initializing your storefront with the Responsive Starter Store white-label store content. This step is necessary before migrating the exported and downloaded content to get rid of the existing content in the database that will be invalid due to changes to the content model. Intershop no longer uses the old *app_sf_webshop* or *sld_ch_b2c_app* content model. The server will only know the* app_sf_responsive* content model instead.

To remove any invalid CMS content instances Intershop provides the job *Synchronize Page Model and Pagelet Instances* in the SLDSystem domain that can be executed from the SMC.

Running this job completely removes all the instances that no longer match to any content model definition. In the present case it would completely remove the old, obsolete CMS instances from the database.

With the introduction of the Responsive Starter Store there have been several changes on how to set up a customer project. This procedure is described in detail in the [Recipe: Set Up Project based on the Responsive Starter Store](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1822571078/Cookbook+-+Setup+CI+Infrastructure#Cookbook-SetupCIInfrastructure-ResponsiveStarterStore). For migration across multiple versions it is probably best to:

Set up your project by starting with a clean Responsive Starter Store.

Note

It is necessary to follow the mentioned recipe to set up your project. While doing this one needs to remove the not needed parts of the Responsive Starter Store, e.g., the B2X cartridges if you are only interested in a B2C shop and especially for a migration project the demo initialization cartridges.

One important step for a migration project is the adaption of the application type. Projects that are based on Intershop prior to version 7.6 usually use the storefront application type `intershop.B2CWebShop`

while the Responsive Starter Store application type is` intershop.B2CResponsive.`

For a migration scenario from an `intershop.B2CWebShop`

storefront to the Responsive Starter Store storefront it is not feasible to use the application types of the Responsive Starter Store (`intershop.B2CResponsive,intershop.SMBResponsive`

) defined in *as_responsive*. Instead, the application types (`intershop.B2CWebShop`

,` intershop.SMBWebShop`

) of the existing project need to be kept. There is no easy way to migrate the application types of existing application instances and its representation in the shared file system. It is much easier to:

Change the application type ID of the Responsive Starter Stores storefront application type definition.

This is done in the *apps.component* file of the *as_responsive* cartridge.

<components xmlns="http://www.intershop.de/component/2010"> <!-- ************************************************************************************ --> <!-- * Application Type "intershop.B2CResponsive" * --> <!-- ************************************************************************************ --> <instance name="intershop.B2CResponsive.Cartridges" with="CartridgeListProvider"> <fulfill requirement="selectedCartridge" value="app_sf_responsive_b2c"/> <fulfill requirement="selectedCartridge" value="app_sf_responsive_cm"/> ... <fulfill requirement="subProvider" with="intershop.DemoCartridges" /> </instance> <instance name="intershop.B2CResponsive" with="ApplicationType"> <fulfill requirement="id" value="intershop.B2CResponsive"/> <fulfill requirement="urlIdentifier" value="b2c-responsive"/> <fulfill requirement="cartridgeListProvider" with="intershop.B2CResponsive.Cartridges"/> ... </instance> ... <!-- ************************************************************************************ --> <!-- * Application Type "intershop.SMBResponsive" * --> <!-- ************************************************************************************ --> <instance name="intershop.SMBResponsive.Cartridges" with="CartridgeListProvider"> <fulfill requirement="selectedCartridge" value="app_sf_responsive_smb"/> <fulfill requirement="selectedCartridge" value="app_sf_responsive_cm"/> ... <fulfill requirement="subProvider" with="intershop.DemoCartridges" /> </instance> <instance name="intershop.SMBResponsive" with="ApplicationType"> <fulfill requirement="id" value="intershop.SMBResponsive" /> <fulfill requirement="urlIdentifier" value="smb-responsive" /> <fulfill requirement="cartridgeListProvider" with="intershop.SMBResponsive.Cartridges" /> ... </instance> ... </components>

In the *apps.component* file the following changes would be necessary:

| original naming | changed naming |
|---|---|
`B2CResponsive` | `B2CWebShop` |
`b2c-responsive` | `b2c-web-shop` |
`SMBResponsive` | `SMBWebShop` |
`smb-responsive` | `smb-web-shop` |

Additional application type definition files like *apps-extension.component* of *as_responsive_b2b* need to be changed too if they are used (in a B2B storefront).

Please consider there might be additional files like this due to the customization of your project.

<components xmlns="http://www.intershop.de/component/2010"> <!-- ************************************************************************************ --> <!-- * Application Type "intershop.B2CWebShop" * --> <!-- ************************************************************************************ --> <instance name="intershop.B2CWebShop.Cartridges" with="CartridgeListProvider"> <fulfill requirement="selectedCartridge" value="app_sf_responsive_b2c"/> <fulfill requirement="selectedCartridge" value="app_sf_responsive_cm"/> ... <fulfill requirement="subProvider" with="intershop.DemoCartridges" /> </instance> <instance name="intershop.B2CWebShop" with="ApplicationType"> <fulfill requirement="id" value="intershop.B2CWebShop"/> <fulfill requirement="urlIdentifier" value="b2c-web-shop"/> <fulfill requirement="cartridgeListProvider" with="intershop.B2CWebShop.Cartridges"/> ... </instance> ... <!-- ************************************************************************************ --> <!-- * Application Type "intershop.SMBWebShop" * --> <!-- ************************************************************************************ --> <instance name="intershop.SMBWebShop.Cartridges" with="CartridgeListProvider"> <fulfill requirement="selectedCartridge" value="app_sf_responsive_smb"/> <fulfill requirement="selectedCartridge" value="app_sf_responsive_cm"/> ... <fulfill requirement="subProvider" with="intershop.DemoCartridges" /> </instance> <instance name="intershop.SMBWebShop" with="ApplicationType"> <fulfill requirement="id" value="intershop.SMBWebShop" /> <fulfill requirement="urlIdentifier" value="smb-web-shop" /> <fulfill requirement="cartridgeListProvider" with="intershop.SMBWebShop.Cartridges" /> ... </instance> ... </components>

Note

Be aware that the changes to the apps*.component files need to be kept for future migrations.

After this step we have a project set up with the standard Responsive Starter Store that fits to the application type that was used in the original project.

Remove all Storefront Customization Cartridges from the Project Sources

Since the standard installation of Intershop does not contain the storefront cartridges anymore it is necessary to remove all custom storefront cartridges that where developed for demo shops that were introduced before the Responsive Starter Store and thus depend on the previous Intershop storefront cartridges that are no longer installed by default. Such custom storefront cartridges are probably not compatible with the changes made to the current version of the Responsive Starter Store anyways.

A manual migration of the contained custom features should be done later on considering what custom features are still needed. Intershop recommends to avoid a completely migrate such storefront cartridges.

Migrate all your custom cartridges that are not storefront customization cartridges and add them to the project assembly. This includes changes to the source structure, the use of Gradle, the dependency declarations etc.

This only should be done for cartridges that extend the Intershop Commerce Management application, System Management application etc. or add basic functionality that is not depending on any previous storefront cartridge like *app_sf_webshop* or *sld_ch_b2_app*.

Once all these changes have been applied:

Publish your project and deploy the server.

cd <COMPONENTSET> gradlew publish gradlew deployServer

If these steps do not result in `"BUILD SUCCESSFUL`

" additional migration changes are needed according to the given failure messages.

Use *dbmigrate* to migrate the project data from your current Intershop version to the intended newer Intershop version, see [Cookbook - DBMigrate](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1875055597/Cookbook+-+DBMigrate) and [Concept - DBMigrate and DBInit](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1822568213/Concept+-+DBMigrate+and+DBInit) for details.

With this step your product data, customer data, etc. is migrated to the new Intershop version. Only the previously removed CMS content is not migrated since this cannot be done automatically anyways.

Once the server is successfully deployed and the data is migrated the server can be started.

Doing so you get a server that already has the Responsive Starter Store functionality but no working content yet. Therefore the storefront will render empty or with an error. Migrating the content is addressed in the next sections.

Since the content and the structure of branding packages was changed in the Responsive Starter Store and the CSS classes of the Responsive Starter Store are completely different from the PrimeTech reference store, it is necessary to:

To get an initial state of the Responsive Starter Store content into the projects storefront one could start to create and assign page variants and components via the Commerce Management application, or one could use the provided white-label content that comes as part of the downloaded Responsive Starter Store. The [Concept - White Label Store](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1787201923/Concept+-+White+Label+Store) explains the process in detail but the basic steps for a migrated project that does not itself include the demo_responsive_content cartridge of the Responsive Starter Store are the following:

Create the needed *whitestore-democontent.zip* from the Responsive Starter Store by zipping the folder * a_responsive\demo_responsive_content\staticfiles\share\sites\inSPIRED-inTRONICS-Site\units\inSPIRED-inTRONICS-b2c-responsive\impex\src\white-label store. *

for smb/b2b applications

Create the needed *whitestore-democontent.zip* from the Responsive Starter Store by zipping the folder *a_responsive\demo_responsive_content\staticfiles\share\sites\inSPIRED-inTRONICS_Business-Site\units\inSPIRED-inTRONICS_Business-smb-responsive\impex\src\white-label store*.

In case your are not only using the plain *smb* application but the *b2b* application the content of *a_responsive\demo_responsive_b2b\staticfiles\share\sites\inSPIRED-inTRONICS_Business-Site\units\inSPIRED-inTRONICS_Business-smb-responsive\impex\src\white-label store* needs to be added to the *whitestore-democontent.zip* too.

The zip files folder structure should look like that:

`whitestore-democontent.zip` `├── component` `├── componenttemplate` `├── enfinity` `├── include` `├── META-INF` `├── page` `├── pagetemplate` `├── pagevariant` `└── ` |

Copy the* **whitestore-democontent.zip* to your servers shared file system to * <IS_SHARE>\sites\<YourOrganization-YourChannel>Site\units\ <YourOrganization-YourChannel-YourApplication> \impex\src *.

Lo into the Commerce Management application, switch to your now Responsive Starter Store based storefront application and go to Content > Import & Export.

There the option *Prepare application content* should be available.

Click the *Prepare* button.

This starts an import process of the *whitestore-democontent.zip* into your application and should finish without any errors.

Click on Preview in the main navigation should bring you to the with default content prepared Responsive Starter Store storefront.

At this point you should have a shop running on a current Intershop 7 version with a plain Responsive Starter Store storefront.

After the Intershop Commerce Management base is migrated and a standard Responsive Starter Store storefront is running on top of it it is a good point to:

Once the relevant parts of your content model are identified, it is necessary to:

The following steps are manual steps with a capable text editor or any scripting tool of your choice.

In general the content of CMS export files should look similar to the below directory listing.

`<CMS_EXPORT_FILE_CONTENT>` `├── component` `├── componenttemplate` `├── enfinity` `├── include` `├── META-INF` `├── page` `├── pagetemplate` `├── pagevariant` `└── ` |

The root directory of this listing is usually the place for any batch operation in case the migration is done export file by export file. If the migration is done for all content exports it will be a collection of such root directories.

There are probably only a few components that stayed similar between your Intershop source version and the Responsive Starter Store content model that could be mapped between the two content models. This applies mainly for the components that do actually contain content but are not heavily involved in the storefront configuration, like the *Freestyle HTML* and *Image* components.

Adapt the old components (previous content model) from the export files to be imported again in the new content model.

| Old content model | Responsive Starter Store Content Model | ||
|---|---|---|---|
| comp.common.freeStyle.pagelet2 | Common - Freestyle HTML Text | Free Style HTML | component.common.freeStyle.pagelet2 |
| comp.common.imageTeaser.pagelet2 | Common - Image Teaser | Image | component.common.image.pagelet2 |

On top of the components that can be mapped between the standard Intershop content models, the migrated, required parts of the project content model (see step before) need to be migrated in the Import/Export files too.

The following steps will be necessary on these Import/Export files to only include the relevant parts of migrated CMS content.

After applying all the manual migrating steps:

Once the content import is executed without errors or warnings the content migration on the import files is done. All remaining steps can be done on the server.

After successfully migrating the storefront and importing the relevant CMS content it is a good time to check the result in the storefront.

At this point it is necessary to use the Data View or the Design View to further edit content, especially the *Freestyle HTML* components. Here the CSS classes and the HTML structure needs to be adjusted to the Responsive Starter Store.

Once the content is completely changed to look as expected, it can be exported and used to prepare the content of migrated QA or editing systems.

Once the basic migration is done and the storefront is running on top of the Responsive Starter Store cartridges the migration of custom features to the Responsive Starter Store can be tackled.

whitestore-democontent.zip

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.