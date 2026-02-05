from docling.document_converter import DocumentConverter
from langchain_groq import ChatGroq
from IPython.display import Markdown
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
import json
import pandas as pd
import os
import streamlit as st

path_json = "./curriculos/curriculos.json"

#Converte os PDFs de Currículos em PDFs
def convertePdfMarkdown(path):
    #Lembrar: isso também converte arquivos de links
    converter = DocumentConverter()
    result = converter.convert(path)
    content = result.document.export_to_markdown()
    return content



#Formata a resposta da LLM
def format_res(res, return_thinking=False):
    res = res.strip()

    if return_thinking:
        res = res.replace("<think>", "[pensando...] ")
        res = res.replace("</think>", "\n---\n")
    else:
      if "</think>" in res:
        res = res.split("</think>")[-1].strip()

    return res



def parse_res_llm(response_text: str, required_fields: list) -> dict:
  try:
    if "</think>" in response_text:
      response_text = response_text.split("</think>")[-1].strip()

    start_idx = response_text.find("{")
    end_idx = response_text.find("}") + 1
    if start_idx == -1 or end_idx == 0:
      raise json.JSONDecodeError("Nenhum JSON encontrado na resposta", response_text, 0)

    json_str = response_text[start_idx:end_idx]
    info_cv = json.loads(json_str)

    for field in required_fields:
      if field not in info_cv:
        info_cv[field] = []

    return info_cv

  except json.JSONDecodeError:
    return
  
def parse_doc(file_path):
  converter = DocumentConverter()
  result = converter.convert(file_path)
  content = result.document.export_to_markdown()
  return content


def process_cv(schema, job_details, prompt_template, prompt_score, llm, file_path):

  if file_path:
    if not os.path.exists(file_path):
      raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

  content = parse_doc(file_path)

  chain = prompt_template | llm
  output = chain.invoke({"schema": schema, "cv": content, "job": job_details, "prompt_score": prompt_score})

  res = format_res(output.content)

  return output, res




def save_json_cv(new_data, path_json, key_name="nome"):
    # Carrega o JSON existente, se houver
    if os.path.exists(path_json):
        with open(path_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    if isinstance(data, dict):
        data = [data]

    # Verifica se já existe um currículo com o mesmo nome
    candidates = [entry.get(key_name) for entry in data]
    if new_data.get(key_name) in candidates:
      st.warning(f"Currículo '{new_data.get(key_name)}' já registrado. Ignorando.")
      return

    # Adiciona e salva
    data.append(new_data)
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



def load_json_cv(path_json):
  with open(path_json, "r", encoding="utf-8") as f:
    return json.load(f)


def show_cv_result(result: dict):
    md = f"### 📄 Análise e Resumo do Currículo\n"
    if "nome" in result:
        md += f"- **Nome:** {result['nome']}\n"
    if "area" in result:
        md += f"- **Área de Atuação:** {result['area']}\n"
    if "formacao" in result:
        md += f"- **Área de Atuação:** {result['formacao']}\n"
    if "habilidades" in result:
        md += f"- **Competências:** {', '.join(result['habilidades'])}\n"
    if "resumo" in result:
        md += f"- **Resumo do Perfil:** {result['resumo']}\n"
    if "recomendacao_perguntas" in result:
        md += f"- **Perguntas sugeridas:**\n"
        md += "\n".join([f"  - {q}" for q in result["recomendacao_perguntas"]]) + "\n"
    if "strengths" in result:
        md += f"- **Pontos fortes (ou Alinhamentos):**\n"
        md += "\n".join([f"  - {s}" for s in result["strengths"]]) + "\n"
    if "areas_para_melhorar" in result:
        md += f"- **Pontos a desenvolver (ou Desalinhamentos):**\n"
        md += "\n".join([f"  - {a}" for a in result["areas_para_melhorar"]]) + "\n"
    if "considerecoes_importantes" in result:
        md += f"- **Pontos de atenção:**\n"
        md += "\n".join([f"  - {i}" for i in result["considerecoes_importantes"]]) + "\n"
    if "recomendacoes_finais" in result:
        md += f"- **Conclusão e recomendações:** {result['recomendacoes_finais']}\n"
    if "score" in result:
        md += f"- **Conclusão e recomendações:** {result['score']}\n"
    return md


def display_json_table(path_json):
  with open(path_json, "r", encoding="utf-8") as f:
    data = json.load(f)

  df = pd.DataFrame(data)
  return df

#convertePdfMarkdown("./curriculos/curriculo1.pdf")

def load_llm(id_model, temperature):
  llm = ChatGroq(
      model=id_model,
      temperature=temperature,
      max_tokens=None,
      timeout=None,
      max_retries=2,
  )
  return llm



""" chain = prompt_template | llm
output = chain.invoke({"schema": schema, "cv": content})

output, res = process_cv(schema, content, job_details, prompt_template, llm)

structured_data = parse_res_llm(res, fields)

save_json_cv(structured_data, path_json)

result_cv = load_json_cv(path_json)

show_cv_result(result_cv)

df = display_json_table(path_json)
display(df) """