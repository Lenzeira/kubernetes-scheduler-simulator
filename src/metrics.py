def _bar(percent, width=20):
    visual_percent = min(max(percent, 0), 100)
    filled = int(visual_percent / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent:5.1f}%"


def show_workers_status(workers):

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                    STATUS DOS WORKERS                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    for worker in workers:

        cpu_pct = worker.cpu_usage_percent()
        mem_pct = worker.memory_usage_percent()
        disk_pct = worker.disk_usage_percent()

        print(f"\n  ┌─ {worker.name}  (latência: {worker.latency_ms}ms)")
        print(f"  │  CPU     {_bar(cpu_pct)}  {worker.used_cpu}/{worker.total_cpu} cores")
        print(f"  │  Memória {_bar(mem_pct)}  {worker.used_memory}/{worker.total_memory} GB")
        print(f"  │  Disco   {_bar(disk_pct)}  {worker.used_disk}/{worker.total_disk} GB")

        if worker.pods:
            pod_names = ", ".join(pod.name for pod in worker.pods)
            print(f"  │  PODs ({len(worker.pods)}): {pod_names}")
        else:
            print("  │  PODs: nenhum alocado")

        print(f"  └{'─' * 60}")


def show_pending_pods(pending_pods):

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                      PODS PENDENTES                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    if not pending_pods:
        print("  ✔  Nenhum POD pendente.")
        return

    for pod in pending_pods:
        print(f"  ✘  {pod}")


def show_statistics(workers, allocated_pods, pending_pods):

    total_pods = len(allocated_pods) + len(pending_pods)
    allocated_count = len(allocated_pods)
    pending_count = len(pending_pods)
    allocation_rate = (allocated_count / total_pods * 100) if total_pods > 0 else 0

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                    ESTATÍSTICAS GERAIS                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"  Total de PODs processados : {total_pods}")
    print(f"  PODs alocados             : {allocated_count}")
    print(f"  PODs pendentes            : {pending_count}")
    print(f"  Taxa de alocação          : {allocation_rate:.2f}%")

    print("\n  USO DE RECURSOS POR WORKER")
    header = f"  {'Worker':<12} {'CPU':>7} {'Memória':>9} {'Disco':>7} {'Latência':>10} {'PODs':>5}"
    print(header)
    print("  " + "─" * (len(header) - 2))

    for worker in workers:
        print(
            f"  {worker.name:<12} "
            f"{worker.cpu_usage_percent():>6.1f}% "
            f"{worker.memory_usage_percent():>8.1f}% "
            f"{worker.disk_usage_percent():>6.1f}% "
            f"{worker.latency_ms:>8}ms "
            f"{len(worker.pods):>5}"
        )

    if workers:
        avg_cpu = sum(worker.cpu_usage_percent() for worker in workers) / len(workers)
        avg_mem = sum(worker.memory_usage_percent() for worker in workers) / len(workers)
        avg_disk = sum(worker.disk_usage_percent() for worker in workers) / len(workers)

        print("  " + "─" * (len(header) - 2))
        print(f"  {'Média':<12} {avg_cpu:>6.1f}% {avg_mem:>8.1f}% {avg_disk:>6.1f}%")

    all_violations = [
        f"{worker.name}: {violation}"
        for worker in workers
        for violation in worker.policy_violations
    ]

    print("\n  VIOLAÇÕES DE MÉTRICAS EXTRAS")
    if not all_violations:
        print("  ✔  Nenhuma violação registrada.")
    else:
        for violation in all_violations:
            print(f"  ✘  {violation}")
