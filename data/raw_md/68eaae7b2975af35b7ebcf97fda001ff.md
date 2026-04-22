---
id: '68eaae7b2975af35b7ebcf97fda001ff'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/235F47'
scraped_at: '2026-04-21T05:39:44.647489+00:00'
---
As business objects become increasingly complex, it is necessary to inform shop managers about invalid or incomplete objects that would result in a bad user experience of the storefront. The first steps taken into this direction include the introduction of the shop statistics feature and the enhancement of the advanced product and content search. The provided solution relies on the assumption that a validation for an object can be completely implemented via SQL queries, but, especially in regard to newer content management features, this approach is no longer sufficient.

A new framework has been introduced that is able to validate any business object according to rules of any complexity. The rules can be executed asynchronously, and the results may be stored persistently so that the shop managers can easily look into and fix the detected issues. This feature can also be used to give the back office user immediate feedback when editing single business objects.

This concept only describes the generic object validation framework. How the framework is applied for validating concrete business objects such as content pages or includes or how validation results are brought to and displayed in the back office will be covered in the concept documents for the specific business objects.

Please also have a look at the related cookbook for related common questions: * Cookbook - Object Validation *.

BO | Business Object (see |
PO | Persistent Object |
VR | Validation Result |
VRBO | Validation Result BO |
VRBORepo | VRBO Repository |
VRPO | Validation Result PO |

The framework provides:

The diagram above shows all programming artifacts involved in object validation and their relations and dependencies. The red object is the object that is validated. The blue rectangles mark implementations provided by the framework. The green rectangles mark interfaces provided by the framework that need to be implemented in the different tracks (e.g., for content validation). Continuous lines mean that one component uses a function of another component, dashed lines mean that one component has another component as a member variable or at least parts of it (like that rule ID of a validation rule).

To validate an object, the object validator needs to know the validation rule set provider that will return a number of specific validation rule factories. Each of these factories is able to create one specific validation rule. The validation context given to the object validator is injected into the rules, so that they have a specific context for which to run.

Each rule provides a number of validation results. These can be passed on to the validation BO repository to create validation BOs and, if requested, to persist the results using a validation result persistence factory.

The validation result business object repository (VRBORepo) is the central point of this feature. It (directly or indirectly) uses all components described below.

The VRBORepo is responsible for the following tasks:

The repository is able to create persistent and transient validation result BOs. The transient BOs can be used to validate an object and to display the validation results if there is no need to have the results persisted - e.g., at the end of a *manual* business object update performed by a shop manager. The transient BO cannot be retrieved again from the repository, a request for the BO with the ID of the transient BO will result in `null`

.

The VRBORepo will be wired at the *business object repository* using the component framework. An extension factory is provided that is able to create one repository per business object. This factory needs to be enhanced with two things:

The implementations of these factories need to be wired using the component framework. But they need to be provided by each business track (like content or product). However, on creation of a VRPORepo, the repository will get these from its factory and afterwards can use them either to return rule factories for specific objects or to create persistent validation results.

As there is a deletion propagation mechanism (see below) to remove validation result POs if the validated object is removed, there is no way to directly remove any validation result BO by the repository. But there is a feature implemented that allows for removing outdated validation results when, for example, performing a new object validation. To this end, the VRBORepo provides functions that will use the validated object, the (optional) rules for which the object was previously validated and a (optional) context for which the previous validation was executed - that is, all information one usually has when a validation process is currently running. So you can use it to remove an outdated result and create an updated one.

The validation result BO repository implementation is also registered as an object mapper. This concept allows you to use the query framework to retrieve queries that will return BOs in their result sets. The repository implementation is used to look up the VRBOs, and to find objects, an identifier class has been created: `ValidationResultBOIdentifier`

. The following snippet demonstrates the potential usage:

<return-mappings> <return-mapping name="ValidationResultBO" type="bo-constructor" class="com.intershop.component.validation.capi.orm.ValidationResultBOIdentifier" mapperclass="ValidationResultPOToValidationResultBOMapper"> <return-attribute name="uuid"/> <return-attribute name="factoryname" /> </return-mapping> </return-mappings>

The validation result persistence factory interface defines methods to persist any incoming validation result. It creates validation result persistence objects that will be stored in the data base.

The interface should be implemented by any track (e.g., content or product) for its needs. To simplify the implementation of the VRPO, an abstract class ( `com.intershop.component.validation.capi.orm.AbstractValidationResultPO<T>`

) is provided from which other objects should inherit. The abstract implementation is defined in its own EDL file from which the concrete implementations should inherit. This class implements the common methods of the validation result interface.

orm class MyValidationResultPO extends AbstractValidationResultPO table "MyValidationResult_VR" { }

The factory interface defines the `isApplicable()`

method, which tells the caller whether the factory is able to persist the given business object (e.g., a content component). Or, clearly said, whether the factory is able to persist the relation(s) between the (to be) created VRPO and the given business object, as usually a business component does not need to be persisted by the factory (usually other factories handle the persistence of the business objects).

There is also an abstract implementation of the factory interface: `com.intershop.component.validation.capi.orm.AbstractValidationResultPersistenceFactory<T extends ORMObject>`

. This implementation mainly helps by providing filter methods for `getValidationResultPOsByOwner(T owner)`

using `com.google.common.base.Predicate`

s.

A deletion propagation mechanism has been implemented that will delete all persistent validation results for you if the validated object was deleted. To automatically delete the created validation result POs, they need to inherit from `AbstractValidationResultPO`

. While the server is started and the *bc_validation* cartridge is loaded, this deletion propagation mechanism is loaded and all validation result POs with their owner POs will be collected and registered.

The validation context holds the scope that should be checked by the rules. This means, for example, for a localized object, you can define that the rule should only check values for certain locales, or if a constraint is fulfilled for a given time frame.

Additionally the validation context can also hold variables the rule needs for rule evaluations, e.g., some domains/repositories/preferences that might be needed in evaluation of object relations.

The information is made up of:

If none of this information is set, these values do not need to be taken into account by the rule execution.

A validation rule is the class that performs the object validation. It returns a list of results (not one) depending on the context. If the context defines, for example, a list of locales the object should be checked for, the rule needs to return one result per locale. To execute the rule, the function `validate(Object)`

has to be used.

The rules will be created by a rule factory that also has to inject the context into the created rule. One factory will only create one specific rule, but the context of the rules can differ. That means you can use the same factory two times with different contexts, and you will get the same rule but with different contexts. The factory also decides whether it is able to handle a specific business object. To this end, the function `isApplicable(Object)`

must be used. As a rule factory only creates one single rule, the factory has knowledge about the rule ID of the rule it will create. The factory returns this ID using `getRuleID()`

.

The validation rule set provider is a container for validation rule factories. Whenever an object is validated, also a rule set provider must be given that defines the actual factories according to the object that is validated. There are currently two implementations for the `ValidationRuleSetProvider`

interface that are both designed to be configured with rules via the component framework:

The validation result business object repository (that is used as a default at some places, if no specific provider is given)

<fulfill of="ValidationResultBORepositoryExtensionFactory" requirement="validationRuleFactory" with="example.validation.rule.CategoryDisplayNames"/>

A generic container for rule factories

<instance name="example.CategoryValidation.RuleSet" with="ValidationRuleSetProvider"> <fulfill requirement="validationRuleFactory"> <instance with="example.validation.rule.CategoryDisplayNames"/> </fulfill> </instance>

The validation result is the object that holds any relevant information about the output of the execution of a validation rule. The values are:

The result itself is a transient object, which can be persisted using a validation result persistence factory. Almost all values of the result are only readable, as they do not need to be changed afterwards. Only message key, message parameter and meta information can be changed once a result is created.

A validation result business object provides the business object view on the result.

Meta information comes into play when a client wants store additional data along with a VR produced by a rule. For whatever reason such data will exist is entirely up to the client. The client in such cases can either be the rule itself or the responsible validation result persistence factory.

Suppose a validation rule for a page variant (i.e., a pagelet) wants to store the author of the object, but there is no place inside `ValidationResult`

. Therefore the rule just needs to add the author as meta data `putMetaData(String name, Object object)`

. Along with the validation result persistence factory, the created persistent object receives the VR object (incl. meta data). If the persistent object is extending from the ORM abstract layer (i.e., `AbstractValidationResultPO`

), then it will automatically benefit from the built-in JAXB value serializing mechanism. All that the validation result persistence factory needs to do is to call `public final void applyValidationResult(ValidationResult<T> result)`

with the given VR object.

Meta data types

Simple meta data types, such as `Integer`

, `String`

, `Date`

, etc., can be used without further administration effort. All other classes (like the author from the above example) must be registered so that a VR value containing meta-data values can be processed as an XML value. Registration is done automatically from the factory default implementation of VRBORepo. That means, when registering a `ValidationRuleFactory`

(this step is always necessary, see the sections above) on the VRBO repository factory, meta-data types returned by `ValidationRuleFactory.getMetaDataTypes()`

will be registered subsequently. Any custom VRBO repository factory **must** stick to this behavior. There is the class `TypeRegistry`

in the capi package of `bc_validation`

that allows a custom repository to fulfill this contract.

The object validator is the class that uses a rule set provider and a context to validate the given object. For any validation you need to instantiate a new object validator that will be initialized with one rule set provider and one context. Based on the given object, the object validator asks the rule set provider for a set of rule factories. The context then will be taken to create rules from these factories. After that, all created rules will be executed, and the results will be collected and returned to the caller.

To actually perform object validation, two pipelets are provided: **ValidateObject** and **ValidateObjects**. They validate single objects or many objects in parallel running threads.

The `bc_validation`

cartridge provides a listener mechanism that allows to trigger a validation if any ORM object has been changed by a database transaction. This allows to keep validation results always consistent without the need of plug in pipelets in a possibly large amount set of pipelines responsible for a certain business object.

The main features are:

`bc_validation`

provides a global object `ORMValidator`

.`ORMValidator`

can be filled with any number of (different) validation configurations.Basically, the process for a single configuration is a follows:

<fulfill requirement="configuration" of="ORMValidator"> <instance with="ORMValidatorApplicationTypeConfigurationAssignment"> <!-- <fulfill requirement="app" with="intershop.EnterpriseBackoffice" /> --> <!-- keep the configuration in sync with configurations used in the pipelines --> <fulfill requirement="configuration"> <instance with="ORMValidatorConfiguration" scope="global"> <fulfill requirement="validationResultBORepositoryName" value="ValidationResultBORepository"/> <!-- <fulfill requirement="validationRuleSetProviderName" value="..."/> --> <!-- <fulfill requirement="validationContextProviderName" value="..."/> --> <fulfill requirement="storeMode" value="invalid"/> <fulfill requirement="removeMode" value="all"/> <fulfill requirement="objectListener"> <instance with="ORMValidator.StandardListener"> <fulfill requirement="factoryName" value="com.intershop.component.pmc.internal.pagelet.PageletPO"/> <fulfill requirement="factoryName" value="com.intershop.component.pmc.internal.pagelet.SlotPO"/> </instance> </fulfill> <fulfill requirement="immediateValidationHandler"> <instance with="ORMValidator.DirectValidationHandler"> <fulfill requirement="factoryName" value="com.intershop.component.pmc.internal.pagelet.PageletPO"/> </instance> </fulfill> <fulfill requirement="delayedValidationHandler"> <instance with="ORMValidator.DirectValidationHandler"> <fulfill requirement="factoryName" value="com.intershop.component.pmc.internal.pagelet.SlotPO"/> </instance> </fulfill> <!-- <fulfill requirement="contextFilter" > <instance with="..."/> </fulfill> --> </instance> </fulfill> </instance> </fulfill>

**ORMValidator.StandardListener**

Defines for which objects is listened by simple declaring the according ORM factory names. If an event occurs normally, the listened object is returned for being validated. Only if it is an attribute value PO, the owner objects is returned for validation.

**ORMValidator.DirectValidationHandler**

This validation handler actually does nothing other than filtering. This means, it returns the given PO as the (BO) object for validation. The filtering is needed if different PO types need another handling.

The threads for the delayed validation can be configured:

intershop.ORMValidator.DelayedValidation.TaskQueue.size = 1000 intershop.ORMValidator.DelayedValidation.Thread.count = 1

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.