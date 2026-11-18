import csv
import json
import os
import time
from datetime import datetime
from base_conhecimento import BaseConhecimento


class Assistente:
    """Conduz os atendimentos, bloqueia dados pessoais, registra logs e calcula indicadores."""

    def __init__(
        self,
        nome: str,
        base: BaseConhecimento,
        caminho_historico: str = "data/historico.json",
        caminho_csv: str = "data/atendimentos.csv",
    ):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico: list[dict] = self._carregar_historico()
        self.notas_facilidade: list[int] = []

    def _carregar_historico(self) -> list[dict]:
        """Carrega atendimentos anteriores se o arquivo existir e for válido."""
        if not os.path.exists(self.caminho_historico):
            return []
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _salvar_historico(self) -> None:
        """Salva a lista de atendimentos em data/historico.json."""
        os.makedirs(os.path.dirname(self.caminho_historico), exist_ok=True)
        with open(self.caminho_historico, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _contem_dado_pessoal(texto: str) -> bool:
        """Bloqueia entradas com 8 ou mais dígitos (CPF/telefone) ou '@' (e-mail)."""
        total_digitos = sum(1 for c in texto if c.isdigit())
        return total_digitos >= 8 or "@" in texto

    @staticmethod
    def _ler_sim_nao(mensagem: str) -> bool:
        """Garante resposta válida 's' ou 'n' sem encerrar o programa."""
        while True:
            resp = input(mensagem).strip().lower()
            if resp == "s":
                return True
            if resp == "n":
                return False
            print("Entrada inválida. Digite apenas 's' para sim ou 'n' para não.")

    def registrar(
        self,
        origem: str,
        pergunta: str,
        orientacao_id: int | None,
        encontrou: bool,
        ajudou: bool,
        tentativas: int,
        tempo_segundos: float,
    ) -> None:
        """Registra um atendimento no histórico em memória e persiste em JSON."""
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao_id,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(registro)
        self._salvar_historico()

    def perguntar(self) -> None:
        """Realiza o atendimento por texto livre com busca pontuada."""
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("Entrada vazia. Digite sua dúvida ou 0 para voltar.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)
            validos = [(pts, ori) for pts, ori in resultados if pts >= 3]

            if not validos:
                tempo = round(time.time() - inicio, 1)
                print("\nNão encontrei uma orientação exata para essa dúvida.")
                print("Tente usar palavras-chave mais diretas (ex.: CPF, CTPS, título, SUS, ID Jovem)")
                print(f"Ou explore as categorias disponíveis: {', '.join(self.base.categorias())}")
                self.registrar("pergunta", pergunta, None, False, False, tentativas, tempo)
                continue

            melhor_pontos, melhor_orientacao = validos[0]
            nivel = "ALTA" if melhor_pontos >= 6 else "MÉDIA"

            print(f"\nConfiança da resposta: {nivel} ({melhor_pontos} pontos)")
            melhor_orientacao.exibir()

            alternativas = validos[1:3]
            if alternativas:
                print("Outras orientações relacionadas:")
                for pts_alt, ori_alt in alternativas:
                    print(f"  - [{ori_alt.id}] {ori_alt.titulo} ({pts_alt} pontos)")
                print()

            ajudou = self._ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)

            self.registrar(
                origem="pergunta",
                pergunta=pergunta,
                orientacao_id=melhor_orientacao.id,
                encontrou=True,
                ajudou=ajudou,
                tentativas=tentativas,
                tempo_segundos=tempo,
            )
            return

    def navegar(self) -> None:
        """Permite navegar pelas categorias e orientações numeradas."""
        inicio = time.time()
        categorias = self.base.categorias()

        if not categorias:
            print("Nenhuma categoria disponível na base.")
            return

        while True:
            print("\n=== Categorias Disponíveis ===")
            for idx, cat in enumerate(categorias, start=1):
                print(f"  {idx}. {cat}")
            print("  0. Voltar")

            escolha_cat = input("Escolha uma categoria: ").strip()
            if escolha_cat == "0":
                return

            if not escolha_cat.isdigit() or not (1 <= int(escolha_cat) <= len(categorias)):
                print("Opção inválida. Digite o número de uma categoria ou 0 para voltar.")
                continue

            categoria_selecionada = categorias[int(escolha_cat) - 1]
            lista_ori = self.base.por_categoria(categoria_selecionada)

            while True:
                print(f"\n=== Orientações em [{categoria_selecionada}] ===")
                for idx, ori in enumerate(lista_ori, start=1):
                    print(f"  {idx}. {ori.titulo}")
                print("  0. Voltar")

                escolha_ori = input("Escolha uma orientação: ").strip()
                if escolha_ori == "0":
                    break

                if not escolha_ori.isdigit() or not (1 <= int(escolha_ori) <= len(lista_ori)):
                    print("Opção inválida. Escolha um número da lista ou 0 para voltar.")
                    continue

                orientacao = lista_ori[int(escolha_ori) - 1]
                orientacao.exibir()

                ajudou = self._ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    origem="categoria",
                    pergunta=f"[Categoria: {categoria_selecionada}] {orientacao.titulo}",
                    orientacao_id=orientacao.id,
                    encontrou=True,
                    ajudou=ajudou,
                    tentativas=1,
                    tempo_segundos=tempo,
                )
                return

    def registrar_nota_facilidade(self) -> None:
        """Solicita ao usuário uma nota de 1 a 5 ao encerrar o sistema."""
        while True:
            nota = input("\nAntes de sair, dê uma nota de facilidade de uso de 1 a 5: ").strip()
            if nota.isdigit() and 1 <= int(nota) <= 5:
                self.notas_facilidade.append(int(nota))
                print("Obrigado pela avaliação!")
                return
            print("Entrada inválida. Digite um número inteiro entre 1 e 5.")

    def indicadores(self) -> dict:
        """Calcula e exibe os indicadores de desempenho do assistente."""
        total = len(self.historico)
        if total == 0:
            print("\nNenhum atendimento registrado até o momento.")
            return {}

        encontrados = [h for h in self.historico if h["encontrou"]]
        ajudaram = [h for h in self.historico if h["ajudou"]]
        sem_solucao = [h["pergunta"] for h in self.historico if not h["encontrou"] or not h["ajudou"]]

        pct_encontrada = round((len(encontrados) / total) * 100, 1)
        pct_ajudou = round((len(ajudaram) / total) * 100, 1)
        tempo_medio = (
            round(sum(h["tempo_segundos"] for h in encontrados) / len(encontrados), 1)
            if encontrados
            else 0.0
        )
        media_tentativas = round(sum(h["tentativas"] for h in self.historico) / total, 2)
        media_facilidade = (
            round(sum(self.notas_facilidade) / len(self.notas_facilidade), 1)
            if self.notas_facilidade
            else "N/A"
        )

        resumo = {
            "total_atendimentos": total,
            "resposta_encontrada_pct": pct_encontrada,
            "taxa_acerto_ajudou_pct": pct_ajudou,
            "tempo_medio_segundos": tempo_medio,
            "tentativas_por_atendimento": media_tentativas,
            "facilidade_uso": media_facilidade,
            "duvidas_sem_solucao": sem_solucao,
        }

        print("\n=== Indicadores de Atendimento ===")
        print(f"Total de registros: {total}")
        print(f"Resposta encontrada: {pct_encontrada}%")
        print(f"Taxa de acerto (ajudou): {pct_ajudou}%")
        print(f"Tempo médio para encontrar: {tempo_medio}s")
        print(f"Tentativas por atendimento: {media_tentativas}")
        print(f"Facilidade de uso (1 a 5): {media_facilidade}")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f"  - {duvida}")
        else:
            print("  - Nenhuma dúvida sem solução registrada.")

        return resumo

    def exportar_csv(self) -> None:
        """Exporta o histórico de atendimentos para data/atendimentos.csv com DictWriter."""
        if not self.historico:
            print("\nNão há atendimentos registrados para exportar.")
            return

        os.makedirs(os.path.dirname(self.caminho_csv), exist_ok=True)
        campos = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos",
        ]

        with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
            writer.writeheader()
            writer.writerows(self.historico)

        print(f"\nHistórico exportado com sucesso para '{self.caminho_csv}'.")
