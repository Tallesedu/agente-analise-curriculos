import csv
import os
import pandas as pd

def criaVaga(data, filename):
    headers = ['title', 'description', 'details']
    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = headers, delimiter=';')
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


#Ler arquivo:
    #df = pd.read_csv(path_job_csv, sep = ";")
def load_vaga(path_job_csv):
    try:
        df = pd.read_csv(path_job_csv, sep = ";", encoding='utf-8')
        job = df.iloc[-1]

        #Cria template para envio da vaga:
        prompt_text = f"""
            **Vaga para {job['title']}**

            **Descrição da Vaga:**
            {job['description']}

            **Detalhes Completos:**
            {job['details']}
            """

        return prompt_text.strip()

    except FileNotFoundError:
        return "Erro: Arquivo de vagas não encontrado"


#vaga = {}
#vaga['title'] = "Desenvolvedor(a) Full Stack"
#vaga['description'] = "Estamos em busca de um(a) Desenvolvedor(a) Full Stack para integrar o time de tecnologia da nossa empresa, atuando em projetos estratégicos com foco em soluções escaláveis e orientadas a dados. O(a) profissional será responsável por desenvolver, manter e evoluir aplicações web robustas, além de colaborar com times multidisciplinares para entregar valor contínuo ao negócio."
#vaga['details'] = """
#    Atividades:
#    - Desenvolver e manter aplicações web em ambientes modernos, utilizando tecnologias back-end e front-end.
#   - Trabalhar com equipes de produto, UX e dados para entender demandas e propor soluções.
#   - Criar APIs, integrações e dashboards interativos.
#   - Garantir boas práticas de versionamento, testes e documentação.
#   - Participar de revisões de código, deploys e melhorias contínuas na arquitetura das aplicações.
#
#    Pré-requisitos:
#    - Sólidos conhecimentos em Python, JavaScript e SQL.
#   - Experiência prática com frameworks como React, Node.js e Django.
#    - Familiaridade com versionamento de código usando Git.
#    - Experiência com serviços de nuvem, como AWS e Google Cloud Platform.
#   - Capacidade de trabalhar em equipe, com boa comunicação e perfil colaborativo.
#
#   Diferenciais:
#   - Conhecimento em Power BI ou outras ferramentas de visualização de dados.
#   - Experiência anterior em ambientes ágeis (Scrum, Kanban).
#   - Projetos próprios, contribuições open source ou portfólio técnico disponível.
#   - Certificações em nuvem ou áreas relacionadas à engenharia de software.
#   """

#Rodar somente para criar vagas
#criaVaga(vaga, path_job_csv)


