import datetime


class ExpDesc:
    def __init__(self,
                 exp_name,
                 datetime_:datetime,
                 commit,
                 hardware,
                 note):
        self.exp_name = exp_name
        self.datetime = datetime_
        self.commit = commit
        self.hardware = hardware
        self.note = note

    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)


class ToolRunParams:
    def __init__(self, tool_cmd, tool_params, input_file, output_file, tool_log_file):
        self.cmd = tool_cmd
        self.params = tool_params
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = tool_log_file

    def to_cmd_str(self):   # TODO: clean: move out of here
        return '{exec} {params} {input_file} {output}' \
            .format(exec=self.cmd,
                    params=self.params,
                    input_file=self.input_file,
                    output='' if not self.output_file else ' -o ' + self.output_file)

    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)


class TimedRunParams:
    def __init__(self, time_limit_sec, memory_limit_mb):
        self.time_limit_sec = time_limit_sec
        self.memory_limit_mb = memory_limit_mb

    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)


class RunResult:
    def __init__(self,
                 total_time_sec: int or None,
                 circuit_size: int or None,
                 memory_mb: int or None,
                 is_realizable: str,
                 model: str or None):
        self.total_time_sec = total_time_sec
        self.circuit_size = circuit_size
        self.memory_mb = memory_mb
        self.is_realizable = is_realizable
        self.model = model

    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)
