---
id: 'bdfca893fd4d6a0d2ecb0e11f2950afd'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/31D295'
scraped_at: '2026-04-21T05:35:04.280493+00:00'
---
This concept discusses features of the catalog component, which belongs to a set of business components and provides functionality that can be used in a variety of business scenarios.

Catalog features include:

Repository and catalog concepts

Catalog filters

Classification catalogs

[Overview - Catalog Management](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1755492938/Overview+-+Catalog+Management) - lists all available documents for this topic

This chapter discusses catalog and repository concepts, catalog filters, and classification catalogs.

A sales organization can set up multiple product catalogs. Those product catalogs can be shared with the channels of the sales organization. Catalogs can be created manually in the Commerce Management application on organization and channel level. Catalog structures can also be imported via a file in different import modes.

An import process with DELETE mode does not remove the catalogs from the system, but only their sub-categories.

Intershop Commerce Management allows to create and maintain different types of catalogs or categories using the *Catalogs* section in the *Master Catalogs* manager in the parent organization and the* Catalogs* manager in the channels. The intention of catalogs is to structure products in a meaningful way. The structure helps customers by making it easier and faster to find products in the storefront. The different catalogs types are:

Standard Catalogs - type code 1. Provided by the parent organization (shared catalogs) or locally created for the channel (local catalogs):

Local Standard Catalogs - Manually managed catalogs

Shared Standard Catalogs - Structure of a shared catalog

Classification Catalogs - type code 2:

Shared Classification Catalogs - Classification systems that are either globally available (eCl@ss, UN/SPSC) or maintained by your parent company

Local Classification Catalogs - Manually managed classification systems displayed as local classification catalogs

System Classification Catalogs - To handle special products like warranties, proxy products for customization, gift wraps, and other types:

Shared System Classification Catalogs

Local System Classification Catalogs

A catalog describes a container and serves as a root for the categories below it. There is no limit to the number or depth of underlying categories. Multiple root catalogs can exist in parallel. The *Catalogs* section contains a list of catalog types which can be expanded and collapsed as required.

When a new catalog of a certain type is created, a new row is added to the `CATALOG`

database table. The new record is also stored in the `CATALOGCATEGORY`

table. When a new catalog is created, a new root category is automatically created for it. A category object (the object name is CatalogCategory) structures a catalog to present sub-categories in a hierarchical structure. It is defined in the context of a domain. Each catalog has a unit domain depending on the level at which it is created - organization or channel. In this case, the domain can be, for example, *inSPIRED *(organization) or *inSPIRED-inTRONICS_Business* (channel). At the same time, for each catalog, its catalog domain is created with the name *<OrganizationName>-<CatalogName*> / *<OrganizationName>-<ChannelName>-<CatalogName>*. For example *inSPIRED-inTRONICS_Business-catalog* for a catalog created on channel level, or *inSPIRED-Computers* for a catalog *Computers* created in the *inSPIRED *organization.

All sub-categories of a catalog are created in the catalog domain, so a category *TestCategory* that is a sub-category of *Computers* will inherit the domain *inSPIRED-Computers*.

The creation of a new catalog creates a new catalog category object.

A new catalog is created in the *Catalog* database table.

Every catalog has its own domain.

The creation of a new catalog creates a new catalog domain.

A new `CatalogCategory`

object is created in the `CATALOGCATEGORY`

database table.

The `CatalogCategory`

object has its own domain, the catalog domain.

To create a new catalog:

Choose the desired organization level (organization or channel).

Navigate to *Master Catalogs | Catalogs*.

In the section of the desired catalog type, click *New*.

Enter the basic information and click *Apply*.

The *Product Assignment* section is displayed.

(Optionally) Enter the required data and click *Apply*.

Click *Back to List*.

The new catalog appears in the according section.

Catalogs can be edited at any time.

Click the *Edit* button in the *Actions* column of the catalog list.

The *Product Assignment* section of the *General* tab offers two options:

Assign Products manually

Assign Products dynamically

The first option is default. In this case, the *Product Sorting* section is displayed.

