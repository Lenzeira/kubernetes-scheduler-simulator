PROFILE_WEIGHTS = {
    "light": {
        "cpu": 0.25,
        "memory": 0.25,
        "disk": 0.20,
        "latency": 0.30
    },
    "balanced": {
        "cpu": 0.30,
        "memory": 0.30,
        "disk": 0.25,
        "latency": 0.15
    },
    "cpu": {
        "cpu": 0.50,
        "memory": 0.20,
        "disk": 0.20,
        "latency": 0.10
    },
    "memory": {
        "cpu": 0.20,
        "memory": 0.50,
        "disk": 0.20,
        "latency": 0.10
    },
    "storage": {
        "cpu": 0.18,
        "memory": 0.17,
        "disk": 0.55,
        "latency": 0.10
    },
    "latency": {
        "cpu": 0.18,
        "memory": 0.17,
        "disk": 0.15,
        "latency": 0.50
    }
}


class BalancedResourceScheduler:

    strict_allocation = True

    def select_worker(self, pod, workers):

        possible_workers = []

        for worker in workers:

            if worker.can_allocate(pod):

                score = self.calculate_score(worker, pod)

                possible_workers.append((score, worker))

        if not possible_workers:

            return None

        possible_workers.sort(key=lambda item: item[0], reverse=True)

        return possible_workers[0][1]


    def calculate_score(self, worker, pod):

        weights = PROFILE_WEIGHTS.get(
            pod.profile,
            PROFILE_WEIGHTS["balanced"]
        )

        future_cpu = worker.used_cpu + pod.cpu_required

        future_memory = worker.used_memory + pod.memory_required

        future_disk = worker.used_disk + pod.disk_required

        cpu_free = (worker.total_cpu - future_cpu) / worker.total_cpu

        memory_free = (worker.total_memory - future_memory) / worker.total_memory

        disk_free = (worker.total_disk - future_disk) / worker.total_disk

        latency_score = 1 - (worker.latency_ms / pod.max_latency_ms)

        return (
            weights["cpu"] * cpu_free +
            weights["memory"] * memory_free +
            weights["disk"] * disk_free +
            weights["latency"] * latency_score
        )


class KubernetesDefaultScheduler:

    strict_allocation = False

    def select_worker(self, pod, workers):

        for worker in workers:

            if worker.can_allocate_default(pod):

                return worker

        return None
