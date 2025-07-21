from core.plugin_interface import PluginInterface

class SamplePlugin(PluginInterface):
    def run(self):
        print("Hello from the sample plugin!")

def get_plugin():
    return SamplePlugin()
