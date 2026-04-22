---
id: '0aab7cef5fc7df9d08627e06e506defc'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/2923K1'
scraped_at: '2026-04-21T05:36:49.148364+00:00'
---
Intershop recommends Azure DevOps as tooling to support the CI processes. A project-ready Azure DevOps environment can be provided by Intershop. It already contains a Git repository with the Responsive Blueprint Store and the necessary build pipelines. Also boards for agile management are included in Azure DevOps.

This way professional project development can be started right away without the need to set it up manually.

The Blueprint project with all necessary cartridges is provided in an Azure DevOps Git repository when Intershop sets up the project.

This repository must be cloned to the developer machine:

**Cloning the Repository**

git clone https://example@dev.azure.com/example/example/_git/example

You can either set a password for the Git account or provide your public key.

Edit the file *environment.properties* based on you local configuration, e.g.,

Set database connection

Set path to the license file

Provide the file *development.properties* containing the development specific configurations, e.g.,

Check source

Pre-loading

See also [Cookbook - Gradle Developer Workflow](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1822584007/Cookbook+-+Gradle+Developer+Workflow).

Run the following commands to build and deploy the project:

**Build and Deploy the Project**

gradle_environment.bat gradlew enableHotCodeReloading gradlew publish gradlew deployServer

As soon as you have pushed your local changes to the Azure DevOps Git repository, the CI Build pipeline will be started.

See also [Concept - Continuous Delivery Tools (valid to 7.10)](https://knowledge.intershop.com/kb/go.php/a/ENFDEVDOC/pages/1784317189).

To trigger a release build that publishes the binaries release with a specific version of the Nexus binary repository, you just need to add a release label in form of a git tag.

Nexus:

The information provided in the Knowledge Base may not be applicable to all systems and situations. Intershop Communications will not be liable to any party for any direct or indirect damages resulting from the use of the Customer Support section of the Intershop Corporate Website, including, without limitation, any lost profits, business interruption, loss of programs or other data on your information handling system.