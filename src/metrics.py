def show_workers_status(workers):

    print("\n=== STATUS DOS WORKERS ===")

    for worker in workers:

        print(f"\n{worker}")

        if worker.pods:

            for pod in worker.pods:

                print(f"  - {pod.name}")

        else:

            print("  - Nenhum POD alocado")


def show_pending_pods(pending_pods):

    print("\n=== PODS PENDENTES ===")

    if not pending_pods:

        print("Nenhum POD pendente.")

        return

    for pod in pending_pods:

        print(f"  - {pod}")


def show_statistics(workers, allocated_pods, pending_pods):

    total_pods = len(allocated_pods) + len(pending_pods)

    allocated_count = len(allocated_pods)

    pending_count = len(pending_pods)

    if total_pods > 0:

        allocation_rate = (allocated_count / total_pods) * 100

    else:

        allocation_rate = 0

    print("\n=== ESTATÍSTICAS GERAIS ===")

    print(f"Total de PODs processados: {total_pods}")

    print(f"PODs alocados: {allocated_count}")

    print(f"PODs pendentes: {pending_count}")

    print(f"Taxa de alocação: {allocation_rate:.2f}%")

    print("\n=== USO DE RECURSOS POR WORKER ===")

    for worker in workers:

        print(
            f"{worker.name}: "
            f"CPU {worker.cpu_usage_percent():.2f}% | "
            f"Memória {worker.memory_usage_percent():.2f}% | "
            f"Disco {worker.disk_usage_percent():.2f}% | "
            f"Latência {worker.latency_ms}ms"
        )

    total_violations = []

    for worker in workers:

        for violation in worker.policy_violations:

            total_violations.append(f"{worker.name}: {violation}")

    print("\n=== VIOLAÇÕES DE MÉTRICAS EXTRAS ===")

    if not total_violations:

        print("Nenhuma violação registrada.")

    else:

        for violation in total_violations:

            print(f"- {violation}")
