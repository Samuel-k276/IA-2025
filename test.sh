#!/bin/bash

# Script para testar todos os arquivos de teste e medir o tempo de execução
# Grupo 84: João Matreno (110246), Samuel Gomes (110274)

echo "=== NURUOMINO TEST SUITE ==="
echo "Testando todos os casos de teste disponíveis..."
echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
total_tests=0
passed_tests=0
failed_tests=0
total_time=0

# Arrays para armazenar resultados
declare -a test_names
declare -a test_times
declare -a test_results

# Função para executar um teste
run_test() {
    local test_file=$1
    local expected_file=$2
    local test_name=$(basename "$test_file" .txt)
    
    echo -n "Testando $test_name... "
    
    # Medir tempo de execução
    start_time=$(date +%s.%N)
    
    # Executar o programa e capturar saída
    if timeout 60s python3 nuruomino.py < "$test_file" > "output_${test_name}.tmp" 2>&1; then
        end_time=$(date +%s.%N)
        execution_time=$(echo "$end_time - $start_time" | bc -l)
        
        # Verificar se existe arquivo de saída esperada
        if [ -f "$expected_file" ]; then
            if diff -q "output_${test_name}.tmp" "$expected_file" > /dev/null; then
                echo "PASSOU"
                test_results+=("PASSOU")
                ((passed_tests++))
            else
                echo "FALHOU"
                test_results+=("FALHOU")
                ((failed_tests++))
            fi
        else
            echo "SEM VERIFICAÇÃO"
            test_results+=("SEM VERIFICAÇÃO")
        fi
        
        # Armazenar resultados
        test_names+=("$test_name")
        test_times+=("$execution_time")
        
        # Adicionar ao tempo total
        total_time=$(echo "$total_time + $execution_time" | bc -l)
        
    else
        end_time=$(date +%s.%N)
        execution_time=$(echo "$end_time - $start_time" | bc -l)
        echo "TIMEOUT/ERRO"
        test_names+=("$test_name")
        test_times+=("$execution_time")
        test_results+=("TIMEOUT")
        ((failed_tests++))
    fi
    
    # Limpar arquivo temporário
    rm -f "output_${test_name}.tmp"
    
    ((total_tests++))
}

# Verificar se o programa existe
if [ ! -f "nuruomino.py" ]; then
    echo -e "${RED}Erro: nuruomino.py não encontrado!${NC}"
    exit 1
fi

# Verificar se bc está instalado (para cálculos de tempo)
if ! command -v bc &> /dev/null; then
    echo -e "${YELLOW}Aviso: bc não está instalado. Tempos podem não ser calculados corretamente.${NC}"
fi

# Mudar para o diretório do script
cd "$(dirname "$0")"

# Executar todos os testes
echo "Procurando arquivos de teste em sample-nuruominoboards/..."
echo

for test_file in sample-nuruominoboards/test*.txt; do
    if [ -f "$test_file" ]; then
        # Determinar nome do teste
        test_base=$(basename "$test_file" .txt)
        
        # Pular testes específicos
        if [[ "$test_base" == "test05" || "$test_base" == "test09" ]]; then
            echo "Pulando $test_base..."
            continue
        fi
        
        # Determinar arquivo de saída esperada
        expected_file="sample-nuruominoboards/${test_base}.out"
        
        run_test "$test_file" "$expected_file"
    fi
done

# Estatísticas finais
echo
echo "=== RESULTADOS ==="
echo
printf "%-12s %-12s %-10s\n" "TESTE" "TEMPO(s)" "RESULTADO"
printf "%-12s %-12s %-10s\n" "--------" "--------" "---------"

for i in "${!test_names[@]}"; do
    # Formatar tempo de forma simples
    time_value=${test_times[$i]}
    time_rounded=$(echo "$time_value" | cut -d'.' -f1-2 | sed 's/$/s/')
    printf "%-12s %-12s %-10s\n" "${test_names[$i]}" "$time_rounded" "${test_results[$i]}"
done

echo
echo -e "Total de testes: ${BLUE}$total_tests${NC}"
echo -e "Testes passou: ${GREEN}$passed_tests${NC}"
echo -e "Testes falharam: ${RED}$failed_tests${NC}"

if [ $total_tests -gt 0 ]; then
    success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc -l)
    echo -e "Taxa de sucesso: ${success_rate}%"
fi

if command -v bc &> /dev/null; then
    average_time=$(echo "scale=3; $total_time / $total_tests" | bc -l)
    echo -e "Tempo total: ${total_time}s"
    echo -e "Tempo médio por teste: ${average_time}s"
fi

echo
if [ $failed_tests -eq 0 ] && [ $passed_tests -gt 0 ]; then
    echo -e "${GREEN}🎉 Todos os testes passaram!${NC}"
    exit 0
elif [ $passed_tests -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Alguns testes falharam.${NC}"
    exit 1
else
    echo -e "${RED}❌ Nenhum teste passou.${NC}"
    exit 2
fi