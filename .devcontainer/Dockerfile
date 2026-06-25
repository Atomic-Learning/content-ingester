FROM mcr.microsoft.com/devcontainers/python:1-bookworm

# Graphviz is required by some graph tooling workflows that rely on pydot.
RUN apt-get -o Dir::Etc::sourcelist="sources.list.d/debian.sources" -o Dir::Etc::sourceparts="-" update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*
