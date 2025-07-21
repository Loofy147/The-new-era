from core.plugin_manager import PluginManager

def main():
    plugin_manager = PluginManager("plugins")
    plugin_manager.discover_plugins()
    plugin_manager.run_plugins()

if __name__ == "__main__":
    main()
