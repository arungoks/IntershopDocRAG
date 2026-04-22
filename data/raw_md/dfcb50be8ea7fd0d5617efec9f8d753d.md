---
id: 'dfcb50be8ea7fd0d5617efec9f8d753d'
title: 'Managing Searchandizing'
url: 'https://knowledge.intershop.com/kb/index.php/Display/32Z817'
scraped_at: '2026-04-21T05:31:27.775836+00:00'
---
# Managing Searchandizing

Searchandizing subsumes mechanisms for promoting products or categories when users search for certain keywords or phrases. With Intershop Commerce Management, you can set up redirects, which are intended to produce specific pages instead of actually performing the user's search.

## Creating Search Redirect

-
Select the management context from the context selection box, then select Mass Data Tasks | Search Indexes.
This displays a list of all search indexes for the selected management context.
-
Click the name of the search index you intend to edit.
This displays the Search Index detail view for the selected index.
-
Change to the Searchandizing tab.
The Redirects section lists the defined search redirects for the current search index.
-
In the Redirects section, click New.
This displays an empty redirect detail view.
-
Specify the intended search term, and select the match type.
The available match types include exact and partial.
-
Set the redirect trigger.
To make sure that the redirect action only takes place after the search has been executed and has produced no result, select the checkbox Trigger When No Search Result.
-
Select the redirect target.
The following table lists the available targets.
Table 1. Search redirect targets Target Type Description Category Allows for selecting a catalog category of the current channel as the redirect target. Product Allows for selecting an individual product of the current channel as the redirect target. Page Allows for selecting any available content page of the current channel as the redirect target. Search Allows for defining a target search term to search for if the trigger search term is used. URL Specifies any user-defined URL as the redirect target. -
Click Apply.
This immediately enables the redirect for the specified search term. Clicking the Preview button () opens the target page in the storefront editing mode (not available for "Search" redirect type). Clicking Back to List returns you to the Searchandizing tab of the Search Index detail view.

## Modifying Search Redirect

-
Select the management context from the context selection box, then select Mass Data Tasks | Search Indexes.
This displays a list of all search indexes for the selected management context.
-
Click the name of the search index you intend to edit.
This displays the Search Index detail view for the selected index.
-
Change to the Searchandizing tab.
The Redirects section lists the defined search redirects for the current search index.
-
To preview a redirect target, click the Preview button in the row of the intended redirect (not available for "Search" redirect target).
This opens the configured target page in the storefront editing mode.
-
To edit a redirect target, click the name of the intended search term.
This displays the redirect detail view.
- Edit the match type and redirect target as required.
-
Click Apply to save your settings.
Otherwise, click Reset to discard your changes. Clicking the Preview button () opens the target page in the storefront editing mode (not available for "Search" redirect target). Clicking Back to List returns you to the Searchandizing tab of the Search Index detail view.

## Deleting Search Redirect

-
Select the management context from the context selection box, then select Mass Data Tasks | Search Indexes.
This displays a list of all search indexes for the selected management context.
-
Click the name of the search index you intend to edit.
This displays the Search Index detail view for the selected index.
-
Change to the Searchandizing tab.
The Redirects section lists the defined search redirects for the current search index.
-
Select the redirect to be removed.
Mark the checkbox of the intended redirect configuration.
-
Click Delete, then OK to confirm the deletion.
The selected redirect configuration is removed from the current search index.