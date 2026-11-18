class Orientacao:
    """Representa uma orientação verificada da base de conhecimento."""

    def __init__(
        self,
        id: int,
        categoria: str,
        titulo: str,
        palavras_chave: list[str],
        resposta: str,
        documentos: list[str],
        onde: str,
        fonte: str,
        verificado_em: str,
    ):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self) -> None:
        """Exibe a orientação formatada com documentos, fonte e aviso legal."""
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(f"{self.resposta}\n")
        print("Documentos necessários:")
        for doc in self.documentos:
            print(f"  - {doc}")
        print(f"\nOnde ir/acessar: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.\n")