The manual sorting can be *Default* or *Custom*. The custom sorting depends on the *Sorting Attribute* that can be standard or custom. Also the *Sorting Direction* can be selected.

If a catalog is shared from the parent organization, it cannot be edited at channel level. Name, ID, Description, and Product Assignment fields are disabled, and the optional sections *Assign Products manually* and *Assign Products dynamically* are not displayed.

Catalog, category, and product sorting can also be defined in the *Channel Preferences*, section *Sorting*:

When *Assign Products dynamically* is selected, a new section appears. Here you can specify the catalog category (*Category* subsection) to which the product filter search operation is restricted. In the sub section *Filter Condition*, you can specify text values (for text attributes) or value ranges (for numeric attributes) intended to be retrieved by the filter. The *Weighting* subsection allows you to specify a weight for specific attribute values. Also sorting can be selected. Up to 10 entries can be created for each filter condition, sorting, or weighting.

The conditions are connected by AND. Only filter conditions for the same attribute are connected by OR.

For dynamic product assignment, a valid search index must exist. If there is no configured search index, the following message is displayed:

"No Search Index found. Please create a Search Index of type 'SFProductSearch'."

Creating a dynamic product assignment adds a new record of type `product`

to the `searchquerydefinition`

table. In the `searchquery`

column, all configurations are stored in XML format, as shown in the following snippet:

<searchquery> <contextcategoryid>catalog1@inSPIRED-catalog1</contextcategoryid> <multi-value-conditions/> <range-conditions> <range-condition> <attribute-name>ProductSalePriceNet</attribute-name> <attribute-lower-value>1</attribute-lower-value> <attribute-upper-value>10</attribute-upper-value> </range-condition> </range-conditions> <rankings> <ranking> <attribute-name>shortDescription</attribute-name> <percentage>10</percentage> <attribute-value>description</attribute-value> </ranking> </rankings> <sortings> <sorting> <attribute-name>name</attribute-name> <direction>ASCENDING</direction> </sorting> </sortings> <value-conditions> <value-condition> <attribute-name>ManufacturerName</attribute-name> <attribute-value>Dell</attribute-value> </value-condition> </value-conditions> </searchquery>

Use the *Content *tab to manage the assigned pages and includes for this catalog.

Use the *Online/Offline* tab to limit the catalog's online/offline period.

Specify whether the catalog is *Always* available or only for a *Limited period*.

Set *Start Date/Time* and *End Date/Time* when using *Limited period*.

From the master organization, a catalog can be shared with all channels to benefit from re-usability and to avoid unnecessary administration efforts. The sharing applies only to catalogs, but not to categories.

On organization level navigate to *Master Catalogs | Catalogs*.

Edit a catalog.

Switch to the *Channels* tab.

A list of currently unassigned channels will be displayed.

Click *New*.

In the Assign New Channel dialog, select a channel and click *OK*.

Click *Back to List*.

After successful sharing, the channel appears in the list as the following picture shows. In the example below, the catalog is shared to *inTRONICS *and *inTRONICS Business* channels.

When a catalog is shared to a channel, a new record is created in the `catalog`

database table. The new row has a different value in the `domainid`

column, which points to the domain ID of the assigned channel.

In the *Sub-Categories* tab, new sub-categories can be created for the catalog. Sub-categories can be sorted.

You cannot add new sub-categories to shared catalogs and channel-level categories, and you cannot remove existing sub-categories.

The following diagram shows the relation between a catalog and its sub-categories. A catalog belongs to its own domain, and each catalog has a catalog domain. The sub-categories are created in the catalog domain. So the own domain of a sub-category is the catalog domain.

The *Attributes* tab allows to add custom and SEO attributes to a catalog. In the SEO Attributes section, you can define web search engine attributes to improve search result rankings.

New attributes cannot be appended to shared catalogs or categories.

The *Labels* tab allows for grouping certain elements to perform all kinds of tasks afterwards. Catalogs can be combined by using labels.

To create a new label:

Click *New*.

