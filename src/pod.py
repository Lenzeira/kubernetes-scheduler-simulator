class Pod:

    def __init__(
        self,
        name,
        cpu_required,
        memory_required,
        disk_required,
        max_latency_ms,
        profile="balanced",
        priority=1
    ):

        self.name = name

        self.cpu_required = cpu_required

        self.memory_required = memory_required

        self.disk_required = disk_required

        self.max_latency_ms = max_latency_ms

        self.profile = profile

        self.priority = priority

        self.allocated_worker = None


    def __str__(self):

        return (
            f"{self.name} | "
            f"CPU: {self.cpu_required} | "
            f"Memória: {self.memory_required}GB | "
            f"Disco: {self.disk_required}GB | "
            f"Latência máxima: {self.max_latency_ms}ms | "
            f"Perfil: {self.profile} | "
            f"Prioridade: {self.priority}"
        )
