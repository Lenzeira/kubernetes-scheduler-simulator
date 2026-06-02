class Pod:

    def __init__(
        self,
        name,
        cpu_required,
        memory_required,
        gpu_required=0,
        priority=1
    ):

        self.name = name

        self.cpu_required = cpu_required

        self.memory_required = memory_required

        self.gpu_required = gpu_required

        self.priority = priority

        self.allocated_worker = None


    def __str__(self):

        return (
            f"{self.name} | "
            f"CPU: {self.cpu_required} | "
            f"Memória: {self.memory_required}GB | "
            f"GPU: {self.gpu_required} | "
            f"Prioridade: {self.priority}"
        )
