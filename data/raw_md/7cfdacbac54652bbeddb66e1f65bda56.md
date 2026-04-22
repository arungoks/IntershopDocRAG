---
id: '7cfdacbac54652bbeddb66e1f65bda56'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/299V06'
scraped_at: '2026-04-21T05:40:24.319331+00:00'
---
Projects have to update their dependencies:

<dependency> <groupId>org.wildfly.bom</groupId> <artifactId>wildfly-jakartaee8-with-tools</artifactId> <scope>import</scope> <type>pom</type> <version>23.0.1.Final</version> </dependency> <dependency> <groupId>org.wildfly</groupId> <artifactId>wildfly-spec-api</artifactId> <scope>provided</scope> <type>pom</type> <version>23.0.1.Final</version> </dependency>

In addition, IOM uses some dependencies that are provided by Wildfly, but are not exported by the BOM shown above. In case you are using one of the following dependencies with scope `provided`

, you have to update to the version shown in the list below.

<dependency> <groupId>commons-collections</groupId> <artifactId>commons-collections</artifactId> <version>3.2.2</version> </dependency> <dependency> <groupId>commons-io</groupId> <artifactId>commons-io</artifactId> <version>2.5</version> </dependency> <dependency> <groupId>commons-lang</groupId> <artifactId>commons-lang</artifactId> <version>2.6</version> </dependency> <dependency> <groupId>commons-beanutils</groupId> <artifactId>commons-beanutils</artifactId> <version>1.9.4</version> </dependency> <dependency> <groupId>org.jboss.ws</groupId> <artifactId>jbossws-api</artifactId> <version>1.1.2.Final</version> </dependency> <dependency> <groupId>org.apache.velocity</groupId> <artifactId>velocity-engine-core</artifactId> <version>2.3</version> </dependency> <dependency> <groupId>org.apache.cxf</groupId> <artifactId>cxf-core</artifactId> <version>3.3.10</version> </dependency> <dependency> <groupId>org.reactivestreams</groupId> <artifactId>reactive-streams</artifactId> <version>1.0.3</version> </dependency> <dependency> <groupId>org.apache.commons</groupId> <artifactId>commons-lang3</artifactId> <version>3.12.0</version> </dependency> <dependency> <groupId>org.apache.httpcomponents</groupId> <artifactId>httpmime</artifactId> <version>4.5.13</version> </dependency>

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.