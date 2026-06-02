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

        cpu_usage = (worker.used_cpu / worker.total_cpu) * 100

        memory_usage = (worker.used_memory / worker.total_memory) * 100

        if worker.total_gpu > 0:

            gpu_usage = (worker.used_gpu / worker.total_gpu) * 100

        else:

            gpu_usage = 0

        print(
            f"{worker.name}: "
            f"CPU {cpu_usage:.2f}% | "
            f"Memória {memory_usage:.2f}% | "
            f"GPU {gpu_usage:.2f}%"
        )
