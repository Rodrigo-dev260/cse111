import math

def main():
    """Calcula e imprime o volume de um cone circular reto."""
    # Exemplo de cálculo com valores fixos
    ex_radius = 2.8
    ex_height = 3.2
    ex_vol = cone_volume(ex_radius, ex_height)
    
    print("Este programa calcula o volume de um cone circular reto.")
    print(f"Por exemplo, se o raio do cone for {ex_radius} e a altura for {ex_height},")
    print(f"então o volume será {ex_vol:.1f}")
    print()
    
    # Solicita ao usuário os valores do cone
    radius = float(input("Digite o raio do cone: "))
    height = float(input("Digite a altura do cone: "))
    
    # Corrigindo a chamada da função
    vol = cone_volume(radius, height)
    
    # Exibe os resultados
    print(f"Raio: {radius}")
    print(f"Altura: {height}")
    print(f"Volume: {vol:.1f}")

def cone_volume(radius, height):
    """Calcula e retorna o volume de um cone circular reto."""
    volume = math.pi * radius**2 * height / 3
    return volume

# Chamar a função principal
main()
