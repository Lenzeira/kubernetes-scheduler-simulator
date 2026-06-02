class BalancedResourceScheduler:

    def select_worker(self, pod, workers):

        possible_workers = []

        for worker in workers:

            if worker.can_allocate(pod):

                score = self.calculate_score(worker, pod)

                possible_workers.append((score, worker))

        if not possible_workers:

            return None

        possible_workers.sort(key=lambda item: item[0])

        return possible_workers[0][1]


    def calculate_score(self, worker, pod):

        future_cpu = worker.used_cpu + pod.cpu_required

        future_memory = worker.used_memory + pod.memory_required

        future_gpu = worker.used_gpu + pod.gpu_required

        cpu_usage = future_cpu / worker.total_cpu

        memory_usage = future_memory / worker.total_memory

        if worker.total_gpu > 0:

            gpu_usage = future_gpu / worker.total_gpu

        else:

            gpu_usage = 0

        average_usage = (cpu_usage + memory_usage + gpu_usage) / 3

        imbalance = (
            abs(cpu_usage - average_usage) +
            abs(memory_usage - average_usage) +
            abs(gpu_usage - average_usage)
        )

        return imbalance
