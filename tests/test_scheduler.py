from src.pod import Pod
from src.worker import Worker
from src.master import Master
from src.scheduler import BalancedResourceScheduler, FirstFitScheduler


def test_worker_can_allocate_pod():

    worker = Worker("worker-test", total_cpu=4, total_memory=8, total_gpu=1)

    pod = Pod("pod-test", cpu_required=2, memory_required=4, gpu_required=0)

    assert worker.can_allocate(pod) is True


def test_worker_cannot_allocate_pod_when_resources_are_insufficient():

    worker = Worker("worker-test", total_cpu=2, total_memory=4, total_gpu=0)

    pod = Pod("pod-heavy", cpu_required=4, memory_required=8, gpu_required=0)

    assert worker.can_allocate(pod) is False


def test_balanced_scheduler_allocates_pod():

    workers = [
        Worker("worker-1", total_cpu=4, total_memory=8, total_gpu=0),
        Worker("worker-2", total_cpu=8, total_memory=16, total_gpu=1)
    ]

    pod = Pod("pod-api", cpu_required=2, memory_required=4, gpu_required=0)

    scheduler = BalancedResourceScheduler()

    selected_worker = scheduler.select_worker(pod, workers)

    assert selected_worker is not None


def test_first_fit_scheduler_uses_first_available_worker():

    workers = [
        Worker("worker-1", total_cpu=4, total_memory=8, total_gpu=0),
        Worker("worker-2", total_cpu=8, total_memory=16, total_gpu=1)
    ]

    pod = Pod("pod-api", cpu_required=2, memory_required=4, gpu_required=0)

    scheduler = FirstFitScheduler()

    selected_worker = scheduler.select_worker(pod, workers)

    assert selected_worker.name == "worker-1"


def test_master_registers_pending_pod():

    workers = [
        Worker("worker-1", total_cpu=2, total_memory=2, total_gpu=0)
    ]

    pods = [
        Pod("pod-heavy", cpu_required=8, memory_required=16, gpu_required=1)
    ]

    scheduler = BalancedResourceScheduler()

    master = Master(workers, scheduler)

    master.schedule_all(pods)

    assert len(master.pending_pods) == 1