The Assign Label dialog is displayed.

Specify the label Name and label ID and click *Add*.

The *Labels* tab is not available for shared catalogs on channel level.

When a label is assigned to a catalog or category, a new record is created in the `catalogcategorylabelassignment`

table. The label UUID, catalog/category UUID, and domain ID are stored there.

The *Links* tab allows to manage links between independent products and categories. A catalog can have multiple links to the products of other catalogs/categories and to individual products. The catalog can have different types of links and can also be a link. The link types are:

Cross-Selling - related individual products or all products in selected categories

Up-Selling - alternative individual products or all products in selected categories

Accessory - complementary individual products or all products in selected categories

Follow-Up - selected individual products or the products in the selected categories are follow up version(s)

Spare Parts - selected individual products or the products in the selected categories are as available spare parts

Other

The *Links for catalog* section displays the link types that can be assigned to the current catalog. In the right section the catalog can be linked to other products or catalogs/categories.

For more information about catalog and category link see [Concept - Product and Category Links](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1793821593/Concept+-+Product+and+Category+Links).

Intershop 7 offers various import & export functionalities for catalog data. At the moment there are three different types of catalog/category import-export processes:

XML Import & Export - Import or export catalog categories or whole catalogs from or into XML files.

CSV Import - Import catalog categories or whole catalogs from CSV source files. CSV export is currently not available.

BMEcat Import & Export - Import or export catalog categories from or into XML files in BMEcat format.

Before importing, a file must be uploaded to the server. Once the file has been validated, the catalogues and categories can be imported.

The following import modes are available:

UPDATE

DELETE

REPLACE

OMIT

IGNORE

INITIAL

The export process extracts data from the system and save them into a file. The export file must have a name and a file extension. Depending on the amount of data, the export may take some time. Once the process is completed, the generated file can be downloaded. The download can be started from the Import & Export section. A click on a file name link opens a new page holding a log file if there are any errors or warnings. A click on the exported file link starts the physical download.

The following XML snippet shows an example of exported catalog category file structure. The import process expects the same XML structure.

**Catalog Category Import&Export XML File Structure**

<?xml version="1.0" encoding="UTF-8"?> <enfinity xsi:schemaLocation="http://www.intershop.com/xml/ns/enfinity/7.0/xcs/impex catalog.xsd http://www.intershop.com/xml/ns/enfinity/6.5/core/impex-dt dt.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.intershop.com/xml/ns/enfinity/7.0/xcs/impex" xmlns:xml="http://www.w3.org/XML/1998/namespace" xmlns:dt="http://www.intershop.com/xml/ns/enfinity/6.5/core/impex-dt" major="6" minor="1" family="enfinity" branch="enterprise" build="build"> <category name="catalog" import-mode="UPDATE"> <name>catalog</name> <root>1</root> <product-assignment-query></product-assignment-query> <template></template> <online>1</online> <category-links> <category-link name="Cameras-Camcorders" domain="inSPIRED-inTRONICS-Cameras-Camcorders"> <category-link-type name="ES_SpareParts_C"></category-link-type> <position>1.0</position> </category-link> </category-links> <description xml:lang="en-US"></description> <display-name xml:lang="en-US">catalog</display-name> <searchquery-definition-name>sCwKDACUGGEAAAFKfekHZM2N</searchquery-definition-name> <custom-attributes> <custom-attribute name="PRODUCT_SORTING_TYPE" dt:dt="string">default</custom-attribute> <custom-attribute name="ShowInMenu" dt:dt="string">True</custom-attribute> </custom-attributes> </category> <category name="1"> <name>1</name> <root>0</root> <product-assignment-query></product-assignment-query> <template></template> <online>1</online> <position>1.0</position> <category-links></category-links> <description xml:lang="en-US"></description> <display-name xml:lang="en-US">1</display-name> <parent name="catalog" /> </category> </enfinity>

XML files in BMEcat format can also be used to import and export catalogs and categories.

