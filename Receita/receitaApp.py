import tkinter as tk
import requests
from googletrans import Translator

API_KEY = "0b66b23d5fa0428a943b398a53411dcc"
BASE_URL = "https://api.spoonacular.com/recipes"

def buscar_receitas_pelo_nome(nome_receita):
    url = f"{BASE_URL}/complexSearch"
    params = {
        "apiKey": API_KEY,
        "query": nome_receita,
        "number": 5
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Erro na solicitação: {response.status_code}")
        print(response.text)
        return None
    
    try:
        receitas = response.json().get('results', [])
        receitas_completas = []
        for receita in receitas:
            detalhes = obter_detalhes_receita(receita["id"])
            if detalhes:
                receitas_completas.append(detalhes)
        return receitas_completas
    except ValueError:
        print("Erro ao decodificar o JSON.")
        print(response.text)
        return None

def obter_detalhes_receita(receita_id):
    url = f"{BASE_URL}/{receita_id}/information"
    params = {
        "apiKey": API_KEY,
        "includeNutrition": False
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Erro ao obter detalhes da receita: {response.status_code}")
        print(response.text)
        return None
    
    try:
        detalhes = response.json()
        return traduzir_receita(detalhes)
    except ValueError:
        print("Erro ao decodificar o JSON.")
        print(response.text)
        return None

def traduzir_receita(detalhes):
    translator = Translator()
    detalhes["title"] = translator.translate(detalhes["title"], src='en', dest='pt').text
    detalhes["instructions"] = translator.translate(detalhes.get("instructions", ""), src='en', dest='pt').text
    detalhes["ingredients"] = [translator.translate(ingredient["name"], src='en', dest='pt').text for ingredient in detalhes["extendedIngredients"]]
    return detalhes

def buscar_receitas():
    nome_receita = entry.get()
    receitas = buscar_receitas_pelo_nome(nome_receita)
    result_text.delete(1.0, tk.END)
    
    if receitas:
        for receita in receitas:
            result_text.insert(tk.END, f"Título: {receita['title']}\n")
            result_text.insert(tk.END, "Ingredientes:\n")
            for ingrediente in receita['ingredients']:
                result_text.insert(tk.END, f" - {ingrediente}\n")
            result_text.insert(tk.END, f"Instruções: {receita['instructions']}\n")
            result_text.insert(tk.END, "\n" + "="*40 + "\n")
    else:
        result_text.insert(tk.END, "Nenhuma receita encontrada.\n")

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("App de Receitas")

tk.Label(root, text="Digite o nome da receita ou ingredientes:").pack()
entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Buscar Receitas", command=buscar_receitas).pack()

result_text = tk.Text(root, height=20, width=70)
result_text.pack()

root.mainloop()
