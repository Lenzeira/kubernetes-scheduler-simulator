from src.pod import Pod
from src.worker import Worker
from src.master import Master
from src.scheduler import BalancedResourceScheduler, KubernetesDefaultScheduler


def test_worker_can_allocate_pod_with_all_metrics():

    worker = Worker(
        "worker-test",
        total_cpu=4,
        total_memory=8,
        total_disk=100,
        latency_ms=10
    )

    pod = Pod(
        "pod-test",
        cpu_required=2,
        memory_required=4,
        disk_required=20,
        max_latency_ms=30,
        profile="balanced",
        priority=1
    )

    assert worker.can_allocate(pod) is True


def test_worker_rejects_pod_when_disk_is_insufficient():

    worker = Worker(
        "worker-test",
        total_cpu=8,
        total_memory=16,
        total_disk=30,
        latency_ms=10
    )

    pod = Pod(
        "pod-storage",
        cpu_required=2,
        memory_required=4,
        disk_required=80,
        max_latency_ms=50,
        profile="storage",
        priority=1
    )

    assert worker.can_allocate(pod) is False


def test_worker_rejects_pod_when_latency_is_too_high():

    worker = Worker(
        "worker-test",
        total_cpu=8,
        total_memory=16,
        total_disk=100,
        latency_ms=80
    )

    pod = Pod(
        "pod-low-latency",
        cpu_required=2,
        memory_required=4,
        disk_required=20,
        max_latency_ms=20,
        profile="latency",
        priority=1
    )

    assert worker.can_allocate(pod) is False


def test_balanced_scheduler_selects_valid_worker():

    workers = [
        Worker("worker-1", total_cpu=4, total_memory=8, total_disk=40, latency_ms=80),
        Worker("worker-2", total_cpu=8, total_memory=16, total_disk=120, latency_ms=10)
    ]

    pod = Pod(
        "pod-api",
        cpu_required=2,
        memory_required=4,
        disk_required=30,
        max_latency_ms=30,
        profile="latency",
        priority=1
    )

    scheduler = BalancedResourceScheduler()

    selected_worker = scheduler.select_worker(pod, workers)

    assert selected_worker is not None
    assert selected_worker.name == "worker-2"


def test_kubernetes_default_scheduler_ignores_disk_and_latency():

    workers = [
        Worker("worker-1", total_cpu=8, total_memory=16, total_disk=30, latency_ms=80)
    ]

    pod = Pod(
        "pod-default-test",
        cpu_required=2,
        memory_required=4,
        disk_required=80,
        max_latency_ms=20,
        profile="storage",
        priority=1
    )

    scheduler = KubernetesDefaultScheduler()

    selected_worker = scheduler.select_worker(pod, workers)

    assert selected_worker is not None
    assert selected_worker.name == "worker-1"


def test_master_registers_pending_pod_with_balanced_scheduler():

    workers = [
        Worker("worker-1", total_cpu=2, total_memory=4, total_disk=20, latency_ms=60)
    ]

    pods = [
        Pod(
            "pod-heavy",
            cpu_required=8,
            memory_required=16,
            disk_required=100,
            max_latency_ms=20,
            profile="balanced",
            priority=1
        )
    ]

    scheduler = BalancedResourceScheduler()

    master = Master(workers, scheduler)

    master.schedule_all(pods)

    assert len(master.pending_pods) == 1
