import json
import os

# Define o nome do arquivo que guardará as pontuações
SCORE_FILE = "scores.json"


def load_scores():
    """Carrega as pontuações do arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
    # Garante que o arquivo exista
    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Se o arquivo estiver vazio ou corrompido, retorna uma lista vazia
        return []


def save_scores(scores_list):
    """Salva a lista de pontuações no arquivo JSON."""
    with open(SCORE_FILE, 'w') as f:
        # 'indent=4' deixa o arquivo JSON bem formatado e legível
        json.dump(scores_list, f, indent=4)


def add_score(new_score: dict):
    """Adiciona uma nova pontuação, ordena a lista e salva."""
    # Carrega as pontuações existentes
    scores = load_scores()

    # Adiciona a nova pontuação à lista
    scores.append(new_score)

    # Ordena a lista em ordem decrescente. A melhor pontuação (mais inimigos eliminados) fica no topo.
    # Você pode criar uma chave de ordenação mais complexa se quiser, ex: por waves e depois por kills.
    scores.sort(key=lambda s: s['kills'], reverse=True)

    # Salva a lista atualizada
    save_scores(scores)