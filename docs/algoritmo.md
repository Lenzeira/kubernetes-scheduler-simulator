# Algoritmo de escalonamento

O algoritmo principal do projeto é o BalancedResourceScheduler.

Ele foi criado para distribuir PODs entre os Workers considerando mais métricas do que uma estratégia baseada apenas em CPU e memória.

## Métricas consideradas

O escalonador proposto considera quatro métricas:

- CPU
- memória
- disco
- latência

Essas métricas ajudam a avaliar se um Worker realmente é adequado para receber determinado POD.

## Funcionamento geral

Para cada POD, o algoritmo segue esta lógica:

1. recebe o POD;
2. verifica quais Workers possuem recursos suficientes;
3. elimina Workers que não respeitam CPU, memória, disco ou latência;
4. calcula uma pontuação para cada Worker viável;
5. escolhe o Worker com melhor pontuação;
6. aloca o POD ou registra como pendente.

## Comparação com o escalonador padrão

O KubernetesDefaultScheduler considera apenas CPU e memória.

Na simulação atual, ele alocou mais PODs, mas gerou violações de disco e latência. Já o escalonador proposto foi mais restritivo, porém respeitou todas as métricas adicionais.
