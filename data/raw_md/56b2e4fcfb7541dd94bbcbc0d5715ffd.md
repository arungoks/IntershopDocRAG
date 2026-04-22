---
id: '56b2e4fcfb7541dd94bbcbc0d5715ffd'
title: 'Table of Contents'
url: 'https://knowledge.intershop.com/kb/index.php/Display/30704F'
scraped_at: '2026-04-21T05:37:38.817360+00:00'
---
This guide lists all migrations required from Intershop Order Management 4.3 to 4.4. The document is aimed to project developers.

Migration to Wildfly 27 requires following the breaking switch from Java Enterprise 8 to Jakarta EE 10. The following guidelines outline what was necessary to accomplish this in the IOM platform code - but it is not “guaranteed” to be complete, depending on the number of customizations done in a project.

**IMPORTANT** Please coordinate this migration with your team. Nearly every file in your project will be changed.

__Wildfly BOM:__ Change `artifactId`

from `wildfly-jakartaee8-with-tools`

to `wildfly-ee-with-tools`

and update the version to 27.0.1.Final

__JAXB runtime:__ In case you have declared any `jaxb-impl`

dependencies - for example for the "test" lifecycle - change the dependency to `org.glassfish.jaxb:jaxb-runtime`

. The version is managed by Wildfly BOM.

__Hibernate:__ The artifact `hibernate-jpamodelgen`

has been moved from `org.hibernate`

to `org.hibernate.orm`

groupId.

__JAXB plugin:__ Switch from `org.jvnet.jaxb2.maven2:maven-jaxb2-plugin`

to `com.evolvedbinary.maven.jvnet:jaxb30-maven-plugin`

