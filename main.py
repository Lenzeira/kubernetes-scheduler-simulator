import json

from src.pod import Pod
from src.worker import Worker
from src.master import Master
from src.scheduler import BalancedResourceScheduler, FirstFitScheduler
from src.metrics import (
    show_workers_status,
    show_pending_pods,
    show_statistics
)


def load_workers(file_path):

    with open(file_path, "r", encoding="utf-8") as file:

        workers_data = json.load(file)

    return [
        Worker(
            worker["name"],
            worker["total_cpu"],
            worker["total_memory"],
            worker["total_gpu"]
        )
        for worker in workers_data
    ]


def load_pods(file_path):

    with open(file_path, "r", encoding="utf-8") as file:

        pods_data = json.load(file)

    return [
        Pod(
            pod["name"],
            pod["cpu_required"],
            pod["memory_required"],
            pod["gpu_required"],
            pod["priority"]
        )
        for pod in pods_data
    ]


def run_simulation(title, scheduler):

    workers = load_workers("config/workers.json")

    pods = load_pods("config/pods.json")

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
