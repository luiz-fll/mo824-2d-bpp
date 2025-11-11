import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_FILE_PATH = 'results/resultados_grasp.csv'
OUTPUT_FILENAME = "results/performance_profile.png"

try:
    df = pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado no caminho: {CSV_FILE_PATH}")
    raise
except Exception as e:
    print(f"Um erro ocorreu ao ler o CSV: {e}")
    raise

df['algorithm'] = df['Construcao'] + '-' + df['Busca']
df = df.rename(columns={'Instancia': 'instance', 'Bins': 'metric_value'})
data_to_plot = df[['instance', 'algorithm', 'metric_value']]

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

# Formatar o gráfico
plt.title("Perfil de Desempenho (Métrica: Tempo(s))", fontsize=16)
plt.xlabel("Taxa de Desempenho (τ)", fontsize=12)
plt.ylabel(f"P(Tempo / Tempo_Mínimo ≤ τ) (Total N={num_instances})", fontsize=12)
plt.grid(True, linestyle=':', linewidth=0.7)
plt.legend(loc='lower right', fontsize=10, title="Algoritmo (N=instâncias)")
plt.xlim(1, plot_max_tau)
plt.ylim(0, 1.05)
plt.tight_layout()

# Salvar o gráfico
plt.savefig(OUTPUT_FILENAME)
plt.close()

print(f"\nGráfico de Perfil de Desempenho salvo como: {OUTPUT_FILENAME}")