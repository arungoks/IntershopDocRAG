---
id: 'fbe8837fadd85dcfaa53e0f89f477be3'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/Z25911'
scraped_at: '2026-04-21T05:35:56.907520+00:00'
---
Product and Category links are objects that are intended to be explored by a customer when browsing product pages and / or category pages. The purpose is to show the customer related offers. Providing such information may tempt a customer to buy more. Actually a product link represents another product, while a category link represents another categories. Possible combinations for this type of data are the links between:

Samples are "Cross-Selling" and "Ship-together-items" (e.g., buy batteries, if the mixer in the basket needs some). Therefore, different types of links are necessary to respond to the actual business needs. The standard product provides some basic types of links that can be used if no need for a different type exists. If such new types are necessary they have to be added/implemented in a custom project.

If a custom project needs to add a new link type to respond to the business requirements, use the cookbook according to the appropriate version:

The different types of links are represented by type codes. Type codes are integer numbers and one single number represents one link type.

The standard product provides following type codes and for what kind of link it is used:

Type codes are initially created during dbinit. Each type code has to be defined globally by appropriate entries. See the according cookbook according to your desired version. All available cookbooks for this topic are listed in the [References](https://knowledge.intershop.com#References) section.

Semantic of link types means the explanation of "what they can be used for" and how to decide what kind of link to be assigned to a product or to a category. As shown on the diagram above each link type has own ID and display name in order to be readable for the end user and thus addresses the different use cases applicable for the links. Each link type is self-describing for which use case it could be applied.

The following table contains basic description for each of the standard link types:

| Link Type | Description |
|---|---|
| Cross-Selling | Offer related products to incite buyers to purchase more than originally intended. |
| Replacement | Offer similar/substitute products to buyers. |
| Up-Selling | Offer alternative, higher-value products to incite buyers to purchase higher-priced products. |
| Accessory | Offer complementary products to incite buyers to purchase more than originally intended. E.g., a case might be offered for a notebook. Not usable for ship-together items. |
| Follow-Up | Refer to follow-up (newer) version(s) of the product. |
| Different Order Unit | Refers to offer(s) of the same product sold in a different order unit. |
| Spare Parts | Offer available spare parts for a product. |
| Other | |
| Proxy Product | From the frontend perspective, a Proxy Product could be seen as a clone of a "real" product. |
| Warranty | A warranty relation between a product/category and a warranty product. |
| Gift Wrap | Products representing gift wrapping for other product(s). |
| Gift Message | Products representing a gift wrapping message for other product(s). |

The table shows the link types that can be used with links between:

For links between

standard product provides additional (category) link types:

| Type Code | Link Type | Description |
|---|---|---|
| 1 | Cross-Selling | Offer related 'category of' products to incite buyers to purchase more than originally intended. |
| 2 | Up-Selling | Offer alternative, higher-value products to incite buyers to purchase higher-priced products. |
| 3 | Accessory | Offer complementary products to incite buyers to purchase more than originally intended. E.g., a case might be offered for a notebook. Not usable for ship-together items. |
| 4 | Follow-Up | Refer to follow-up (newer) version(s) of products within the category. |
| 5 | Spare Parts | Offer available spare parts for products of this category. |
| 6 | Other |

Product links represent the relation between one product and another product which are linked together. The product link logically points from a source product to a target product. Each product link has a type code which is used to determine the type of the link. All the type codes are defined by type code definitions and these definitions must define a group with name equals to the constant `ProductLink:TypeCodeDefinitionGroup`

, i.e., the type code definition group defined by the product link itself.

To ensure uniqueness of the `TypeCodeDefinition:Name`

the following naming convention should be used: use the project name as a prefix for the type code name, followed by an underscore. Standard Intershop and Enfinity use "ES_" as prefix for its type code names.

The following diagram shows the `ProductLink `

object with its relations:

The diagram above shows a `ProductLink `

object with possible attributes and a constant that defines the type code group to filter applicable type code definitions. In our case we have a link of type "Follow-Up" which brings together both source (*Product 2*) and target (*Product N*) products. Thus we have both products linked and entering source product page (*Product 2* - Links) will show the links to the other products (if any) with the link type. In our case entering *Product 2 - Links* page will show us *Product N* as a product link of type "Follow-Up", i.e., *Product 2* has as a "Follow-Up" link *Product N*. In other words, *Product 2* has **outgoing **link to *Product N* of type "Follow-Up". Entering *Product N - Links* page will show us that this is a "Follow-Up" link of *Product 2*. At the target product's side *Product N *has **incoming** link from *Product 2* of type "Follow-Up".

Category links are used to establish cross-relations between catalog categories in opposite to the parent-child relations on which the catalog structure is based. The category link points from a so called source CatalogCategory to a target CatalogCategory. Each category link has a type code which is used to determine the type of the link. All the type codes are defined by type code definitions and these definitions must define a group with name equals to the constant `CatalogCategoryLink:TypeCodeDefinitionGroup`

, i.e., the type code definition group defined by the category link itself.

To ensure uniqueness of the `TypeCodeDefinition:Name`

the following naming convention should be used: use the project name as a prefix for the type code name, followed by an underscore. Standard Enfinity uses "ES_" as prefix for its type code names.

The following diagram shows the `CatalogCategoryLink`

object with its relations:

The diagram above shows a `CatalogCategoryLink `

object with possible attributes and a constant that defines the type code group to filter applicable type code definitions. In our case we have a link of type "Spare Parts" which brings together both source (*CC23@Catalog 1*) and target (*CC211@Catalog 2*) categories. Thus we have both categories linked and entering source category page (*CC23@Catalog 1* - Links) will show the links to the other categories (if any) with the link type. In our case entering * CC23@Catalog 1 - Links* page will show us

A product-category assignment is used to bind a product to a catalog category.

Note

A product can have multiple product-category assignments. This means that a product can be bound to several catalog categories at the same time.

Note also that there are different types of product-category assignments. The plain product-category assignment is used to assign products to the category tree for catalog browsing, whereas other assignments (like typed product-category assignment) may be used for purposes like defining hot deal products of a category or cross sell products for a category or any other product-category relations which should (by default) not show up in the regular product list of a category when browsing the catalog tree.

Typed product-category assignments represent the relation between a catalog category and a product which are linked together. Each typed product-category assignment has a type code which is used to determine the type of the link (or the type of the assignment). All the type codes are defined by type code definitions and these definitions must define a group with name equals to the constant `TypedProductCategoryAssignment:TypeCodeDefinitionGroup`

, i.e., the type code definition group defined by the assignment link itself.

Typed product-category assignments represent the links between:

To ensure uniqueness of the `TypeCodeDefinition:Name`

the following naming convention should be used: use the project name as a prefix for the type code name, followed by an underscore. Standard Enfinity uses "ES_" as prefix for its type code names.

The following diagram shows the `TypedProductCategoryAssignment`

object with its relations:

The diagram above shows a `TypedProductCategoryAssignment`

object with possible attributes and a constant that defines the type code group to filter applicable type code definitions. In our case we have a link of type "Replacement" which brings together both category (*CC32@Catalog 1*) and product (*Product 3*). Thus we have category and product linked and entering category page (*CC32@Catalog 1* - Links) will show us *Product 3* as a product link of type "Replacement", i.e., * CC32@Catalog 1* has as a "Replacement" link

The following screenshot represents the assigned product and category links of a regular product:

The following screenshot represents the assigned product and category links of a category:

The following screenshot shows the assigned product and category links of a regular product page in storefront:

The following screenshot shows the assigned product and category links of a category page in storefront:

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.