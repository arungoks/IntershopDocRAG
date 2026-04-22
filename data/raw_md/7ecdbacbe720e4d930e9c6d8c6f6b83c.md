---
id: '7ecdbacbe720e4d930e9c6d8c6f6b83c'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/30G892'
scraped_at: '2026-04-21T05:37:20.859465+00:00'
---
This document describes the new* Basket Processing API* initially introduced with Intershop version 7.4 including the latest changes done with version 7.8.

The previous basket handling implementation on processing layer(s) can be considered as being historically evolved from early Enfinity versions until Intershop version 7.3 and could not satisfy present and future requirements any longer because of the following lacks and issues:

The advent of the new *Application*-centric design in Intershop 7 and the fact that basic Intershop 7 frameworks have not to support Web UI based applications exclusively, but also mobile clients and REST clients results in the following main requirements:

`com.intershop.beehive.app.capi.AppContext`

instance is available in all pipelines now and contains all necessary information, e.g., for retrieval of configuration values.During its lifetime a basket is in one of the following states:

After the basket creation (1) the basket is in the state BASKET_OPEN. The creation is triggered when a customer adds a product to the basket for the first time. When customer successfully finishes his/her checkout (4), the basket gets the state BASKET_ORDERED. The transition (2) from BASKET_OPEN to BASKET_EXPIRED depends on the basket type. A session-based basket will get this state when the session times out or user logs out. A time-based basket, which reaches the configured inactivity time period (domain preference "BasketLifetime") is moved to the basket history by the background job *Move Outdated Baskets To History*. Note that the actual expiration time of a basket depends on a combination of both, the configured inactivity time period as well as the run-time of the job: For instance, if the inactivity time period is set to two hours, but the job runs only once at midnight, then an inactive basket may still become active again, if the configured inactivity time period is increased in the back-office after the two hours have passed, but before the end of the day.

After basket reaches the state BASKET_EXPIRED, it is treated in the same way independent from its type.

Either the basket is marked as removable by changing its state to BASKET_INVALID (5) after a configurable period of time (domain preference "BasketInHistoryLifetime") or it is 'reactivated' for some reasons (3). It is in the responsibility of the functionality that 'reactivates' the basket from basket history to remove certain parts of the basket, e.g. payment methods, addresses, item prices, etc.

The transition to BASKET_INVALID is made by the job * Invalidate History Baskets*. It updates the field status only. The job *Remove Invalid Baskets* finally purges (7) all invalid baskets from the database.

You will find a description and additional information about the jobs in [Reference - Intershop 7.8 Jobs](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1824065011/Reference+-+Intershop+7.8+Jobs).

Baskets are created by the pipeline `ViewCart-GetCurrentCartBO`

in case they cannot be retrieved from a session or cookie by calling lower level processing pipelines. For unregistered users and time-based baskets, a basket cookie is created so the basket will be restored in case the user leaves the shop and the session is terminated.

Business object layer specific logic is implemented in the `bc_orderprocess`

pipeline, the `bc_basket`

(BO interfaces), *bc_basket_orm* and *sld_ch_b2c_base* cartridges (BO implementations).

`ProcessBasket-CreateBasket`


The pipeline defines following extension points:

`CreateBasket`

`CreatedBasket`

Extension pipelines assigned to extension point `CreateBasket`

are called before the basket will be created. Pipelines assigned to this extension point are **not **part of the basket creation transaction.

Extension pipelines assigned to extension point `CreatedBasket`

are called after the basket has been created. Pipelines assigned to this extension point are part of the basket creation transaction.

Basic basket creation functionality is done in Java by implementations of `com.intershop.component.basket.capi.BasketBORepository`

which provide the following two methods:

BasketBO createBasketBO(); BasketBO createBasketBO(UserBO user);

The only difference between the two methods above is that the second one assigns the basket to the given user. There may be application specific implementations of `com.intershop.component.basket.capi.BasketBORepository`

that implement other or additional behavior.

Existing baskets are retrieved by the pipeline `ViewCart-GetExistingCartBO`

