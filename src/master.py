class Master:

    def __init__(self, workers, scheduler):

        self.workers = workers

        self.scheduler = scheduler

        self.allocated_pods = []

        self.pending_pods = []


    def schedule_pod(self, pod):

        selected_worker = self.scheduler.select_worker(pod, self.workers)

        if selected_worker is None:

            self.pending_pods.append(pod)

            return False

        selected_worker.allocate_pod(pod)

        self.allocated_pods.append(pod)

        return True


    def schedule_all(self, pods):

        pods_sorted = sorted(
            pods,
            key=lambda pod: pod.priority,
            reverse=True
        )

        for pod in pods_sorted:

            self.schedule_pod(pod)
