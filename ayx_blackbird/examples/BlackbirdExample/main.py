import AlteryxPythonSDK as sdk

from ayx_blackbird import BasePlugin, RecordUpdater


class AyxPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # import cProfile
        # self.pr = cProfile.Profile()
        # self.pr.enable()

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdExample"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return None

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor = self.get_output_anchor("Output")

        output_record_info = self.input_anchor.connections[
            0
        ].record_info.clone()

        output_record_info.add_field("Blackbird", sdk.FieldType.double)

        self.output_anchor.record_info = output_record_info
        self.push_all_metadata()
        return True

    def process_records(self) -> None:
        """Process records in batches."""
        # import pandas as pd

        input_records = self.input_anchor.connections[0].record_container
        output_records = self.output_anchor.record_container
        # df = pd.DataFrame({"Blackbird": [10 for _ in range(len(input_records))]})
        # RecordUpdater(input_records, output_records).apply_update(df)

        df = input_records.parse_to_df()
        df["Blackbird"] = [10 for _ in range(len(input_records))]
        output_records.set_from_df(df)

        # self.push_all_records()
        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalizer for plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))

        # import pstats
        # self.pr.disable()
        # ps = pstats.Stats(self.pr).sort_stats('cumulative')
        # ps.dump_stats('C:\\Users\\dellison\\Desktop\\profile.pstats')
