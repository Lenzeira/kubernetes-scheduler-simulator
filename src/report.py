def generate_report(file_path, simulation_results):

    with open(file_path, "w", encoding="utf-8") as file:

        file.write("RELATÓRIO DA SIMULAÇÃO DE ESCALONAMENTO\n")
        file.write("=" * 50)
        file.write("\n\n")

        for result in simulation_results:

            file.write(f"{result['title']}\n")
            file.write("-" * 50)
            file.write("\n")

            file.write(f"Total de PODs: {result['total_pods']}\n")
            file.write(f"PODs alocados: {result['allocated_pods']}\n")
            file.write(f"PODs pendentes: {result['pending_pods']}\n")
            file.write(f"Taxa de alocação: {result['allocation_rate']:.2f}%\n")

            file.write("\nUso dos Workers:\n")

            for worker in result["workers"]:

                file.write(
                    f"- {worker['name']}: "
                    f"CPU {worker['cpu_usage']:.2f}% | "
                    f"Memória {worker['memory_usage']:.2f}% | "
                    f"Disco {worker['disk_usage']:.2f}% | "
                    f"Latência {worker['latency_ms']}ms\n"
                )

                file.write("  PODs: ")

                if worker["pods"]:

                    file.write(", ".join(worker["pods"]))

                else:

                    file.write("nenhum")

                file.write("\n")

            file.write("\nPODs pendentes:\n")

            if result["pending_names"]:

                for pod_name in result["pending_names"]:

                    file.write(f"- {pod_name}\n")

            else:

                file.write("- Nenhum POD pendente\n")

            file.write("\nViolações de métricas extras:\n")

            if result["violations"]:

                for violation in result["violations"]:

                    file.write(f"- {violation}\n")

            else:

                file.write("- Nenhuma violação registrada\n")

            file.write("\n\n")
