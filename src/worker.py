class Worker:

    def __init__(self, name, total_cpu, total_memory, total_disk, latency_ms):

        self.name = name

        self.total_cpu = total_cpu

        self.total_memory = total_memory

        self.total_disk = total_disk

        self.latency_ms = latency_ms

        self.used_cpu = 0

        self.used_memory = 0

        self.used_disk = 0

        self.pods = []

        self.policy_violations = []


    def can_allocate(self, pod):

        return (
            self.used_cpu + pod.cpu_required <= self.total_cpu and
            self.used_memory + pod.memory_required <= self.total_memory and
            self.used_disk + pod.disk_required <= self.total_disk and
            self.latency_ms <= pod.max_latency_ms
        )


    def can_allocate_default(self, pod):

        return (
            self.used_cpu + pod.cpu_required <= self.total_cpu and
            self.used_memory + pod.memory_required <= self.total_memory
        )


    def allocate_pod(self, pod, strict=True):

        if strict:

            can_allocate = self.can_allocate(pod)

        else:

            can_allocate = self.can_allocate_default(pod)

        if not can_allocate:

            return False

        self.used_cpu += pod.cpu_required

        self.used_memory += pod.memory_required

        self.used_disk += pod.disk_required

        self.pods.append(pod)

        pod.allocated_worker = self.name

        if self.used_disk > self.total_disk:

            self.policy_violations.append(
                f"{pod.name}: uso de disco acima da capacidade do Worker"
            )

        if self.latency_ms > pod.max_latency_ms:

            self.policy_violations.append(
                f"{pod.name}: latência do Worker acima do limite do POD"
            )

        return True


    def cpu_usage_percent(self):

        return (self.used_cpu / self.total_cpu) * 100


    def memory_usage_percent(self):

        return (self.used_memory / self.total_memory) * 100


    def disk_usage_percent(self):

        return (self.used_disk / self.total_disk) * 100


    def __str__(self):

        return (
            f"{self.name} | "
            f"CPU: {self.used_cpu}/{self.total_cpu} | "
            f"Memória: {self.used_memory}/{self.total_memory}GB | "
            f"Disco: {self.used_disk}/{self.total_disk}GB | "
            f"Latência: {self.latency_ms}ms | "
            f"PODs: {len(self.pods)}"
        )
