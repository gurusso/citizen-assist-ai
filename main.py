from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main() -> None:
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar o assistente devido a erro na base de conhecimento.")
        return

    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print("\n==========================================")
        print(f"  {assistente.nome} - Orientação Cidadã")
        print("==========================================")
        print("1. Fazer uma pergunta em texto livre")
        print("2. Navegar por categorias")
        print("3. Ver indicadores de atendimento")
        print("4. Exportar atendimentos para CSV")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.registrar_nota_facilidade()
            assistente.indicadores()
            assistente.exportar_csv()
            print("\nEncerrando o Citizen Assist AI. Até logo!")
            break
        else:
            print("Opção inválida. Escolha entre 0 e 4.")


if __name__ == "__main__":
    main()
