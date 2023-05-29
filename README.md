# SwitchBoard

SwitchBoard is a library that leverages severless functions to allow users to create data pipelines and apply orchestration logic without running a dedicated instance.

## What problem does SwitchBoard solve?

There are many tools for orchestration out there already like Airflow, Luigi, Google Workflows, etc. However, for more simple and less complex use cases, there are a few problems with using previously existing tools.
* Usually, a dedicated instance is required for orchestration. This is typically an additional cost that can seem unreasonable given simple or low volume use cases that still have an orchestration need.
* In the case of something like Workflows, additional tools are required to manage orchestration. Additional tools utilized means additional technologies to manage.
* With a simple, low complexity use case, managing tools built for complex data flows can feel a bit over engineered.
SwitchBoard attempts to provide a simplistic option by enabling a development environment without having to align between multiple tools. Multiple data pipelines can be built using the SwitchBoard library and the orchestration can also be managed within all within a monorepo, or multiple if desired.

## How does it work?

SwitchBoard is comprised of four main components: **Callers**, **DataSources**, **Pipelines**, **StatusControllers**, and **a SwitchBoard**.

A **Caller** is triggered by a pubsub topic that will pass caller information to the **SwitchBoard**.
The **SwitchBoard** will determine the appropriate **Pipeline** to execute and reference the **StatusController** to verify if dependencies, if any, have been met.
The **Pipeline** will use a **DataSource** to perform the specified task.
On completion, the **Pipeline** will send confirmation to the **SwitchBoard** that it was executed successfully.
The **SwitchBoard** then updates the **StatusController** and identifies any downstream **Pipeline** to execute.

![Diagram](SwitchBoard.png)

