import datetime


class ExperimentRecord:
    def __init__(self,
                 name:str,
                 date:datetime.datetime,
                 tool_cmd:str,
                 tool_params:str,
                 commit:str or None,
                 time_limit_sec:int,
                 memory_limit_mb:int,
                 hardware:str,
                 note:str or None,
                 tag:str or None):
        self.name = name
        self.date = date
        self.tool_cmd = tool_cmd
        self.tool_params = tool_params
        self.commit = commit
        self.time_limit_sec = time_limit_sec
        self.memory_limit_mb = memory_limit_mb
        self.hardware = hardware
        self.note = note
        self.tag = tag

    def __str__(self):
        return '<ExperimentRecord>' + '\n' \
               + '\n'.join(list(map(lambda vv: vv[0] + ': ' + str(vv[1]),
                                    self.__dict__.items()))) \
               + '\n</ExperimentRecord>'


class RunRecord:
    def __init__(self,
                 exp:ExperimentRecord or None,
                 input_file:str,
                 total_time_sec:int,
                 time_win_region_sec:int or None,
                 time_circuit_sec: int or None,
                 circuit_size:int or None,
                 memory_mb:int,
                 is_realizable:bool,
                 model:str or None,
                 logs:str or None,
                 note:str or None,
                 tag:str or None):
        self.exp = exp
        self.filename = input_file
        self.total_time_sec = total_time_sec
        self.time_win_region_sec = time_win_region_sec
        self.time_extraction_sec = time_circuit_sec
        self.circuit_size = circuit_size
        self.memory_mb = memory_mb
        self.is_realizable = is_realizable
        self.model = model
        self.logs = logs
        self.note = note
        self.tag = tag

    def __str__(self):
        return '<RunRecord>' + '\n'\
               + '\n'.join(list(map(lambda vv: vv[0] + ': ' + str(vv[1]),
                                    self.__dict__.items())))\
               + '\n</RunRecord>'


