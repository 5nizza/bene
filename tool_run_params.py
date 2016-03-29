class ToolRunParams:
    def __init__(self,
                 tool_cmd, tool_params, input_file, output_file, tool_log_file):
        self.cmd = tool_cmd
        self.params = tool_params
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = tool_log_file

    def to_cmd_str(self):
        return '{exec} {params} {input_file} -o {output_file}'\
            .format(exec=self.cmd,
                    params=self.params,
                    input_file=self.input_file,
                    output_file=self.output_file)
