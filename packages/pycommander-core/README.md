# Silicon Labs PyCommander Core

This package contains the core Python code for Silicon Labs PyCommander.

Note that this package does not contain the Commander executable, it is not intended to be installed directly, and it is not functional on its own. This package is a dependency of the `silabs-pycommander-cli` and `silabs-pycommander-gui` packages.

Preferably, PyCommander should be installed and updated via the [`silabs-pycommander`](../pycommander/README.md) meta-package. That install provides the CLI executable and the Python API:

```bash
pip install "silabs-pycommander"
```

To install the GUI executable as well:

```bash
pip install "silabs-pycommander[gui]"
```

The `pycommander` command and the Python API are documented in that README.
