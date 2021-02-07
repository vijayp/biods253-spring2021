# Design Document Template

## Overview

Biologists, data scientists, etc. make use of software to analyse their datasets. We want to aid them in setting up new projects with a structure better suited to writing code that is well-documented, structured, testable, and readable. Additionally we want to make it really easy to encapsulate dependencies, using best practices, either using virtual environments, Docker, or serverless infrastructure on Amazon/Google/Sherlock.  

We will build a system that (when complete) allows a user to select from a set of ode / infrastructure options for their project, and will provide them with a ready-to-use git-enabled repository with an appropriate structure and easy-to-use systems.  We will start with support for Python-based systems, and then later expand to R, anaconda, and a number of other systems. The system will eventually support a plug-in architecture that will allow members of the community to add support for new languages/frameworks without writing a lot (ideally any) code.

## Background: 

A few minutes spent setting up infrastructure appropriately at the start of a project (e.g., parsing command-line arguments properly, or starting off with a unittest) can play large dividends in the long run.  For non-SWE-experts, however, it can often be a distraction, and knowing what exactly to do, and how to do it can be daunting. 

Currently the best approach is to have each scientist understand the tradeoffs and design systems from scratch. This is error-prone; it is particularly difficult for non-domain-experts to make the right tradeoffs, or even understand what the implications of their decisions are.

### Other solutions

Our proposed solution is to design a system, hosted on a web page which will (eventually) allow a user to select components they intend to use from a set of choices. The site will generate a git repo and send it to them, at first by a .zip file download. 

Other possible solutions that we rejected include (1) creating a document describing how to accomplish this and expecting scientists to follow the doc (too complicated/error-prone), as well as (2) publishing a git repo with a sample infrastructure, and expecting the user to rename/copy/etc. the code.

The complexity of Java projects has led to similar systems which generate scaffolding based on user input on a web site.

### Current Goals

This project is complex, and might not be as used as we hope. Therefore we will implement it in multiple phases:

#### Phase I: Basic functionality

In Phase I, we will have a website that only supports one language, and no options (each zip file will contain all possible frameworks). It will not be possible to easily add plugin functionality. The only options the user can supply will be:

* The name of the project
* The name/email of the author
* The repository name


#### Phase II: Selecting some features
Phase II will build on Phase I by adding support for selecting some features (e.g. include docker support but not serverless support). We will still only support one type of language.



#### Phase III: Selecting multiple languages/plugin infrastructure

Here, we will allow the users to support different languages. We will also allow contributors to (relatively) easily add support for other languages and options. This will necessitate a extensible manifest and template logic structure.

### Non-Goals

We will not attempt to manage interactions with github, e.g. creating the repository for the user or uploading it. We will also not do much to help users set up AWS/GCP instances. We will not (easily) support upgrading basic scripts after the user has made some changes (this might necessitate using branches in the future). We won't support windows natively (though the zip file should work fine). 

### Future Goals

* Use github command line tool to interface with git making it easy to set up tracking repo
* All the stuff in non-goals above.


## Detailed Design


The system will be composed of a number of components that all work together to produce our desired output. The user will say something like "create me a scaffolding for a project called P1 that has a python commandline interface, and web interface that can be deployed to AWS lambda", and we will send the user back a zip file which has all the appropriate files with user input substituted in.

Code for the system will be in `repo/py`.


### File Templates

Every user request will generate a unique set of files. We will compute these by creating certain code template files, which will then be rendered using data provided by the user. We will use the Jinja2 templating system. In Phase I, all files will be nested under the following directory: `repo/py/data/code_templates/py3_expansion/`. Under here, the file system structure will be replicated into the eventual zip file.  In future phases, we will have a manifest for each plugin area with a bit of logic, i.e. which choices are incompatible, and which ones rely on other ones. This will be loaded and used to render the user form.

### Template expansion

We will write python code to expand the file templates against user input. This will be tested. The following parameters will be provided:
* language_name = {py3, anaconda, R, etc.}
* program_name = 
* author_name = name, can include spaces but no other whitespace TODO: utf-8?
* author_email = validated email
* repository_name = github_repo_name
* selected_features = dictionary of user selected features. for now {docker, serverless, unittest} are options.

This will generate files in a filesystem tree. We will ideally use a temporary directory or in-memory filesystem to perform this expansion.  

### Git repo creation

We will use `gitpython` to create a git repository in python. We will create a commit using the filesystem described above. In the future we should be able to do this directly by creating blobs.  We need to handle +x mode appropriately; in phase I, we can just copy the +x state from the template file, but in the future we should probably control this via a manifest file.

### Web interface

We will write a `flask`-based webapp that can be deployed to aws lambda. In Phase I, the webapp will render a landing page which will allow the user to put in values for the above template params. When the form is submitted, a different handler will respond with a `application/zip` file to be downloaded.

In future phases, the form will be rendered based on data gathered from manifest files in the appropriate directories, making the deployment of plugins easier. 


### User requirements

The user is expected to be a smart person with some experience coding, but limited software engineering expertise. Thus, the system should be relatively simple, defaults should set the user up for success, and documentation should explain clearly how to connect the downloaded repo to a github repository.

### What APIs will you use/change?
We will use serverless to abstract AWS/GCP command-line apis.


### Throughput/latency/cost/efficiency concerns?
none.

### Data validation/what are potential error states?

All user input will be validated. For instance all initial user inputs will conform to the regex `[0-9A-Za-z_\]+` to prevent any RCE


### Logging/monitoring/observability
We won't worry about this for now

### Security/Privacy
We will only collect user emails for contacting the user in the future. We should probably have a security page and a privacy policy on the web page.

### What will you test?
We're going to test the template framework extensively to ensure that code that is created works.

## Third Party dependencies

## Work Estimates
Phase I should take approximately 3 hours to write, other phases TBD

## Related Work?

Java spring has a similar [generator](https://start.spring.io).