. The lookup mechanism first checks the session dictionary for an active basket. If a basket is found and not expired, this one will be used in the further checkout process. Otherwise the user's active baskets will be looked up from the database. If there is an active (not expired) basket, this one will be returned. For anonymous users and time-based baskets a basket cookie is created. If there is neither a basket for the current user in the session dictionary nor in the database, this basket cookie will be used to retrieve the basket. When a basket is retrieved this way, the basket will be anonymized and the owner will be set to the current user.

Business object layer specific logic is implemented in the `bc_orderprocess`

(pipeline), the `bc_basket`

(BO interfaces), *bc_basket_orm* and *sld_ch_b2c_base* cartridges (BO implementations).

`ProcessBasket-GetBasketByID`


`ProcessBasket-GetBasketsByUser`


In contrast to the previous `ProcessCart`

pipelines, no new basket is created if no existing one has been found.

Basket business object instances can be retrieved by implementations of `com.intershop.component.basket.capi.BasketBORepository`

. A repository defines the following methods:

BasketBO getBasketBO(String id); BasketBO getActiveBasketBO(String id); Collection<? extends BasketBO> getActiveBasketBOs(); Collection<? extends BasketBO> getActiveBasketBOs(UserBO user);

Method `getActiveBasketBO(String id)`

only returns the basket with the specified ID if it is in the state BASKET_OPEN, whereas method `getBasketBO(final String id)`

returns a basket that is in state BASKET_EXPIRED too. None of the methods above returns baskets that are in the states: BASKET_ORDERED, BASKET_INVALID, BASKET_UNSPECIFIED.

Adding a product to the basket may be a simple operation at the first glance. There are a lot of special cases beside the happy path that have to be considered.

Handler chain executes listed pre-add-to-basket handlers in the following order:

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductVariationHandler`


If the product to be added specified in the add-to-basket context is a *Variation Master* then handler tries to retrieve the default variation product. If default variation product exists then this one is set at the add-to-basket context instead, otherwise handler indicates an failure if no default variation is available.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductStatusHandler`


Configuration: `BasketAcceptedItemStatus `

-> ( `OnlineOnly`

| `OnlineOrOffline`

)

Handler indicates an failure if the product to be added has the status *Offline*, but according to configuration only products with status *Online* (`OnlineOnly`

) are allowed to be added to the basket.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductLifeCycleHandler`


Handler checks whether the product reached the end-of-life or last-order-date. In case of expiry one of the dates an error is indicated and the product not added to the basket.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductIntegrityHandler`


The handler verifies that the product fulfills following criteria:

For each of these constraint violated a failure is pointed out and the product not added.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductAccessibilityHandler`


The handler indicates a failure if the product to be added to the basket is not accessible. A product may be inaccessible, e.g., because a catalog view is defined and the product is excluded from this view for a given customer.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.LookupExistingLineItemHandler`


Handler looks for all existing line items in the basket that represents the same product as the one to be added. Handler sets the found line items at the add-to-basket context if the start node parameter `ForceSeparateLineItem`

at the `ProcessBasket-AddProduct`

pipeline has not been set to value equals to `true`

to force creation of a new line item explicitly.

Configuration: `BasketAddProductBehaviour`

-> ( ```
MergeQuantities
```

| `DisallowRepeats`

| `AllowRepeats`

)

Handler determines the add-to-basket behavior based on following values:

`BasketAddProductBehaviour`

.`ForceSeparateLineItem `

setting at the add-to-basket context.`MergeGroup`

setting at the add-to-basket context.Default implementation: `com.intershop.component.basket.orm.internal.handlers.LookupMergeCandidateHandler`


Handler iterates over all line items found by the LookupExistingLineItemHandler and stores the line item which meets of the following conditions:

`MergeGroup`

at the `ProcessBasket-AddProduct`

pipeline has been set to a value that is equal to the one of the existing line item. (An example with different merge group values would be the following case: Four products should be added to the basket, whereas two ones are paid with the default currency and the other two ones are paid with bonus points.)Default implementation: `com.intershop.component.basket.orm.internal.handlers.MaxItemSizeHandler`


Configuration: `BasketMaxItemSize `

-> (n)

