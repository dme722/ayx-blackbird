import AlteryxPythonSDK as sdk


class EngineMixin:
    def xmsg(self, message):
        return message

    def error(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.error, message)

    def warning(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.warning, message)

    def info(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.info, message)

    @property
    def update_only_mode(self):
        return (
                self.engine.get_init_var(
                    self.tool_id, "UpdateOnly"
                )
                == "True"
        )