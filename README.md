# Plugin System

This project includes a modular plugin system that allows for easy extension of its functionality.

## Creating a Plugin

To create a new plugin, you need to:

1.  Create a new directory in the `plugins` folder.
2.  Create an `__init__.py` file in your new directory.
3.  In the `__init__.py` file, create a class that inherits from `core.plugin_interface.PluginInterface`.
4.  Implement the `run` method in your plugin class.
5.  Create a `get_plugin` function that returns an instance of your plugin class.

For an example, see the `plugins/sample_plugin` directory.
