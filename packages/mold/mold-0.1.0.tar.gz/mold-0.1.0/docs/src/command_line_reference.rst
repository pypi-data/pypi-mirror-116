
.. _cli:

Command line reference
======================

.. code-block:: text

   Extensible and configurable project initialisation.

   usage: mold [configuration]
          mold add [configuration]
          mold config <command> [arg]
          mold [--help] [--version]

   COMMANDS:
   [configuration]     Initialise a new project.
   add [configuration] Add files to an existing project. All files
                       that a tool would write must be missing for
                       them to be added to the project.

   config list         List all saved configurations.
   config new [name]   Create a new configuration.
   config show [name]  Show a configuration.
   config del [name]   Delete a configuration.

   --help, -h          Display this help message and quit.
   --version, -v       Display Mold version and quit.

   Missing optional parameters are determined with a dialog.
