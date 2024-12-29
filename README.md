# Chat MGoBlog

A project demonstrating an end to end project for a RAG based LLM chatbot using data from MGoBlog.

## Structure

### ./src

The source code for services is found within this directory. Services follow a unit of work style of abstraction to enable test driven development. 

Each directory within this folder is a service responsible for a specific portion of the application. Each directory typically has a common and a service_layer directory. The common directory holds domain specific data models and interfaces and are shared across the service layer use cases. Interfaces are implemented as abstract classes and dependencies are injected upon initialization to enable easy unit testing for the application.

The service_layer directory typically contains two files:

- services.py - python methods for services implemented by this directory
- unit_of_work.py - Encapsulates the dependencies and state, following the Unit of Work pattern. This class would manage transactions or state persistence, helping ensure that actions across multiple services or repositories are handled atomically.

These two files work together to implement the services that can be used in the application.

It's common for each service directory to have config.py and bootstrap.py files as well. These are used to bootstrap the service layer with standard, pre-defined dependencies. 

- config.py: Typically holds configuration settings (e.g., database configurations, service URLs, environment-specific settings).
- bootstrap.py: Responsible for initializing the service layer, wiring dependencies together, and setting up pre-defined services.
