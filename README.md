# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

Assistente de terminal desenvolvido em Python para a **Global Solution 2026.2 (Pensamento Computacional e Automação com Python)**, focado em orientar **jovens em busca do primeiro emprego** com informações verificadas de canais oficiais, sem coletar dados pessoais.

---

## Integrantes

- **Gustavo Russo** — RM `569283`
- **Guilherme Muniz** — RM `569521`

---

## Público e Problema Escolhidos

- **Público-alvo:** Jovens de 14 a 29 anos em transição para o primeiro emprego e vida adulta.
- **Problema:** Informações sobre emissão de documentos básicos (CPF, CIN, Título de Eleitor, CTPS Digital, Cartão SUS) e programas sociais/trabalhistas (Jovem Aprendiz, ID Jovem, Alistamento Militar) estão espalhadas em páginas técnicas ou misturadas a sites não oficiais que cobram taxas indevidas por serviços gratuitos.
- **ODS Relacionados:**
  - **ODS 8 (Trabalho Decente e Crescimento Econômico):** Facilita o acesso à Carteira de Trabalho Digital e ao programa Jovem Aprendiz.
  - **ODS 10 (Redução das Desigualdades) e ODS 16 (Paz, Justiça e Instituições Eficazes):** Democratiza o acesso claro e gratuito à documentação civil e direitos do cidadão.

---

## Como Executar

1. Certifique-se de ter o **Python 3.10+** instalado.
2. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone https://github.com/SEU-USUARIO/citizen-assist-ai.git
   cd citizen-assist-ai
   ```
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```
*(Nenhuma biblioteca externa é necessária; o projeto utiliza apenas módulos nativos do Python).*

---

## Regra de Pontuação e Busca

A busca aplica normalização textual (minúsculas, remoção de acentos e pontuação) e atribui pontos a cada orientação da base:

| Critério | Pontuação |
| :--- | :---: |
| Palavra-chave da orientação encontrada na pergunta | **+3 pontos** |
| Palavra da pergunta (4+ letras) presente no título | **+1 ponto** |

**Níveis de Confiança:**
- **6 pontos ou mais:** Confiança `ALTA`
- **3 a 5 pontos:** Confiança `MÉDIA`
- **Menor que 3 pontos:** Orientação não encontrada (o sistema sugere termos e categorias).

---

## Fontes Oficiais Consultadas

- Portal Gov.br / Receita Federal: `https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf`
- Governo Digital (CIN): `https://www.gov.br/governodigital/pt-br/identidade`
- Tribunal Superior Eleitoral (TSE): `https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral`
- Ministério da Saúde (Cartão SUS): `https://www.gov.br/saude`
- Ministério do Trabalho e Emprego (CTPS e Jovem Aprendiz): `https://www.gov.br/trabalho-e-emprego`
- Ministério do Desenvolvimento Social (ID Jovem): `https://www.gov.br/mds`
- Exército Brasileiro (Alistamento Militar): `https://alistamento.eb.mil.br/`
- Secretaria Nacional do Consumidor: `https://www.consumidor.gov.br/`

---

## Resultado do Teste com Usuários

Foram realizados **10 atendimentos** com **3 usuários externos** (sem coleta de nomes ou dados pessoais):

| Indicador | Resultado |
| :--- | :---: |
| Resposta encontrada (%) | **90,0%** |
| Taxa de acerto — ajudou (%) | **90,0%** |
| Tempo médio para encontrar | **5,2 s** |
| Tentativas por atendimento | **1,1** |
| Facilidade de uso (1 a 5) | **4,7** |

- **Dúvida sem solução registrada:** *"Preciso de ajuda com passaporte"* (fora do escopo atual da base).
- **Melhoria aplicada após os testes:** Inclusão das palavras-chave `"segunda via"` e `"primeira via"` no registro da Carteira de Identidade Nacional (ID 2), aumentando a taxa de acerto para perguntas sobre emissão de documento.

---

## Limitações do Assistente

- **Dependência lexical:** Por operar com regras determinísticas e palavras-chave, erros graves de digitação ou sinônimos não cadastrados no JSON podem não pontuar.
- **Base estática:** As orientações dependem de atualização manual no arquivo `data/base_conhecimento.json`.
- **Caráter informativo:** O sistema não substitui canais oficiais do governo e não realiza agendamentos ou emissões diretamente.

---

## Vídeo Técnico

- **Link no YouTube (Não Listado):** `https://youtu.be/COLE-AQUI-O-LINK-DO-VIDEO`