BMEcat is a standard for electronic data transfer by electronic catalogs created and published by the **BME** (Bundesverband Materialwirtschaft, Einkauf und Logistik e. V., the German association for materials management, purchasing and logistics). BMEcat is about actual instances of application classes which are described by distinct values in accordance to the dictionary. The following snippet shows the same catalog as the snippet above, but exported in BMEcat format.

Imports of catalogs and categories using BMEcat format sometimes require adaption to the import file validation (XSD), see [Cookbook - Catalog | Recipe - Adapt BMEcat Import File Validation](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1826491717/Cookbook+-+Catalog#BMEcatImportValidation).

**Catalog Category Import&Export BMEcat File Structure**

<BMECAT xmlns="http://www.bmecat.org/XMLSchema/1.2/bmecat_new_catalog" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.bmecat.org/XMLSchema/1.2/bmecat_new_catalog bmecat_new_catalog_1_2.xsd" version="1.2"> <HEADER> <CATALOG> <LANGUAGE>eng</LANGUAGE> <CATALOG_ID>catalog</CATALOG_ID> <CATALOG_VERSION>1.0</CATALOG_VERSION> <CATALOG_NAME>catalog</CATALOG_NAME> <DATETIME type="generation_date"> <DATE>2015-01-14</DATE> <TIME>10:18:31</TIME> </DATETIME> <TERRITORY>US</TERRITORY> <CURRENCY>USD</CURRENCY> </CATALOG> <SUPPLIER> <SUPPLIER_ID>inSPIRED</SUPPLIER_ID> <SUPPLIER_NAME>inSPIRED</SUPPLIER_NAME> <ADDRESS type="supplier"> <NAME>inSPIRED</NAME> <NAME2>Max Meier</NAME2> <STREET>Main Street</STREET> <ZIP>143456</ZIP> <CITY>inSPIREDCity</CITY> <COUNTRY>Germany</COUNTRY> <EMAIL>inSPIRED_info@test.intershop.de</EMAIL> </ADDRESS> </SUPPLIER> </HEADER> <T_NEW_CATALOG> <CATALOG_GROUP_SYSTEM> <CATALOG_STRUCTURE type="root"> <GROUP_ID>1</GROUP_ID> <GROUP_NAME>catalog</GROUP_NAME> <PARENT_ID>0</PARENT_ID> </CATALOG_STRUCTURE> <CATALOG_STRUCTURE type="leaf"> <GROUP_ID>2</GROUP_ID> <GROUP_NAME>2</GROUP_NAME> <PARENT_ID>1</PARENT_ID> <GROUP_ORDER>1</GROUP_ORDER> </CATALOG_STRUCTURE> <CATALOG_STRUCTURE type="leaf"> <GROUP_ID>1</GROUP_ID> <GROUP_NAME>1</GROUP_NAME> <PARENT_ID>1</PARENT_ID> <GROUP_ORDER>1</GROUP_ORDER> </CATALOG_STRUCTURE> </CATALOG_GROUP_SYSTEM> </T_NEW_CATALOG> </BMECAT>

Catalog categories or entire catalogs can also be imported from CSV source files. This process only works for imports. The following image shows how the CSV file is presented in Excel. The different values are separated by a **" ; "** .

There are few mapping template types and one of them can be selected. Also field delimiter and format line number can be defined.

One of the key concepts of the catalog feature is the strict separation of catalog structure and product data. This separation is implemented by the concept of catalogs and repositories.

The concept itself is described best through the following definitions:

**Repository**

A repository is a container for product and / or offers content owned by an organization. There are two types of repositories:

Master Repository - Each sales organization has a master repository to set up its products. Products can be derived from the master repositories to the available channel repositories. Each organization can have multiple repositories to store product data.

Channel Repository - Channel repositories are defined in the context of a channel. Each channel has a channel product repository. The channel repository contains the products to be made available to consumers, customers, or partners.

Using master and channel repositories, products can flow down the demand chain: from the sales organization to consumers, customers, and partners, from sales partners to resellers, and so on. To enable this kind of information flow, products must be shared between repositories. With product sharing, the sales or partner organization can distribute large numbers of master products to consumer or business channels without copying them. The sharing targets are consumer and business channels only. The products remain in the base repository from which they are shared. Target channels can also add new products or change the attributes of a base product by overriding the entire product. If any attribute of the base product is changed, a new derived product is created with reference to the base product (`DERIVEDPRODUCT`

table).

**Catalog**

A catalog provides a specific view of an existing product / offer repository. The catalog view is defined by a specific hierarchy of catalog categories. Catalogs also contain the bindings (product category assignments) between the products of a repository and the actual catalog category. The main advantage of this concept is that multiple catalogs (i.e., catalogs in terms of navigation structure) can now be defined for the same repository. This feature is particularly useful when it comes to supporting standard classifications (such as eCl@ss) for the product content of an organization.

With respect to the implementation of catalogs and repositories, the Intershop domain concept plays an important role.

For **catalogs**, the following implementation concepts are of importance:

A catalog is modeled as a standard business object in the public API.

A catalog is always associated with a domain instance (the catalog domain).

The catalog domain is used to store the actual catalog content (catalog categories).

A catalog instance is always owned by a domain. A single domain can own multiple catalog instances. A single catalog is always owned by a single domain.

Multiple catalog instances can reference the same catalog domain.

The implementation model for **repositories** is similar:

A repository is modeled as a standard business object in the pubic API.

A repository is always associated with a domain instance (i.e., the repository domain).

The repository domain is used to store the actual repository content (i.e., the products / offers and their category bindings).

A repository is always owned by a domain. A single domain can own multiple repository instances. A single repository is always owned by a single domain.

The image below illustrates the implementation concept and its integration with the organization and domain concept.

The organization depicted below owns a single product repository and a single catalog view.

The entire implementation relies on basic mechanisms of the Intershop domain concept.

The catalog and repository instances basically serve as descriptors (or proxies) for the catalog and repository domains, respectively.

The domains instantiated along with each catalog and repository serve as storage containers that logically separate the content to be stored.

This logical separation of content has major advantages in various search scenarios where content of certain repositories / catalogs should be searched. Based on the (content) domain concept, it is very easy to limit searches to certain repositories and or catalogs.

Another advantage of this implementation approach is that all IS7 features relying on domains can be used. This greatly facilitates, for example, the implementation of catalog specific user management (i.e., different catalog managers per catalog within a single organization) since it is possible to directly rely on the domain user group handling.

The UML diagram below provides a high-level view on the implementation of catalogs and repositories.

Catalogs as well as repositories feature numeric type codes as well as unique catalog and repository IDs.

Numeric type codes can be used to separate different types of catalogs (e.g., external catalogs, standard catalogs, classification catalogs).

The interpretation of the type codes is up to the application that uses the catalogs.

The catalog / repository ID is intended to be a human-readable identifier that uniquely identifies a catalog / repository instance in the context of an owning domain. The ID specified upon catalog / repository creation is used as domain ID for the resulting catalog / repository domain.The catalog manager prefixes the provided catalog / repository ID with the domain name of the owning organization to ensure globally unique domain names. For example, when creating a catalog *MyCatalog* in the context of Organization *inSPIRED*, a catalog domain with ID `inSPIRED-MyCatalog`

will be created. All sub-categories created under the catalog will belong to the respective catalog domain.

Catalog Filters, also known as Catalog Views, have been changed multiple times during different versions of Intershop software. There are separate concepts (see [Overview - Catalog Management](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1755492938/Overview+-+Catalog+Management) for a list of all available documents) explaining the catalog views in the different versions. The basic idea of catalog views is the control of product visibility, show or hide catalog content to or from specific consumer groups.

Intershop 7 (IS7) provides out-of-the-box support for two standard classification mechanisms:

eCl@ss

UN/SPSC

It also allows to create custom classification catalogs. (e.g.: 'ServiceTypes', 'ProductTypes').

For details on classification catalogs refer to the Concept: [Classification Catalogs](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1787204428/Concept+-+Classification+Catalogs+valid+to+7.6).

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.