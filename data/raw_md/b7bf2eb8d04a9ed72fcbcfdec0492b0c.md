---
id: 'b7bf2eb8d04a9ed72fcbcfdec0492b0c'
title: 'Product Lifecycle'
url: 'https://knowledge.intershop.com/kb/index.php/Display/321E95'
scraped_at: '2026-04-21T05:33:56.332310+00:00'
---
# Product Lifecycle

Two special attributes are available to manage the product lifecycle.

-
The last order date defines the latest point in time at which a product can be ordered. The product remains visible in the storefront, but cannot be added to the basket anymore.

-
The end-of-life date has the same effect. It can be used for additional purposes, e.g., to indicate when support for a product expires. Note that the end-of-life date (if defined) has to follow the last order date.


Product lifecycle definitions can be used as advanced search parameters.

[Product Bundles and Retail Sets](https://knowledge.intershop.com/oh/go.php/icm/master/icm_main_en/catalogs_products/concept_product_bundles_and_retail_sets.html)) and product variation masters (see

[Product Variations and Product Variation Types](https://knowledge.intershop.com/oh/go.php/icm/master/icm_main_en/catalogs_products/concept_product_variations_and_product_variation_types.html)) can inherit the last order date and the end-of-life date from the bundled products or variation products they contain. When using the inheritance mechanism, last order date/end-of-life date of the product bundle or variation master is automatically set to the earliest last order date/end-of-life date set for one of the contained products. Alternatively, the last order date/end-of-life date can be set manually for product bundles or variation masters.