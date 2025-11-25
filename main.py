from typing import Optional
from simulator import Simulator
from fit_strategy import FirstFit, BestFit, WorstFit, CircularFit, FitStrategy


class Menu:
    def choose_policy(self) -> Optional[int]:
        print("1 - First-Fit")
        print("2 - Best-Fit")
        print("3 - Worst-Fit")
        print("4 - Circular-Fit")
        print("0 - Sair")

        choice = input("Escolha: ").strip()
        if not choice.isdigit():
            return None
        return int(choice)

    def build_policy(self, option: int) -> FitStrategy | None:
        if option == 1:
            return FirstFit()
        if option == 2:
            return BestFit()
        if option == 3:
            return WorstFit()
        if option == 4:
            return CircularFit()
        return None

    def run(self) -> None:
        while True:
            option = self.choose_policy()
            if option is None:
                print("Opção inválida")
                continue
            if option == 0:
                break

            policy = self.build_policy(option)
            if policy is None:
                print("Opção inválida")
                continue

            script_path = input("Nome do arquivo de requisições: ").strip()
            while not script_path:
                script_path = input("Informe o nome do arquivo de requisições valido: ").strip()
            
            mem_input = input("Tamanho da memória: ").strip()
            while not mem_input:
                mem_input = input("Informe uma memoria valida: ").strip()
                
            mem_size = int(mem_input)

            try:
                simulator = Simulator(policy)
                simulator.run(script_path, mem_size)
            except Exception as error:
                print(f"Erro: {error}")


if __name__ == "__main__":
    Menu().run()
