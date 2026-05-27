# Dependency Graph

Generated from mode: proposed.

## Legend

- Green: new page in this proposal or content batch
- Grey: existing page already present in platform content
- Yellow: proposed missing prerequisite not yet in platform
- Red: referenced slug not identified as existing or proposed missing

```mermaid
flowchart TD
    python_numpy_introduction["python-numpy-introduction"]
    python_packages["python-packages"]
    python_scipy_introduction["python-scipy-introduction"]
    python_numpy_introduction --> python_scipy_introduction
    python_packages --> python_numpy_introduction
    python_packages --> python_scipy_introduction

    classDef new fill:#b6e7a7,stroke:#2d6a4f,color:#111,stroke-width:1px;
    classDef existing fill:#d9d9d9,stroke:#666,color:#111,stroke-width:1px;
    classDef missing fill:#ffe8a3,stroke:#946200,color:#111,stroke-width:1px;
    classDef unknown fill:#ffd6d6,stroke:#a33,color:#111,stroke-width:1px;
    class python_numpy_introduction,python_scipy_introduction new;
    class python_packages existing;
```