Handler indicates a failure if configured value for maximum number of items will be exceeded after the product is added to the basket.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.MaxItemQuantityHandler`


Configuration: `BasketMaxItemQuantity`

-> (n)

Handler indicates a failure if configured value for maximum line item quantity will be exceeded after the product is added to the basket.

Handler chain executes listed post-add-to-basket handlers in the following order:

Default implementation: `com.intershop.component.basket.orm.internal.handlers.LineItemPositionHandler`


Handler calculates the position number in case a new line item has been created.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.AdjustQuantityHandler`


Configuration: `BasketMaxItemQuantity`

-> (n)

Handler adjusts quantity of newly created line item or of existing item with added requested quantity. Quantity is adjusted based on following configuration values and settings:

`BasketMaxItemQuantity `

otherwise.Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductBundleHandler`


Handler creates bundle member entries, if product to be added is a product bundle.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.GiftCardHandler`


Handler adds some Online Gift Card/Certificate (OGC)-related information to the line item, if product to be added represents an OGC.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.WishlistHandler`


Handler sets the wishlist data to the created/merged product line item.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.OrderRequiredAttributesHandler`


Handler adds all order required product attributes to the newly created line item. It uses the `ProductBOOrderRequiredAttributesExtension.getOrderRequiredAttributes()`

.

This extension is aware of following types of order required attributes:

Attributes are now of the type `BusinessObjectAttribute`

. Those attributes will usually be prefixed with `BusinessObjectAttributes#`

.

Because the checkout process does not use BO's everywhere we use an own factory `ExtensibleObjectBasketProductLineItemAttributesExtensionFactory `

and set the prefix to an empty string.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.DefaultShippingMethodHandler`


The Handler sets the default shipping method to newly created line items.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.InitialShipToAddressHandler`


The handler sets the initial ship-to address for a product line item if multiple shipping is allowed. The address is determined by the following lookup order:

If none of these match, the ship-to address will not be set initially.

If multiple shipping is disabled, the ship-to address of the basket will be set to the preferred ship-to address of the basket owner, if this exists and the ship-to address has not been set yet.

Handler chain executes listed pre-aupdate-variation handlers in the following order:

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductVariationHandler`


If the product to be updated specified in the update-variation context is a *Variation Master* then handler tries to retrieve the default variation product. If default variation product exists then this one is set at the update-variation context instead, otherwise handler indicates an failure if no default variation is available.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductIntegrityHandler`


The handler verifies that the product fulfills following criteria:

For each of these constraint violated a failure is pointed out and the variation product is not updated.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductStatusHandler`


Configuration: `BasketAcceptedItemStatus`

-> ( `OnlineOnly`

| `OnlineOrOffline`

)

Handler indicates an failure if the variation product to be updated has the status *Offline*, but according to configuration only products with status *Online* (`OnlineOnly`

) are allowed to be used in the basket.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductAccessibilityHandler`


The handler indicates a failure if the product to be set at the basket line item is not accessible. A product may be inaccessible, e.g., because a catalog view is defined and the product is excluded from this view for a given customer.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.LookupExistingLineItemHandler`


Handler looks for all existing line items in the basket that represents the same product as the one to be updated. Handler sets the found line items at the update-variation context if the start node parameter `ForceSeparateLineItem`

at the `ProcessBasket-UpdateVariation`

pipeline has not been set to value equals to `true`

to force creation of a new line item explicitly.

Configuration: `BasketAddProductBehaviour`

-> ( `MergeQuantities`

| `DisallowRepeats`

| `AllowRepeats`

)

Handler determines the add-to-basket behavior to be considered during the update-variation process based on following values:

`BasketAddProductBehaviour`

.`ForceSeparateLineItem `

setting at the add-to-basket context.`MergeGroup`

setting at the add-to-basket context.Default implementation: `com.intershop.component.basket.orm.internal.handlers.LookupMergeCandidateHandler`


The handler checks at first whether the line item to be updated comply with the conditions:

If the constraints above are satisfied the handler iterates over all line items found by the LookupExistingLineItemHandler and stores the line item which meets of the following conditions:

`MergeGroup`

at the product line item to be updated is set to a value that is equal to the one of the existing line item.Default implementation: `com.intershop.component.basket.orm.internal.handlers.PreUpdateVariationProductBundleHandler`


In case the product to be replaced was a product bundle, the handler iterate over all bundle member entries and collects the products of this bundle. So they can be replaced in the post-update-variation processing by the UpdateVariationProductBundleHandler.

Handler chain executes listed post-update-variation handlers in the following order:

Default implementation: `com.intershop.component.basket.orm.internal.handlers.AdjustQuantityHandler`


Configuration: `BasketMaxItemQuantity`

-> (n)

Handler adjusts quantity of newly created line item or of existing item with added requested quantity. Quantity is adjusted based on following configuration values and settings:

`BasketMaxItemQuantity`

otherwise.Default implementation: `com.intershop.component.basket.orm.internal.handlers.ProductBundleHandler`


In case the replaced product was a product bundle the old bundle members are removed. Then the handler creates bundle member entries, if the new variation product is a product bundle.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.UpdateVariationOrderRequiredAttributesHandler`


