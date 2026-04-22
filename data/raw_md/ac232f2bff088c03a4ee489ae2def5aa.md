---
id: 'ac232f2bff088c03a4ee489ae2def5aa'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/28G633'
scraped_at: '2026-04-21T05:41:35.307165+00:00'
---
To support different databases alternative BasicSeriesGenerators to handle database specific sequence are required.

The *BasicSeriesGenerator* is no longer instantiated by calling its constructor. Now an instance of type *BasicSeriesGenerator* is created by calling the method of the corresponding *BasicSeriesGeneratorFactory*.

import com.google.inject.Inject; import com.intershop.beehive.core.capi.series.BasicSeriesGenerator; import com.intershop.beehive.core.capi.series.BasicSeriesGeneratorFactory; public class BasicSeriesGeneratorTest { @Inject private BasicSeriesGeneratorFactory generatorFactory; private BasicSeriesGenerator obtainSeriesGenerator(String identifier) { BasicSeriesGenerator generator = null; // ... if (generator == null) { generator = generatorFactory.createGenerator(identifier); } return generator; } }

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.