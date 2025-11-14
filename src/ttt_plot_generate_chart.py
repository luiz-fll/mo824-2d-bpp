import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_ttt_plots_from_csv(csv_path: str, output_dir: str):
    """
    Lê um CSV de resultados de experimentos, processa os dados e gera
    os gráficos Time-to-Target (TTT-Plots) para cada combinação
    de instância e valor-alvo.
    """
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV '{csv_path}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return

    if df.empty:
        print("Aviso: O CSV está vazio.")
        return

    df = df.rename(columns={
        'Instancia': 'instance',
        'Valor Alvo': 'target_value'
    })

    df['algorithm'] = df['Construcao'] + " + " + df['Busca']
    df['target_reached'] = (df['Atingiu valor alvo?'] == True)
    
    df['time_to_target'] = pd.to_numeric(df['Tempo até valor alvo'], errors='coerce')
    
    df = df.dropna(subset=['time_to_target'])

    experiments = df[['instance', 'target_value']].drop_duplicates()
    
    if experiments.empty:
        return

    for _, (instance_name, target_value) in experiments.iterrows():
        plt.figure(figsize=(12, 7))
        
        exp_df = df[
            (df['instance'] == instance_name) & 
            (df['target_value'] == target_value)
        ]
        
        algorithms = exp_df['algorithm'].unique()
        
        for alg in algorithms:
            alg_data = exp_df[
                (exp_df['algorithm'] == alg) & 
                (exp_df['target_reached'] == True)
            ]
            
            if alg_data.empty:
                continue

            sorted_times = np.sort(alg_data['time_to_target'])
            num_runs = len(sorted_times)
            
            probabilities = (np.arange(1, num_runs + 1) - 0.5) / num_runs
            
            plot_times = np.insert(sorted_times, 0, 0)
            plot_probs = np.insert(probabilities, 0, 0)
            
            plt.step(plot_times, plot_probs, where='post', label=alg, marker='o', markersize=4, alpha=0.8)
        
        plt.title(f"TTT-Plot para {instance_name}\nAlvo = {target_value}")
        plt.xlabel("Tempo (segundos) - Escala de Log")
        plt.ylabel("Probabilidade de Atingir o Alvo (Distribuição Empírica)")
        plt.xscale('log') 
        plt.grid(True, which="both", linestyle=':', linewidth=0.6)
        
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        
        plt.tight_layout(rect=[0, 0, 1, 1]) 
        
        base_name = os.path.basename(instance_name) 
        file_stem = os.path.splitext(base_name)[0]
        target_str = str(target_value).replace('.', '_')
        
        filename = f"ttt_plot_{file_stem}_target_{target_str}.png"
        save_path = os.path.join(output_dir, filename)
        
        try:
            plt.savefig(save_path)
            print(f"  -> Gráfico salvo em: {save_path}")
        except Exception as e:
            print(f"  -> ERRO ao salvar gráfico: {e}")
            
        plt.close()

if __name__ == "__main__":
    
    arquivo_csv_resultados = "results/resultados_ttt_plot.csv"
    pasta_saida = "results"
    
    generate_ttt_plots_from_csv(arquivo_csv_resultados, pasta_saida)