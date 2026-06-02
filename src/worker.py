class Worker:

    def __init__(self, name, total_cpu, total_memory, total_gpu=0):

        self.name = name

        self.total_cpu = total_cpu

        self.total_memory = total_memory

        self.total_gpu = total_gpu

        self.used_cpu = 0

        self.used_memory = 0

        self.used_gpu = 0

        self.pods = []


    def can_allocate(self, pod):

        return (
            self.used_cpu + pod.cpu_required <= self.total_cpu and
            self.used_memory + pod.memory_required <= self.total_memory and
            self.used_gpu + pod.gpu_required <= self.total_gpu
        )


    def allocate_pod(self, pod):

        if self.can_allocate(pod):

            self.used_cpu += pod.cpu_required

            self.used_memory += pod.memory_required

            self.used_gpu += pod.gpu_required

            self.pods.append(pod)

            pod.allocated_worker = self.name

            return True

        return False


    def __str__(self):

        return (
            f"{self.name} | "
            f"CPU: {self.used_cpu}/{self.total_cpu} | "
            f"Memória: {self.used_memory}/{self.total_memory}GB | "
            f"GPU: {self.used_gpu}/{self.total_gpu} | "
            f"PODs: {len(self.pods)}"
        )