(see [https://mvnrepository.com/artifact/com.evolvedbinary.maven.jvnet/jaxb30-maven-plugin](https://mvnrepository.com/artifact/com.evolvedbinary.maven.jvnet/jaxb30-maven-plugin))

__JAX-WS plugin:__ Switch from `org.codehaus.mojo:jaxws-maven-plugin`

to `com.sun.xml.ws:jaxws-maven-plugin`

(see [https://mvnrepository.com/artifact/com.sun.xml.ws/jaxws-maven-plugin](https://mvnrepository.com/artifact/com.sun.xml.ws/jaxws-maven-plugin) )

__Swagger codegen:__** **If you are still using the legacy `io.swagger.core.v3:swagger-maven-plugin`

you should be able to easily migrate by using `io.swagger.core.v3:swagger-maven-plugin-jakarta`

instead.

__Openapi generator:__ For generated Java clients, upgrade to the latest plugin version and switch the “library” option from `jersey2`

to `jersey3`

(+ update the according dependencies). For server stubs please check the currently available options in the plugin documentation/issue tracker: [https://github.com/OpenAPITools/openapi-generator/issues?q=jakarta](https://github.com/OpenAPITools/openapi-generator/issues?q=jakarta)

Fallback: In case there is no feasible option to get Jakarta annotations via openapi-generator, you can apply a workaround by adding this plugin to your build configuration. Adjust the `dir`

attribute if necessary:

<plugin> <artifactId>maven-antrun-plugin</artifactId> <executions> <execution> <phase>process-sources</phase> <configuration> <target> <replace token= "javax." value="jakarta." dir="target/generated-sources/swagger/src/gen/java/"> <include name="**/*.java"/> </replace> </target> </configuration> <goals> <goal>run</goal> </goals> </execution> </executions> </plugin>

First of all run `mvn clean`

or manually delete the target directory.

Get the Tomcat Migration Tool for Jakarta EE. Download the *shaded jar* from *Binary distribution*: [https://tomcat.apache.org/download-migration.cgi](https://tomcat.apache.org/download-migration.cgi)

Place the jar in the parent directory of your project. Example: If your project *pom.xml *is located in `/path/to/project/myproject/pom.xml`

, place the jar in `/path/to/project/`

.

Execute the migration tool: `cd /path/to/project && java -jar jakartaee-migration-VERSION-shaded.jar -profile=EE myproject/ myproject.new/`

.

Check log for errors.

Now you can replace the old `myproject`

folder by `myproject.new`

.

Open your *persistence.xml* file:

Ensure that no property still uses the javax. namespace - otherwise change this to Jakarta.

Remove the `hibernate.dialect`

property. The new version works better with autodetection.

When using non jpa-compliant, hibernate specific (HQL) features, you can set `hibernate.jpa.compliance.query`

to `false`

to restore the old behavior of lenient validation.

Native queries that formerly returned `BigInteger`

will now return `Long`

objects

Native queries that formerly returned `Timestamp`

java objects for `Timestamp with Timezone`

columns **might** return `Instant`

now. However, in most cases IOM uses `Timestamp without Timezone`

. Specific database functions that return timezone information (like `now()`

) can be cast to `::timestamp`

to restore the old behavior.

Intershop recommends to test all code involving custom entities and queries due to the numerous changes in Hibernate 6.x.

After following other migration steps in this guide, you should be able to build the project via `mvn clean package`

.

Before applying any workarounds make sure the library you are using is still actively maintained, e.g. by checking their last release or how active the github issue tracker of the project is:

Newer version available: update accordingly.

Newer version should be available soon(tm): you may follow the workaround below.

Library development is dead: check for forks of this library that were created by other maintainers. If this is not the case, evaluate replacing the library. If this is not possible either follow the workaround below.

Using the eclipse transformer plugin, you can update existing libraries to use the Jakarta namespaces instead of javax. To do so, create a new module that includes only a *pom.xml* like this:

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd"> <modelVersion>4.0.0</modelVersion> <parent> <groupId>bakery.parent</groupId> <artifactId>bakery.parent</artifactId> <version>bakery.pom-trunk-SNAPSHOT</version> <relativePath>../../bakery/pom.xml</relativePath> </parent> <version>${iom.version}</version> <groupId>com.intershop.oms.quartz</groupId> <artifactId>quartz</artifactId> <name>[Jar] quartz jakarta version</name> <packaging>jar</packaging> <build> <plugins> <plugin> <groupId>org.apache.maven.plugins</groupId> <artifactId>maven-compiler-plugin</artifactId> </plugin> <plugin> <groupId>org.eclipse.transformer</groupId> <artifactId>transformer-maven-plugin</artifactId> <version>0.5.0</version> <extensions>true</extensions> <configuration> <rules> <jakartaDefaults>true</jakartaDefaults> </rules> </configuration> <executions> <execution> <id>default-jar</id> <goals> <goal>jar</goal> </goals> <configuration> <artifact> <groupId>org.quartz-scheduler</groupId> <artifactId>quartz</artifactId> <version>2.3.2</version> <type>jar</type> </artifact> </configuration> </execution> </executions> </plugin> </plugins> </build> </project>

configuration.artifact contains the **original maven coordinates** of the library that should be migrated.

The groupId/artifactId of this submodule is the **new maven coordinates** of the library.

Update the actual project’s *pom.xml* to use the **new maven coordinates**.

[Postgres 15](https://www.postgresql.org/docs/release/15.0/) is more strict in the SQL syntax and now expects a space character after numerics.

This can lead to exceptions with malformatted native queries in custom code.

These 3 syntaxes worked previously, but now throw an exception ("trailing junk after numeric literal")

select 1UNION select 2 WHERE a=1OR b=2 select 100alias

This database migration can only be perfomed when the application is down.

You can reduce the down time by creating new indexes in advance. **However, this has to be done before stopping the application. **

Moreover, you should verify that the default configuration of the new cleanup job meets your requirements:

This version introduces a new job to delete old entries in table `oms.JobRunHistoryDO`

. For details, refer to [Reference - Database Jobs](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1902583030) *Cleanup of oms.JobRunHistoryDO*.

The database migration will define this job with a default retention time of 35 days and add an index on `JobRunHistoryDO`

.

You can improve the migration time while deleting old entries **prior to the migration**.

This will prevent including values in the new index, which will be deleted at the first job run anyway.

Example:

DELETE FROM oms."JobRunHistoryDO" WHERE "modificationDate" < now() - ('35 days')::interval;

Add the new indexes introduced with that version (respect their name!)

CREATE INDEX CONCURRENTLY IF NOT EXISTS "JobRunHistoryDO_modificationDate" on oms."JobRunHistoryDO" ("modificationDate"); CREATE INDEX CONCURRENTLY IF NOT EXISTS "InvoicingDO_state_part" ON oms."InvoicingDO" USING btree ("stateRef") WHERE ("stateRef" = ANY (ARRAY[0,500,1001,7001,7501])); CREATE INDEX CONCURRENTLY IF NOT EXISTS "PaymentSalesPricePromotionDO_paymentSalesPriceRef" ON oms."PaymentSalesPricePromotionDO"("paymentSalesPriceRef"); CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS "index_OrderStateAO_uk_orderPosRef" ON oms."OrderStateAO" USING btree ("orderPosRef");

In case 35 days retention time is not sufficient, you can define the job manually, shortly prior to the migration.

This may trigger subsequent errors as the related function is added during the migration, (or you first add the job and set it as active after the migration):

INSERT INTO admin.db_jobs(active,function_name,configuration,cron_expression) SELECT false,'admin.delete_jobrunhistorydo','{"days2keep": 35}','1 3 12 ? * * *' WHERE NOT EXISTS (SELECT * FROM admin.db_jobs where function_name='admin.delete_jobrunhistorydo');

UPDATE admin.db_jobs SET active= true WHERE function_name='admin.delete_jobrunhistorydo';

A subset of the order and order position attributes are synchronized to the table `OrderStateAO`

for reporting purposes. This synchronization was faulty in case of order modifications ("order changes").

The corresponding defect ([#81670](https://knowledge.intershop.com/kb/go.php/o/81670)) has been fixed, but as the corresponding feature is not used in existing projects the migration does not check the integrity of the data in `OrderStateAO`

.

Custom implementations of an “order change” feature should verify if they are affected by this bug or a similar issue, potentially correct custom triggers, and rebuild the content of the synchronized data.

(The standard core synchronization is now achieved with 2 triggers: *sync_orderstateao* ON OrderDO and *sync_delete_pos_orderstateao* ON oms."OrderPosDO".

The previous trigger *update_orderstateao *ON OrderDO has been removed.)

IOM 4.4.0 includes the latest fixes from IOM 4.3.4. If you are upgrading from a version **older than IOM 4.3.4**, please check the according [release notes](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/47770962016/Public+Release+Note+-+Intershop+Order+Management+4.X#Release-IOM-4.3.4) and remember to apply the mentioned migration script manually after the deployment of IOM 4.4.0.

Deprecated usage of PostgreSQL 11 ([80821](https://knowledge.intershop.com/kb/go.php/o/80821))

Deprecated ArticleInfoArticleAO.stockLevel ([77458](https://knowledge.intershop.com/kb/go.php/o/77458))

The update of the stock level in this database view was originally meant to provide stock info in the article export functionality. Current projects still have a stock export, but it uses the ATP infrastructure.

IOM is hence stopping the synchronization of ArticleInfoArticleAO.stockLevel in this version.

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.