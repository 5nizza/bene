class RunStats:
    def __init__(self, cpu_time_sec:float=None,
                 wall_time_sec:float=None,
                 virt_mem_mb:int=None):
        self.cpu_time_sec = cpu_time_sec
        self.wall_time_sec = wall_time_sec
        self.virt_mem_mb = virt_mem_mb