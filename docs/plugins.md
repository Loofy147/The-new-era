# Plugin System

The plugin system is designed to be simple and extensible. It allows you to add new functionality to the application without modifying the core code.

## Plugin Manager

The plugin manager is located in `core/plugin_manager.py`. It is responsible for discovering, loading, and running plugins.

### `PluginManager(plugin_folder)`

The `PluginManager` class is initialized with the path to the plugin folder.

### `discover_plugins()`

This method discovers all the plugins in the plugin folder. It iterates through all the subdirectories in the plugin folder and tries to import them as plugins.

### `run_plugins()`

This method runs all the discovered plugins. It calls the `run` method on each plugin instance.

## Plugin Interface

The plugin interface is located in `core/plugin_interface.py`. It defines the contract that all plugins must adhere to.

### `PluginInterface`

This is an abstract base class that all plugins must inherit from.

### `run()`

This is an abstract method that all plugins must implement. This method is called by the plugin manager when the plugin is run.

## Creating a Plugin

To create a new plugin, you need to:

1.  Create a new directory in the `plugins` folder.
2.  Create an `__init__.py` file in your new directory.
3.  In the `__init__.py` file, create a class that inherits from `core.plugin_interface.PluginInterface`.
4.  Implement the `run` method in your plugin class.
5.  Create a `get_plugin` function that returns an instance of your plugin class.

For an example, see the `plugins/sample_plugin` directory.
