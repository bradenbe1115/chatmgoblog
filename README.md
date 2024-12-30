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

The entrypoint into these services is a work in progress. Currently, we are importing them directly into pipeline methods in a different directory, but we may pivot to making the services stand-alone containers at some point for orchestration purposes.

### ./tests

This directory contains all of our tests for the project. Tests are divided into unit, integration, and e2e tests. We are aiming for a testing pyramid where we perform unit tests as much as possible and implement integration and e2e tests wherever necessary.

There is a Dockerfile in the root directory responsible for the creation of a Container to run all of the tests in. 

### ./pipelines

In the current state, this is where the entrypoints to our project source code and logic live. In this directory, we implement pipelines of methods and/or logic that need to run based on a certain command within a self contained environment by importing the necessary services from our source code. We don't view this as our end game infrastructure, but a lightweight method to starting to run some e2e code that will be easy to refactor into a more stable solution.

Each folder in the pipelines directory represents a pipeline that needs to run for the application and his it's own Dockerfile to run that pipeline. 

### ./modeling

Since this is a data science project as much as it's a development project, there is a folder dedicated to modeling work. This folder contains jupyter notebooks used to explore different methods, algorithms, and/or foundational models for the project. 
