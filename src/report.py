def _bar_text(percent, width=15):
    visual_percent = min(max(percent, 0), 100)
    filled = int(visual_percent / 100 * width)
    return "█" * filled + "░" * (width - filled)


def generate_report(file_path, simulation_results):

    with open(file_path, "w", encoding="utf-8") as f:

        f.write("RELATÓRIO DA SIMULAÇÃO DE ESCALONAMENTO\n")
        f.write("=" * 60 + "\n\n")

        for result in simulation_results:

            f.write(f"{result['title']}\n")
            f.write("-" * 60 + "\n")

            f.write(f"Total de PODs     : {result['total_pods']}\n")
            f.write(f"PODs alocados     : {result['allocated_pods']}\n")
            f.write(f"PODs pendentes    : {result['pending_pods']}\n")
            f.write(f"Taxa de alocação  : {result['allocation_rate']:.2f}%\n")

            f.write("\nUso dos Workers:\n")
            f.write(
                f"  {'Worker':<12} "
                f"{'CPU':>7} "
                f"{'Memória':>9} "
                f"{'Disco':>7} "
                f"{'Latência':>10} "
                f"{'PODs':>5}\n"
            )
            f.write("  " + "─" * 50 + "\n")

            cpu_vals = []
            mem_vals = []
            disk_vals = []

            for worker in result["workers"]:
                cpu_vals.append(worker["cpu_usage"])
                mem_vals.append(worker["memory_usage"])
                disk_vals.append(worker["disk_usage"])

                f.write(
                    f"  {worker['name']:<12} "
                    f"{worker['cpu_usage']:>6.1f}% "
                    f"{worker['memory_usage']:>8.1f}% "
                    f"{worker['disk_usage']:>6.1f}% "
                    f"{worker['latency_ms']:>8}ms "
                    f"{len(worker['pods']):>5}\n"
                )

                f.write(
                    f"  {'':12}  CPU  [{_bar_text(worker['cpu_usage'])}]\n"
                    f"  {'':12}  MEM  [{_bar_text(worker['memory_usage'])}]\n"
                    f"  {'':12}  DSK  [{_bar_text(worker['disk_usage'])}]\n"
                )

                pods_str = ", ".join(worker["pods"]) if worker["pods"] else "nenhum"
                f.write(f"  {'':12}  PODs: {pods_str}\n\n")

            total_workers = len(result["workers"])

            if total_workers:
                f.write("  " + "─" * 50 + "\n")
                f.write(
                    f"  {'Média':<12} "
                    f"{sum(cpu_vals) / total_workers:>6.1f}% "
                    f"{sum(mem_vals) / total_workers:>8.1f}% "
                    f"{sum(disk_vals) / total_workers:>6.1f}%\n"
                )
                f.write(
                    f"  {'Máximo':<12} "
                    f"{max(cpu_vals):>6.1f}% "
                    f"{max(mem_vals):>8.1f}% "
                    f"{max(disk_vals):>6.1f}%\n"
                )
                f.write(
                    f"  {'Mínimo':<12} "
                    f"{min(cpu_vals):>6.1f}% "
                    f"{min(mem_vals):>8.1f}% "
                    f"{min(disk_vals):>6.1f}%\n\n"
                )

            f.write("PODs pendentes:\n")
            if result["pending_names"]:
                for name in result["pending_names"]:
                    f.write(f"  - {name}\n")
            else:
                f.write("  - Nenhum POD pendente\n")

            f.write("\nViolações de métricas extras:\n")
            if result["violations"]:
                for violation in result["violations"]:
                    f.write(f"  - {violation}\n")
            else:
                f.write("  - Nenhuma violação registrada\n")

            f.write("\n\n")

        if len(simulation_results) == 2:
            proposed_result = simulation_results[0]
            default_result = simulation_results[1]

            f.write("=" * 60 + "\n")
            f.write("COMPARAÇÃO ENTRE ESCALONADORES\n")
            f.write("=" * 60 + "\n\n")

            col = 28

            f.write(
                f"  {'Métrica':<25} "
                f"{'Proposto':>{col}} "
                f"{'Kubernetes Padrão':>{col}}\n"
            )
            f.write("  " + "─" * (25 + col * 2 + 2) + "\n")

            rows = [
                (
                    "PODs alocados",
                    proposed_result["allocated_pods"],
                    default_result["allocated_pods"]
                ),
                (
                    "PODs pendentes",
                    proposed_result["pending_pods"],
                    default_result["pending_pods"]
                ),
                (
                    "Taxa de alocação",
                    f"{proposed_result['allocation_rate']:.2f}%",
                    f"{default_result['allocation_rate']:.2f}%"
                ),
                (
                    "Violações",
                    len(proposed_result["violations"]),
                    len(default_result["violations"])
                )
            ]

            for label, proposed_value, default_value in rows:
                f.write(
                    f"  {label:<25} "
                    f"{str(proposed_value):>{col}} "
                    f"{str(default_value):>{col}}\n"
                )

            def average_usage(result, key):
                values = [worker[key] for worker in result["workers"]]

                if not values:
                    return 0

                return sum(values) / len(values)

            usage_rows = [
                ("Média CPU workers", "cpu_usage"),
                ("Média Memória workers", "memory_usage"),
                ("Média Disco workers", "disk_usage")
            ]

            for label, key in usage_rows:
                proposed_value = f"{average_usage(proposed_result, key):.1f}%"
                default_value = f"{average_usage(default_result, key):.1f}%"

                f.write(
                    f"  {label:<25} "
                    f"{proposed_value:>{col}} "
                    f"{default_value:>{col}}\n"
                )

            f.write("\nConclusão:\n")
            f.write(
                "  O escalonador proposto considera CPU, memória, disco e latência,\n"
                "  evitando violações de recursos. O escalonador padrão do Kubernetes\n"
                "  considera apenas CPU e memória, podendo gerar alocações inválidas\n"
                "  em disco e latência, como demonstrado pelas violações acima.\n"
            )
