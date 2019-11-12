from ayx_blackbird import BasePlugin


class AyxPlugin(BasePlugin):
    @property
    def tool_name(self):
        return "ExampleTool"

    @property
    def record_batch_size(self):
        return 1

    def initialize_plugin(self):
        self.info(self.xmsg("Plugin initialized."))
        return True

    def build_metadata(self):
        self.info(self.xmsg("Metadata built."))
        self.output_anchors[0].record_info = self.input_anchors[0].connections[0].record_info

    def process_records(self):
        self.output_anchors[0].record_container = self.input_anchors[0].connections[0].record_container

    def on_complete(self):
        self.info(self.xmsg("Completed processing records."))

