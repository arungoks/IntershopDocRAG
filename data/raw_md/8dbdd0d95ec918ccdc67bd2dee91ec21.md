---
id: '8dbdd0d95ec918ccdc67bd2dee91ec21'
title: 'Reference'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2481U7'
scraped_at: '2026-04-21T05:41:54.847053+00:00'
---
The component framework uses XML declarations of contracts, implementations and instances. Related documents are the [concept](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1754628482) and [cookbook](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1768456407/Cookbook+-+Component+Framework) of the component framework.

`<COMPONENTS>`

tag is the body tag for component definitions.<?xml version="1.0" encoding="UTF-8"?> <components xmlns="http://www.intershop.de/component/2010"/>

`scope`

This attribute is optional.

The attribute scope defines a default scope to instantiate contained instances. Currently available are *app* and *global*.

<components scope="global|app" />

Note

If no scope is defined within the instance definition, the component framework applies the default value `global`

.

Note

The provided interface should declare what the instance is doing. It should not declare what is needed to fulfill this functionality.

The `<CONTRACT>`

tag allows to define a component contract.

Note

Currently, only JAVA interfaces are supported.

<?xml version="1.0" encoding="UTF-8"?> <components xmlns="http://www.intershop.de/component/2010"> <contract name="[name]" class="[classname]"/> </components>

`name`

This attribute is required.

`class`

This attribute is required.

`<IMPLEMENTATION>`

tag allows to define an implementation of a contract.<?xml version="1.0" encoding="UTF-8"?> <components xmlns="http://www.intershop.de/component/2010"> <implementation name="[name]" implements="[contract-name]" factory="[factory-name]" class="[class-name]" start="nameOfStartMethod" stop="nameOfStopMethod"> <!-- multiple implements can be listed --> <implements contract="[contract-name]" /> <requires name="[property-name]" contract="[contract-name]" cardinality="[1..1|0..1|1..n|0..n]" /> </implementation> </components>

`name`

This attribute is required.

`factory`

This attribute is optional.

`JavaBeanFactory`

)`implements`

This attribute is required.

`class`

This attribute is optional when using a factory which already have the `class`

attribute. When using the `JavaBeanFactory`

the attribute is required.

`start`

This attribute is optional.

`stop`

This attribute is optional.

`<REQUIRES>`

tag allows to define the requirements of the implementation.`<REQUIRES>`

tag is a child element of the `<IMPLEMENTATION>`

tag. For a syntax example see syntax of `name`

This tag is required.

`contract`

This tag is required.

`cardinality`

This tag is optional (default: 1..1).

`<IMPLEMENTS>`

tag allows to define the names of additional implemented contracts (extension to the attribute implements of `<IMPLEMENTATION>`

tag).`<IMPLEMENTS>`

tag is a child element of the `<IMPLEMENTATION>`

tag. For a syntax example see syntax of `contract`

This attribute is required.

`<INSTANCE>`

tag allows to define a component configuration for a component instance.<?xml version="1.0" encoding="UTF-8"?> <components xmlns="http://www.intershop.de/component/2010"> <!-- an instance for an implementation without requirements --> <instance name="[name]" with="[implementation-name]" /> <!-- an instance for an implementation with directly fulfilled requirements --> <instance name="[name]" with="[implementation-name]"> <!-- fulfill the requirement with a constant --> <fulfill requirement="[property-name]" value="[constant]"/> <!-- fulfill the requirement with another instance --> <fulfill requirement="[property-name]" with="[instance-name]" /> </instance> <!-- outside of instance tag --> <fulfill requirement="[property-name]" of="[instance-name]" with="[instance-name]" /> <fulfill requirement="[property-name]" of="[instance-name]" value="[constant]" /> <!-- instance inside of fulfill tag --> <instance name="[name]" with="[implementation-name]"> <!-- with attribute of fulfill tag is implicit - filled with inner instance element(s) --> <fulfill requirement="[property-name]"> <!-- name of instance is optional - anonymous instances are allowed here --> <instance with="[implementation-name] requirement="[property-name]" with="[instance-name]" /> </instance> <!-- recursive declaration of instances and fulfillment --> <instance with="[implementation-name]"> <fulfill requirement="[property-name]"> <instance with="[implementation-name]" /> </fulfill> </instance> </fulfill> </instance> <!-- replace an instance with a new one, the old is available via the name - value of delegate attribute --> <replace name="[name]" with="[implementation-name]" delegate="[renamed-instance-name]"> <fulfill requirement="[delegate-property-name]" with="[renamed-instance-name]" /> <!-- other fulfill tags ... --> </replace> </components>

`name`

This attribute is optional.

Note

If you use `<INSTANCE>`

tag as a child element of `<COMPONENTS>`

tag, the `name`

attribute is required for wiring.

It is recommended to use anonymous instances if you do not need the instance twice for wiring.

`with`

This attribute is required.

`scope`

This attribute is optional.

The attribute scope defines the context in which an instance is created. So it is possible to create different instances for different applications.

<instance name="[aName]" with="[anImplementation]" scope="global|app" />

Note

If no `scope`

is defined within the instance definition, the component framework applies the value set in the [ components](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1775993923/XML+Definition+-+COMPONENTS) tag. If the

`components`

`global`

.`global`

A single instance of the implementation is created. The instance is available from all applications.

`app`

The framework creates an instance of the implementation for each application. An instance is created exclusively for the current application and cannot be accessed by any other application.

`<FULFILL>`

tag allows to define the wiring or simple configuration of the component instance.`<FULFILL>`

tag can be used both as a child element of `<INSTANCE>`

tag and outside as a child element of the `<COMPONENTS>`

tag.`<INSTANCE>`

`requirement`

This attribute is required.

`of`

One attribute out of `with`

, `of`

or `value`

is mandatory.

`with`

One attribute out of `with`

, `of`

or `value`

is mandatory.

`value`

One attribute out of `with`

, `of`

or `value`

is mandatory.

`<REPLACE>`

tag allows to define replacement of an existing instance.`<INSTANCE>`

.`name`

This attribute is required.

`<INSTANCE>`

tag)`with`

This attribute is required.

`<INSTANCE>`

tag)`delegate`

This attribute is required.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.