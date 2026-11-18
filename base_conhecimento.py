import json
import os
from orientacao import Orientacao

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e",
    "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u",
    "ç": "c",
}


def normalizar(texto: str) -> str:
    """Remove acentos, pontuação e converte o texto para minúsculas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()[]{}'\"-/":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    """Gerencia o carregamento, filtragem e busca pontuada das orientações."""

    def __init__(self, caminho: str):
        self.caminho = caminho
        self.orientacoes: list[Orientacao] = []

    def carregar(self) -> bool:
        """Lê o arquivo JSON e instancia os objetos Orientacao sem travar em caso de erro."""
        if not os.path.exists(self.caminho):
            print(f"[Erro] Arquivo não encontrado: {self.caminho}")
            return False

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                print("[Erro] O JSON da base deve conter uma lista de orientações.")
                return False

            self.orientacoes = []
            for item in dados:
                orientacao = Orientacao(
                    id=item["id"],
                    categoria=item["categoria"],
                    titulo=item["titulo"],
                    palavras_chave=item["palavras_chave"],
                    resposta=item["resposta"],
                    documentos=item["documentos"],
                    onde=item["onde"],
                    fonte=item["fonte"],
                    verificado_em=item["verificado_em"],
                )
                self.orientacoes.append(orientacao)
            return True

        except (json.JSONDecodeError, KeyError, TypeError) as erro:
            print(f"[Erro] Falha ao ler a base de conhecimento ({erro}).")
            return False

    def categorias(self) -> list[str]:
        """Retorna a lista ordenada de categorias únicas."""
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria: str) -> list[Orientacao]:
        """Retorna todas as orientações pertencentes a uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta: str, orientacao: Orientacao) -> int:
        """Calcula a pontuação de relevância entre a pergunta e uma orientação."""
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = 0

        for kw in orientacao.palavras_chave:
            kw_norm = normalizar(kw)
            if kw_norm.strip() and kw_norm in pergunta_norm:
                pontos += 3

        palavras_pergunta = set(pergunta_norm.split())
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and f" {palavra} " in titulo_norm:
                pontos += 1

        return pontos

    def buscar(self, pergunta: str) -> list[tuple[int, Orientacao]]:
        """Retorna lista de tuplas (pontos, orientacao) ordenada da maior para a menor nota."""
        resultados = []
        for orientacao in self.orientacoes:
            pts = self.pontuar(pergunta, orientacao)
            if pts > 0:
                resultados.append((pts, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