Handler removes at first all old order required attributes and then adds all order required product attributes to the newly created line item. It uses the `ProductBOOrderRequiredAttributesExtension.getOrderRequiredAttributes()`

.

This extension is aware of following types of order required attributes:

Attributes are now of the type `BusinessObjectAttribute`

. Those attributes will usually be prefixed with `BusinessObjectAttributes#`

.

Because the checkout process does not use BO's everywhere we use an own factory `ExtensibleObjectBasketProductLineItemAttributesExtensionFactory `

and set the prefix to an empty string.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.GiftOptionsHandler`


In case the replaced product had gifting options or messages it is checked if the new variation product is eligible too. If not the gift options are removed.

Default implementation: `com.intershop.component.basket.orm.internal.handlers.WarrantyHandler`


In case the replaced product had warranty assigned it is checked if the new variation product is eligible for warranties. If not the warranty is removed.

This functionality provides the possibility of merging the content of one basket into another, which is for instance used when a customer starts putting items into his basket and logs then into his account.

Business object layer specific logic is implemented in the `bc_orderprocess`

(pipeline), the `bc_basket`

(BO interfaces) and *bc_basket_orm* cartridges (BO implementations).

ProcessBasket-MergeBaskets

Basic basket creation functionality is done in Java by implementations of `com.intershop.component.basket.capi.BasketBO`

which provide the following two methods:

<T extends Object> MergeBasketResult merge(BasketBO other, Map<String, T> parameters);

When merging the contents of the two baskets the [Add-To-Basket handler chain](https://knowledge.intershop.com#AddToBasket_HandlerChain) is used. The results of the internal add calls are available in the `MergeBasketResult`

.

A basket has to be anonymized in some cases.

This means that following personal data have to be removed from the basket to avoid any kind of abuse, e.g., payment data, or to prevent that another user gets profits only available to the user that created the basket originally:

In customer scenarios there might be additional information that should be removed from a basket presented to a possibly different user. For this reason a handler chain has been introduced on Java level, that can be used to remove custom data.

Every handler has to implement the following interface:

public interface AnonymizeBasketHandler { void anonymize(BasketBO basket); }

@Beta: This feature has been introduced with 7.8. in a @Beta status. It is only used at very specific points at time of 7.8. release.

Validating the basket is necessary at any time during the checkout.

These validations should be done in Java (not in pipelines) so that the basket can easily be validated in REST as well and that the same validation is called whenever you choose to validate. So far, our implementations in pipelines differ, are not flexible, hard to extend, and cannot be directly called from REST.

An extensible Handler Chain solves those problems: Customers can write their one Handlers, it's a single point to call and it can easily be called from REST.

Depending on how far the customer is in the checkout process, different areas of the basket need to be validated. Example: on the shopping cart page, when entering the checkout, only products should be validated, while after the address page, also addresses need to be validated. Those are called scopes. Scopes right now are defined by a String: "Value" is the scope Value, meaning all handlers based on basket value are executed, like the `MinItemValueValidationHandler`

. Keeping it that simple has the advantage of easy extensibility - by just calling the validate methods with a different string, another scope exists and can be used in the handlers.

| Term | Description |
|---|---|
| Scopes | Basket Validation needs to validate different objects of the basket at different times/stages of the checkout. To distinguish those stages, a SCOPE or several SCOPES need to be defined for validation. Example: On the shopping cart page, when entering the checkout, only products (scope ) should be validated, while after the address page, also addresses (scope Products ) need to be validated.Addresses |

(can be set directly via `BasketValidationRecord`

or via pipeline node `ValidateBasket`

)

| Parameter | Default Value | Possible Values | Description |
|---|---|---|---|
| stopOnError | False | NeverStop | Always finish validation (default) |
| StopOnError | Stop as soon as an error occurs | ||
StopOnErrorFinishScope | Stop when an error occurs but finish the scope the error occurred in | ||
| allowAdjustments | True | True | Adjustments are allowed during validation, like removing a PLI in case of missing inventory or trying to set a preferred address if address is missing |
| False | No adjustments are allowed during validation, errors are collected but not corrected |

| Scope | What for | Current Handlers | Default Priority |
|---|---|---|---|
| Products | Product availability, available prices etc | `ProductAccessibilityHandler` | 140 |
`ProductIntegrityHandler` (replaces `ProcessBasket-RemoveLineItemsWithoutPrice` ) | 135 | ||
`ProductInventoryHandler` (replaces `ProcessBasket-AdjustBasketByInventoryStatus` ) | 130 | ||
`ProductLifeCycleHandler` | 125 | ||
| 105 | ||
`MaxItemQuantityHandler` | 95 | ||
| Addresses | Validators that validate existence and/or validity of addresses | `ShipToAddressValidationHandler` (replaces `ProcessCheckoutAddresses-DefaultSettings` ) | 120 |
`InvoiceToAddressValidationHandler` (replaces `ProcessCheckoutAddresses-DefaultSettings` ) | 121 | ||
`AddressChangeCalculationValidationHandler` | 122 | ||
`EligibleShippingMethodsHandler` | 115 | ||
| 110 | ||
| Payment | Payment related validation like is payment available, is basket covered etc., gift-card validation |
| 160 |
`BasketAmountCoveredValidationHandler` (replaces `ViewCheckout-CheckPayment` and `ViewCheckoutReview-CheckPayment` ) | 155 | ||
| Value | Are min and max values not exceeded |
| 175 |
`MaxItemValueValidationHandler` (replaces `ViewCart-IsMaxOrderAmountExceeded` and `ViewCheckoutReview-IsMaxOrderAmountExceeded` ) | 170 | ||
| Shipping | Are shipping methods set and eligible |
Since 7.10 replaced by | 145 |
| 100 | ||
| (empty String) no scope | All validators that should always be executed |
| 195 |
`EmptyBasketValidationHandler` | 190 | ||
`MaxItemSizeHandler` | 185 | ||
| RecurringOrder | Validators specially for validating a recurring basket | `RecurringOrderDateValidationHandler` | 165 |
| CostCenter | Validators that check the correctness of cost center specific data | `CostCenterValidationHandler` | 150 |
| Order | Final order scope |
| 200 |
`TaxServiceAvailableValidationHandler` (replaces `ViewCheckoutReview-CheckBasketContinueCheckoutIfTaxServiceUnavailable` ) | 180 | ||
| Promotion | Validators that check explicit promotions (with promotion code) and all related aspects (code groups, user group assignment etc.) | `BasketValidationPromotionHandler (` replaces` ProcessPromotionCodeForBasket-ValidatePromotion, ` | 210 |
| All | All scopes should be checked | ALL registered handlers are invoked in order of their priority (highest first) | - |

Since the `BasketValidationResult`

is very generic, there was a need for some special parameters. Those are and can be set directly in the handlers.

| Parameter Name | Class | Description |
|---|---|---|
| parameter0 and parameter1 | String | Can be used to hand parameters to the SF message for the failure code. |
| AdjustBasketResult | AdjustBasketResult | Can be used to show details about Product Adjustments in SF |
| RemoveFromBasketResult | RemoveFromBasketResult | Can be used to show details about Product Removals in SF |

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.