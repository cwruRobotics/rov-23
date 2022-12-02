# MATE ROV 2022-23

<a href="https://github.com/cwruRobotics/rov-23/actions"><img src="https://github.com/cwruRobotics/rov-23/workflows/Continuous Integration/badge.svg" alt="Build Status"></a>
<a href=" https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Build Status"></a>

## Setup
[Follow this environment setup guide!](https://github.com/cwruRobotics/rov-23/wiki/Environment-Setup)

Then create a workspace:

Access WSL by opening VSCode, pressing `ctrl`+`` ` `` (below the `esc` key), clicking the dropdown arrow on the right and selecting `Ubuntu (WSL)`. You can also view your WSL files by opening `File Explorer > Linux (bottom left) > Ubuntu > home > your Ubuntu username`.

Run
```
mkdir -p rov_23_ws/src
```

```
cd rov_23_ws/src
```

```
git clone https://github.com/cwruRobotics/rov-23.git .
```
(the period is important)

## Directory Structure
All packages to be installed on the surface computer live in the `surface` directory.

All packages to be installed on the pi compute module live in the `pi` directory.

All packages to be installed on the float live in the `float` directory.

Single commits should not modify more than one of these directories.
