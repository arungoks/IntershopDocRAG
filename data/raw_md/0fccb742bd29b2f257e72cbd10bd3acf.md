---
id: '0fccb742bd29b2f257e72cbd10bd3acf'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/U25993'
scraped_at: '2026-04-21T05:41:55.485872+00:00'
---
This guide describes conventions and rules how business objects and supporting infrastructure for the new BO layer must be implemented. The conventions are mandatory, any violations will be treated as bugs. Existing code that does not comply with the conventions must be reworked.

For more information about the concept and an explanation of the used terms in this document, see the related documents:

Depending on the importance of the business object to be implemented, it may be required to create a whole new cartridge. For example, the basket aggregate could be implemented in its own cartridge *bc_basket*, and the address aggregate could be implemented in the *bc_address* cartridge, which will also contain all additional things related to the business object, like address validation code and pipelets. Whether or not a new cartridge is needed must be decided from case to case. The recommendation is to create a separate cartridge for every important concept.

It is recommended to separate between the business object API and the (possibly multiple different) business object implementation. Thus we need two kinds of cartridges: API cartridges and implementation cartridges.

A cartridge containing only business object APIs has the name "bc_*". It may contain:

**Example:**

A cartridge containing business object implementations has a name that extends the name of the API cartridge which is implemented by an additional identifier that gives a hint about the underlying implementation technology. For example, cartridges for business objects that are implemented using ORM objects should be called "bc_*_orm".

A cartridge containing business object implementations may contain:

**Example:**

The repository is the central entry point for creating or retrieving the root entity (e.g., the root business object) of an aggregate. It hides the underlying implementation.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObjectRepository`

.`java.util.Collection`

or similar (List, Set, Map), but do not work with Iterators in the interfaces.The methods of the repository contain the name of the business object, including the BO:

**Example:**

package com.intershop.component.basket.capi; import com.intershop.beehive.businessobject.capi.BusinessObjectRepository; public interface BasketBORepository extends BusinessObjectRepository { public BasketBO createBasketBO(String id); public BasketBO getBasketBOByID(String id); public Collection<BasketBO> getExpiredBasketBOs(); public void deleteBasketBO(String id); }

The repository implementation implements the repository interface and maps it to an underlying (persistence) technology. There can be multiple alternate implementations for the same repository interface. It may internally rely on other subsystems, like the ORM engine, or can solve everything on its own.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObjectRepository`

)`ORM...RepositoryImpl`

for repositories operating on underlying ORM objects.**Example:**

