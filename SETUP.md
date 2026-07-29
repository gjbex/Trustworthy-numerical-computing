# Environment Setup

This document describes how to set up the software environment for the training
material. It assumes that you have access to a Linux-style terminal and are
comfortable running shell commands.


## Required Software

Install the following software before the training:

* {{PRIMARY_LANGUAGE_OR_TOOLCHAIN}};
* {{BUILD_OR_RUNTIME_TOOL}};
* {{NOTEBOOK_OR_EDITOR_REQUIREMENT}};
* Git, if you plan to clone the repository.


## Get The Repository

Clone the repository with:

```bash
git clone {{REPOSITORY_URL}}
cd {{REPOSITORY_NAME}}
```


## Conda Environment

If this training uses `environment.yml`, create the environment with:

```bash
mamba env create -f environment.yml
```

Activate it with:

```bash
mamba activate {{CONDA_ENVIRONMENT_NAME}}
```

If `environment.yml` changes later, update the environment with:

```bash
mamba env update -f environment.yml --prune
```


## Verify The Setup

Run a small example from the repository:

```bash
{{VERIFY_COMMAND}}
```

You should see output similar to:

```text
{{EXPECTED_OUTPUT}}
```


## Remote Or HPC Access

If the training uses an HPC system, cloud environment, GPU node, database, or
other remote service, verify the following before the session:

* you can log in;
* you can transfer or clone files;
* you can load the required modules or activate the required environment;
* you can run a minimal test job or command;
* you know how to access local web applications if port forwarding is needed.


## Useful References

* {{REFERENCE_1}}
* {{REFERENCE_2}}
* {{REFERENCE_3}}
