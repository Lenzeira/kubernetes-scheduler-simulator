from src.pod import Pod
from src.worker import Worker
from src.master import Master
from src.scheduler import BalancedResourceScheduler, FirstFitScheduler
from src.metrics import (
    show_workers_status,
    show_pending_pods,
    show_statistics
)


def create_workers():

    return [
        Worker("worker-1", total_cpu=8, total_memory=16, total_gpu=1),
        Worker("worker-2", total_cpu=4, total_memory=8, total_gpu=0),
        Worker("worker-3", total_cpu=12, total_memory=32, total_gpu=2),
    ]


def create_pods():

    return [
        Pod("pod-api", cpu_required=2, memory_required=4, gpu_required=0, priority=2),
        Pod("pod-database", cpu_required=4, memory_required=8, gpu_required=0, priority=3),
        Pod("pod-ai-training", cpu_required=6, memory_required=16, gpu_required=1, priority=5),
        Pod("pod-cache", cpu_required=1, memory_required=2, gpu_required=0, priority=1),
        Pod("pod-monitoring", cpu_required=2, memory_required=2, gpu_required=0, priority=2),
        Pod("pod-heavy-gpu", cpu_required=8, memory_required=24, gpu_required=2, priority=4),
        Pod("pod-small-job", cpu_required=1, memory_required=1, gpu_required=0, priority=1),
        Pod("pod-report", cpu_required=3, memory_required=6, gpu_required=0, priority=2),
    ]


def run_simulation(title, scheduler):

    workers = create_workers()

    pods = create_pods()

    master = Master(workers, scheduler)

    print(f"\n\n==============================")
    print(title)
    print(f"==============================")

    master.schedule_all(pods)

    show_workers_status(workers)

    show_pending_pods(master.pending_pods)

    show_statistics(
        workers,
        master.allocated_pods,
        master.pending_pods
    )


def main():

    run_simulation(
        "SIMULAÇÃO COM ESCALONADOR BALANCEADO",
        BalancedResourceScheduler()
    )

    run_simulation(
        "SIMULAÇÃO COM FIRST FIT",
        FirstFitScheduler()
    )


if __name__ == "__main__":

    main()
