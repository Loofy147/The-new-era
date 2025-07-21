import importlib
import os

class PluginManager:
    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder
        self.plugins = []

    def discover_plugins(self):
        for plugin_name in os.listdir(self.plugin_folder):
            plugin_path = os.path.join(self.plugin_folder, plugin_name)
            if os.path.isdir(plugin_path):
                try:
                    module = importlib.import_module(f"plugins.{plugin_name}")
                    plugin = module.get_plugin()
                    self.plugins.append(plugin)
                except (ImportError, AttributeError) as e:
                    print(f"Could not import or get plugin {plugin_name}: {e}")

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.run()
