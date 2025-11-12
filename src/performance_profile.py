import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

GRASP_CSV_PATH = 'results/resultados_grasp.csv'
HEURISTICS_CSV_PATH = 'results/resultados_heuristicas.csv'
OUTPUT_FILENAME = "results/performance_profile.png"

all_data_frames = []
try:
    df_grasp = pd.read_csv(GRASP_CSV_PATH)
    
    df_grasp['algorithm'] = df_grasp['Construcao'] + '-' + df_grasp['Busca']
    
    df_grasp = df_grasp.rename(columns={'Instancia': 'instance', 'Bins': 'metric_value'})
    
    df_grasp['metric_value'] = pd.to_numeric(df_grasp['metric_value'], errors='coerce')
    df_grasp = df_grasp.dropna(subset=['metric_value'])
    
    all_data_frames.append(df_grasp[['instance', 'algorithm', 'metric_value']])
    print(f"Dados GRASP (de {GRASP_CSV_PATH}) carregados com sucesso.")

except FileNotFoundError:
    print(f"AVISO: Arquivo GRASP não encontrado em: {GRASP_CSV_PATH}")
except Exception as e:
    print(f"Um erro ocorreu ao ler o CSV do GRASP: {e}")

try:
    df_heuristics = pd.read_csv(HEURISTICS_CSV_PATH)
    
    df_heuristics = df_heuristics.rename(columns={
        'Instancia': 'instance',
        'Metodo': 'algorithm',
        'Bins': 'metric_value'
    })
    
    if pd.api.types.is_string_dtype(df_heuristics['metric_value']):
        df_heuristics = df_heuristics[df_heuristics['metric_value'].str.upper() != 'INVIÁVEL']

    df_heuristics['metric_value'] = pd.to_numeric(df_heuristics['metric_value'], errors='coerce')
    
    # Remover quaisquer linhas que falharam na conversão (viraram NaN)
    df_heuristics = df_heuristics.dropna(subset=['metric_value'])

    all_data_frames.append(df_heuristics[['instance', 'algorithm', 'metric_value']])
    print(f"Dados de Heurísticas (de {HEURISTICS_CSV_PATH}) carregados com sucesso.")

except FileNotFoundError:
    print(f"AVISO: Arquivo de Heurísticas não encontrado em: {HEURISTICS_CSV_PATH}")
except Exception as e:
    print(f"Um erro ocorreu ao ler o CSV de Heurísticas: {e}")


if not all_data_frames:
    print("ERRO CRÍTICO: Nenhum arquivo de dados foi carregado. Saindo.")
    raise SystemExit("Nenhum dado encontrado para processar.")

# Combinar todos os dataframes carregados em um só
data_to_plot = pd.concat(all_data_frames, ignore_index=True)

best_overall = data_to_plot.groupby('instance')['metric_value'].min().reset_index()
best_overall = best_overall.rename(columns={'metric_value': 'best_value_overall'})

merged_data = pd.merge(data_to_plot, best_overall, on='instance')

# Calcular a taxa de desempenho (ratio) para MINIMIZAÇÃO
merged_data['ratio'] = merged_data['metric_value'] / merged_data['best_value_overall']

# Lidar com casos especiais
merged_data['ratio'] = merged_data['ratio'].replace([np.inf, -np.inf], np.nan)
merged_data.loc[(merged_data['best_value_overall'] == 0) & (merged_data['metric_value'] == 0), 'ratio'] = 1
merged_data = merged_data.fillna(np.inf) 

# Preparar para o plot
algorithms = sorted(merged_data['algorithm'].unique())
num_instances = merged_data['instance'].nunique()
instance_counts = merged_data.groupby('algorithm')['instance'].nunique()

print(f"\nPerfil baseado em {num_instances} instâncias únicas.")
print("Contagem de instâncias por algoritmo:")
print(instance_counts)

# Definir o range de tau (τ)
finite_ratios = merged_data[merged_data['ratio'] != np.inf]['ratio']
if finite_ratios.empty:
    max_ratio = 2.0
else:
    max_ratio = finite_ratios.max()

plot_max_tau = max(2.0, max_ratio)
tau_range = np.linspace(1, plot_max_tau, 200)

plt.figure(figsize=(10, 7))

for alg in algorithms:
    # Obter as taxas para este algoritmo
    alg_ratios = merged_data[merged_data['algorithm'] == alg]['ratio']
    num_runs_for_alg = len(alg_ratios)
    
    if num_runs_for_alg == 0:
        continue

    # Calcular a probabilidade cumulativa: P(ratio <= tau)
    probabilities = [
        (alg_ratios <= tau).sum() / num_instances for tau in tau_range
    ]
    
    label_text = f"{alg} (N={instance_counts.get(alg, 0)})"
    plt.plot(tau_range, probabilities, label=label_text, linewidth=2)

# O seu código usava 'Bins' como a métrica, então ajustei os títulos
plt.title("Perfil de Desempenho (Métrica: Bins)", fontsize=16)
plt.xlabel("Taxa de Desempenho (τ)", fontsize=12)
plt.ylabel(f"P(Bins / Bins_Mínimo ≤ τ) (Total N={num_instances})", fontsize=12)
plt.grid(True, linestyle=':', linewidth=0.7)
plt.legend(loc='lower right', fontsize=10, title="Algoritmo (N=instâncias)")
plt.xlim(1, plot_max_tau)
plt.ylim(0, 1.05)
plt.tight_layout()

# Salvar o gráfico
plt.savefig(OUTPUT_FILENAME)
plt.close()

print(f"\nGráfico de Perfil de Desempenho salvo como: {OUTPUT_FILENAME}")