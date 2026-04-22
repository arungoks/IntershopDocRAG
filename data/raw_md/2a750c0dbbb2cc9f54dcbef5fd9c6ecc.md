---
id: '2a750c0dbbb2cc9f54dcbef5fd9c6ecc'
title: 'Concept'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2G8047'
scraped_at: '2026-04-21T05:37:16.916697+00:00'
---
The JavaScript class `ishHbsController`

was introduced to ease working with the [Handlebars Template Engine](http://handlebarsjs.com/).

Initialize the controller and precompile the handlebars template

**Description:**

Initialize the Handlebars controller and precompile the handlebars template for rendering.

The complete initialization process will be triggered by the ISML module *ishbs.*

Therefore the `init()`

method is not needed to be called by the developer.

**Parameter List:**

**Returns**

**Example**

/* Example for the template snippet in any ISML template: <script id="SubscriptionsList" type="text/x-handlebars-template"> <h3>{{title}}</h3> </script> */ SubscriptionsListController = new ishHbsController('SubscriptionsList'); SubscriptionsListController.init(); SubscriptionsListController.controller(function() { // ... custom controller code });

Set the internal debug parameter

**Description:**

An internal debugging parameter will be set to `true`

.

So the developer will see at console output which controller will be executed.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

SubscriptionsListController = new ishHbsController('SubscriptionsList'); SubscriptionsListController.debug(); SubscriptionsListController.init(); SubscriptionsListController.controller(function() { // ... custom controller code });

var controller = this; controller .debug() .model({ ... }) .update();

Update the model data

**Description:**

Update the model data.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

SubscriptionsListController = new ishHbsController('SubscriptionsList'); SubscriptionsListController.init(); SubscriptionsListController.model({ "title": "...", "subtitle": ".................." });

Update the precompiled Handlebars template

**Description:**

Update the precompiled Handlebars template with the current model.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

SubscriptionsListController.update();

Customized user controller code for the current Handlebars controller instance

**Description:**

Set the customized user controller handler code for the current Handlebars controller instance and execute the handler.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

SubscriptionsListController.controller(function() { // ... custom controller code });

Customized user methods for the current Handlebars controller instance

**Description:**

Extends the current controller instance with customized user methods.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

SubscriptionsListController.extend({ method1: function() { }, method2: function() { } });

Method to filter the current model data

**Description:**

This method helps to filter the current model elements data by a specific filter handler.

The original model data will not be touched.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

// Example for a filter handler to filter all items where the string "Max" is found on the name value subscriptionsListController.filterElements(function(item) { if (item.name.toLowerCase().indexOf('Max') != -1) { return true; }else{ return false; } }); // Example to remove the current filter and use the original model data subscriptionsListController.filterElements(false);

Getter and setter for the currently filtered model data

**Description:**

This method updates the current filtered model data.

The original model data will not be touched.

The method is chainable.

**Parameter List:**

**Returns**

**Example**

// Example for a filter handler to filter all items where the string "Max" is found on the name value subscriptionsListController.filteredModel({ "title": "...", "subtitle": ".................." });

* *

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.