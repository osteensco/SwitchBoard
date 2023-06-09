<h1 align="center">SwitchBoard</h1>

<div align="center">
  <img src="https://github.com/osteensco/SwitchBoard/assets/86266589/d4969c53-1b44-47d6-9be1-6333a9ce6c24"><br>


</div>

<br>
<br>

SwitchBoard is a framework designed for utilizing severless functions and applying orchestration logic for lightweight data transformations, data processing, and data pipelines.

<br>
<br>

## Table of Contents
**[About SwitchBoard](#about-switchboard)**<br>
**[How does it Work?](#how-does-it-work)**<br>
**[Quickstart](#quickstart)**<br>

<br>
<br>
  
***
  
<br>
<br>

## About SwitchBoard  
  
### What problem does SwitchBoard solve?
  
In the age of Big Data it's easy to forget that not every use case involves petabytes of data or thousands of data pipelines.
There are many tools for orchestration out there already, but for low complexity and/or low volume use cases, there are a few problems with using other tools.
<br>
  
* ### Most orchestration tools need a dedicated instance to run. <br>

    This is typically an additional cost that can seem unreasonable given less complex use cases that still have an orchestration need. SwitchBoard is meant to be used with serverless functions, so a dedicated instance is not necessary. In terms of cost, this makes it easy to stay within the free tier or under a few cents a month with most cloud providers. <br>
    
* ### Other tools that don't need a dedicated instance usually require multiple technologies used in conjunction with one another in order to apply orchestration logic. <br>

    It's common for these tools to require log parsing, message or event triggers implemented, and then the actual orchestration logic has to be defined somewhere. Additional tools means additional technologies to manage. This adds seemingly unnecessary complexity to otherwise low complexity projects. SwitchBoard uses JSON files in object storage with simple schemas to track pipeline completetions and check dependencies. <br>
    
* ### Managing tools designed with complex data flows in mind for simple projects can feel a bit over engineered.  <br>
    SwitchBoard is designed to be easy to set up and easy to use. It's not meant for complex data flows. It's purpose is to provide the low complexity solution to low complexity problems. <br>
  
<br>
SwitchBoard attempts to provide a simplistic option by enabling a development environment without having to align between multiple tools.  
Multiple data pipelines can be built and orchestration managed using the SwitchBoard framework within a monorepo. While it is designed with a monorepo in mind, multiple can still be used if desired.  
  
<br>
<br>
<br>
Currently, only Python and Google Cloud are supported. There are plans to support other languages and cloud providers in the future.  

<br>
  
***
  
<br>
<br>

## How does it work?
  
SwitchBoard is comprised of 4 main components: **Callers**, **StatusControllers**, the **destinationMap** and **a SwitchBoard**.  
  
#### Typical workflow for a SwitchBoard App: 
* An enpoint is triggered via pub/sub or http and uses a **Caller** to trigger the **SwitchBoard** and provide information about the caller.  
* The **SwitchBoard** will read the **destinationMap** ENV variable and determine the appropriate serverless function to execute, then check the **StatusController** to verify the dependency requirements, if any, have been met before triggering the function.  
* On completion, the serverless function will use another **Caller** to send confirmation to the **SwitchBoard** that it was executed successfully.  
* The **SwitchBoard** then updates the **StatusController** and checks the **destinationMap** to identify any additional downstream functions to execute.  
<br>

<div align="center">
  <img src="https://github.com/osteensco/SwitchBoard/assets/86266589/f9f5df77-8e36-41b8-8984-4b04d634ed29"><br>
</div>

<br>
  
***
  
<br>
<br>

## Quickstart  

Install the switchboard library:  

`pip install git+https://github.com/osteensco/Cloud-SwitchBoard.git#egg=cloud-switchboard`  

To build boilerplate project directory, run:  

`switchboard-cli start_project <project_name> <cloud_provider>`
