---
id: '00d52dbfac5ac48ecb11b59fd4f924ce'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/295T65'
scraped_at: '2026-04-21T05:38:30.715615+00:00'
---
Several libraries with vulnerabilities were updated and can potentially break the implementation.

| Library | Old Version | New Version |
|---|---|---|
| com.google.guava:guava | 24.1-jre | 29.0-jre |
| com.google.code.gson:gson | 2.1 | 2.8.6 |
| org.apache.commons:commons-dbcp2 | 2.1.1 | 2.7.0 |

In case of version conflicts of underlying and custom libraries, the version must be defined explicitly. The *build.gradle *can contain the following block:

versionRecommendation { provider { // thirdparty.version to resolve version conflicts of custom cartridges properties('thirdparty', file('thirdparty.version')) {} } }

Example version file to resolve version conflict for library "`error_prone_annotations`

".

com.google.errorprone:error_prone_annotations=2.3.1

Some libraries can contain resources which have the same name. To exclude such resources, a configuration of the task must be adapted:

* What went wrong: Execution failed for task ':<assembly>:checkClassCollisions'. > There are class collisions in your dependencies > Collision between io.github.classgraph:classgraph:4.6.32 and net.bytebuddy:byte-buddy:1.9.10 > META-INF.versions.9.module-info

// verify whole server classpath to be collision-free checkClassCollisions { allCartridges = true ignore 'META-INF.versions.\\d+.module-info' // ignore module-info.class files in META-INF/**cd }

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.