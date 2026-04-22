---
id: 'feb9ef78d92ffc64720fbedfef978ddc'
title: 'Guide'
url: 'https://knowledge.intershop.com/kb/index.php/Display/25S917'
scraped_at: '2026-04-21T05:41:31.941961+00:00'
---
# Introduction

This document describes conventions for the layout of pipelines for applications based on Intershop 7.

# Guidelines

- The pipeline execution should flow downwards. This means that transitions in general should not go up (loops are an exception).


- Prefer straight transitions and right angled transitions to diagonal ones.


- An exception can be made if a call node has more than one exit. One transition will go straight down and the others will start diagonally (down and right) and then go down.


- The transition that follows the normal execution exit of a pipeline node (pipelet next, decision node “yes”) should go straight down and the ones that follow the error exit should go to the right (or diagonally down and right in case of a call node).


- The directions of the normal and error exit transitions can be reversed if it would produce a cleaner pipeline (for example if when using the previous rules some transitions intersect)


- Do not overlap transitions


- For loop nodes the last transition of the loop goes left and up.


- If a branched pipeline is combined again, the transition can go left.


- A transition may also go left if two different branches have to be merged. Merging different branches should be avoided.

- Create additional join nodes when required by the above rules.


These rules should not be broken, unless it will improve the clarity and readability of the pipeline.