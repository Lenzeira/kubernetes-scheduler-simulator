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
from src.report import generate_report


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


def build_result(title, workers, allocated_pods, pending_pods):

    total_pods = len(allocated_pods) + len(pending_pods)

    allocated_count = len(allocated_pods)

    pending_count = len(pending_pods)

    if total_pods > 0:

        allocation_rate = (allocated_count / total_pods) * 100

    else:

        allocation_rate = 0

    workers_usage = []

    for worker in workers:

        cpu_usage = (worker.used_cpu / worker.total_cpu) * 100

        memory_usage = (worker.used_memory / worker.total_memory) * 100

        if worker.total_gpu > 0:

            gpu_usage = (worker.used_gpu / worker.total_gpu) * 100

        else:

            gpu_usage = 0

        workers_usage.append({
            "name": worker.name,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "gpu_usage": gpu_usage
        })

    return {
        "title": title,
        "total_pods": total_pods,
        "allocated_pods": allocated_count,
        "pending_pods": pending_count,
        "allocation_rate": allocation_rate,
        "workers": workers_usage,
        "pending_names": [pod.name for pod in pending_pods]
    }


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

    return build_result(
        title,
        workers,
        master.allocated_pods,
        master.pending_pods
    )


def main():

    simulation_results = []

    simulation_results.append(
        run_simulation(
            "SIMULAÇÃO COM ESCALONADOR BALANCEADO",
            BalancedResourceScheduler()
        )
    )

    simulation_results.append(
        run_simulation(
            "SIMULAÇÃO COM FIRST FIT",
            FirstFitScheduler()
        )
    )

    generate_report(
        "reports/resultados.txt",
        simulation_results
    )

    print("\nRelatório gerado em reports/resultados.txt")


if __name__ == "__main__":

    main()