package com.intershop.component.basket.orm.internal; import com.intershop.component.basket.capi.BasketBO; import com.intershop.component.basket.capi.BasketBORepository; public class ORMBasketBORepositoryImpl implements BasketBORepository { @Override public BasketBO createBasketBO(String id) { ...//create BO and invokes its objectCreated-method } @Override public BasketBO getBasketBOByID(String id) { ... } @Override public Collection<BasketBO> getExpiredBasketBOs() { ... } @Override public void deleteBasketBO(String id) { ... //look up the BO and invokes its delete-method } }

The business object interfaces represent the actual business objects. The root entity provides methods for controlling the lifecycle of dependent entities. The entities provide methods for accessing their attributes, for navigation and for processing business operations, resulting in a modification of their structure. All entities completely hide their internal implementation. There may be different backend implementations for them, thus the API may not expose any implementation details. In particular, it may not directly return underlying ORM objects, because this would make an alternative implementation of this BO interface impossible which does not rely on ORM.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObject`

(directly or indirectly).`java.util.Collection`

or similar (list, set, map), but do not work with Iterators in the interfaces.**Example:**

package com.intershop.component.basket.capi; public interface BasketBO extends BusinessObject { public BasketProductLineItemBO addProduct(ProductRef ref, Quantity amount, Money price); public Collection<BasketProductLineItemBO> getProductLineItemBOs(); }

The business object implementation implements the business object interface and maps it to the internal representation. There can be multiple alternate implementations for the same business object interface.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObject`

).`com.intershop.beehive.core.capi.domain.AbstractExtensibleObjectBO`

for BO impls that internally use an ExtensibleObject as delegate.`com.intershop.beehive.core.capi.domain.AbstractPersistentObjectBO`

for BO impls that internally use a PersistentObject as delegate.`com.intershop.beehive.businessobject.capi.AbstractBusinessObject`

for all other BO impls.**Example:**

package com.intershop.component.basket.orm.internal; import com.intershop.component.basket.capi.BasketBO; import com.intershop.component.basket.capi.BasketBORepository; import com.intershop.beehive.core.capi.domain.AbstractExtensibleObjectBO; public class ORMBasketBOImpl extends AbstractExtensibleObjectBO implements BasketBO { @Override public BasketProductLineItemBO addProduct(ProductRef ref, Quantity amount, Money price) { ... } @Override public Collection<BasketProductLineItemBO> getProductLineItemBOs() { ... } @Override public void delete() { super.delete(); //trigger the hooks ... //do some clean up (e.g., deletes affected ORM objects) } }

Existing business objects can be enhanced in customer projects and / or in other application layers (like the presentation layer) by attaching extensions to them.

The conventions for allowed arguments / return values for extensions are not as strict as for business object interfaces, as extensions represent optional features only. There are rarely multiple implementations of the same extension interface.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObjectExtension`

.`getExtension`

method at the BO).**Example:**

import com.intershop.beehive.businessobject.capi.BusinessObjectExtension; /** * This extension covers all applied rebate related functionality for the basket * business object. */ public interface BasketBOAppliedRebateExtension extends BusinessObjectExtension<BasketBO> { /** * The ID of the created extensions which can be used to get them from the * business object later. */ public static final String EXTENSION_ID = "AppliedRebate"; /** * Returns all dynamic messages describing the promotions to gather, when * fulfilling the noted condition. * * @param locale the locale to return them for * @return the collection of dynamic messages */ public Collection<String> getComputedDynamicMessageDiscountItems(Locale locale); }

package com.intershop.component.basket.capi; import com.intershop.beehive.businessobject.capi.BusinessObjectExtension; import com.intershop.component.repository.capi.RepositoryBO; /** * This extension adapts a RepositoryBO to act as a basket repository. */ public interface RepositoryBOBasketExtension extends BusinessObjectExtension<RepositoryBO>, BasketBORepository { /** * The ID of the created extensions which can be used to get them from the * business object later. */ public static final String EXTENSION_ID = "BasketBORepository"; }

For a logical and consistent naming scheme the EXTENSION_IDs should be named as follows:

**Rules:**

For the extension interface, there must be an extension implementation.

**Rules:**

`com.intershop.beehive.businessobject.capi.AbstractBusinessObjectExtension`

and must implement the extension interface.**Example:**

import com.intershop.beehive.businessobject.capi.AbstractBusinessObjectExtension; /** * This extension covers all applied rebate related functionality for the basket * business object. */ public class BasketBOAppliedRebateExtensionImpl extends AbstractBusinessObjectExtension<BasketBO> implements BasketBOAppliedRebateExtension { ... }

Extension factories are responsible to create instances of business object extension implementation classes.

**Rules:**

`com.intershop.beehive.businessobject.capi.BusinessObjectExtensionFactory`

.`com.intershop.beehive.businessobject.capi.AbstractBusinessObjectExtensionFactory`

instead, which already implements some of the required interface methods.**Example:**

import com.intershop.beehive.businessobject.capi.AbstractBusinessObjectExtensionFactory; /** * Factory for the specific implementation of the applied rebate extension for the basket * business object. */ public class BasketBOAppliedRebateExtensionFactory extends AbstractBusinessObjectExtensionFactory<BasketBO> { @Override public BusinessObjectExtension<BasketBO> createExtension(BasketBO object) { return new BasketBOAppliedRebateExtensionImpl(BasketBOAppliedRebateExtension.EXTENSION_ID, object); } @Override public Class<BasketBO> getExtendedType() { return BasketBO.class; } @Override public Class<BasketBOAppliedRebateExtension> getExtensionType() { return BasketBOAppliedRebateExtension.class; } }

Pipelets are the main building blocks for setting up business processes. Therefore, it is essential to use a consistent naming scheme for pipelets that allows customers as well as developers to guess the purpose of a pipelet based on its name only.

The naming convention outlined here is by no means complete. There will always be pipelets that do not fall into the categories defined here. The focus of the naming scheme is to provide guidance for the famous 80% of all cases.

Creates a new instance of the business object in business object repository based on some sort of identification criteria (semantic key) retrieved from the pipeline dictionary. This pipelet should focus on object creation with the primary key attributes and other mandatory attributes. The pipelet should not take care of completely configuring the business object with all optional parameters. This should be done by a following update pipelet.

Dictionary In: *Business Object Repository, Semantic Key Attributes*

Dictionary Out: *Business Object*

Error Exit: *Yes, if product can not be created*

Transaction Mode: *Required*

Example: *CreateProductBO*

Deletes a business object instance from the business object repository. The business object to be deleted should be retrieved directly from the pipeline dictionary. Remove pipelets should not contain any lookup logic for looking up the objects to be removed. Remove pipelets remove a single business object instance only (no iterators).

Dictionary In: *Business Object*

Error Exit: *No, errors that might come up when deleting the object should be gracefully ignored*

Transaction Mode: *Required*

Example: *DeleteProductBO*

Udates a business object instance (available in the pipeline dictionary) with some new attributes (available in the pipeline dictionary). This pipelet should not have an error connector and should gracefully ignore errors that might come up when updating the object attributes.

Dictionary In: *Business Object, Attribute(s)*

Error Exit: *No, errors that might come up when updating the object attributes should be gracefully ignored*

Transaction Mode: *Required*

Example: *UpdateProductBO*

Tries to identify a single business object instance within the business object repository based on its semantic key.

Dictionary In: *Business Object Repository, Semantic Key*

Dictionary Out: *Business Object*

Error Exit: *Yes, if the requested business object could not be found*

Transaction Mode: *Optional*

Example: *GetProductBOByID*

Tries to identify a single business object instance based on some attribute(s) (not the semantic key). The identifying attribute(s) are retrieved from the pipeline dictionary.

Dictionary In: *Business Object Repository, Attribute(s)*

Dictionary Out: *Business Object*

Error Exit: *Yes, if the requested business object could not be found*

Transaction Mode: *Optional*

Example: *GetProductBOBySKU*

Same concept as the pipelet above. The only difference is that here another, usually associated, business object is used for the lookup.

Dictionary In: *Business Object Repository, (Business) Object*

Dictionary Out: *Business Object*

Error Exit: *Yes, if the requested business object could not be found*

Transaction Mode: *Optional*

Example: *GetCatalogBOByCatalogCategoryBO*

Tries to identify a collection of business objects based on some attribute (that is not the semantic key). The identifying attribute(s) are retrieved from the pipeline dictionary. This pipelet is important whenever list of business objects need to be processed (e.g., all departments of an organization).

Dictionary In: *Business Object Repository, Attribute(s)*

Dictionary Out: *Collection <Business Object>*

Error Exit: *No, instead an empty collection is stored in the pipeline dictionary in case of errors or empty result sets*

Transaction Mode: *Optional*

Example: *GetProductBOsBySKU*

Same concept as the pipelet above. The only difference is that here another, usually associated, business object is used for the lookup.

Dictionary In: *Business Object Repository, (Business) Object*

Dictionary Out: *Collection <Business Object>*

Error Exit: *No, instead an empty collection is stored in the pipeline dictionary in case of errors or empty result sets*

Transaction Mode: *Optional*

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.