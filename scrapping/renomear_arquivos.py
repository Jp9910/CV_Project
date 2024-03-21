import os
from pathlib import Path

def renomear(dir: Path):
    if not os.path.exists(dir):
        print("Diretório não encontrado:")
        print(dir)
        exit()

    qtdArq = len(os.listdir(dir))
    existentes = []
    for entry in dir.iterdir():
        n = int(entry.stem)
        existentes.append(n)

    existentes.sort(reverse = True)
    maior = existentes[0]

    i=0
    faltando = []
    for i in range(1,maior):
        if (not os.path.isfile(f"{dir}\\{i}.png") and not os.path.isfile(f"{dir}\\{i}.jpg")):
            faltando.append(i)

    print("Maior:", maior)
    print("Existentes:", existentes)
    print("Faltando:", faltando)
    print("Total:", qtdArq)
    print("Faltando:", len(faltando))

    rename = True
    if (rename):
        i=0
        while(maior != qtdArq and i<qtdArq):
            renamed = f"{dir}\\{existentes[i]}"
            if (os.path.isfile(f"{renamed}.png")):
                renamed += ".png"
            if (os.path.isfile(f"{renamed}.jpg")):
                renamed += ".jpg"
            dst = f"{dir}\\{faltando[i]}.png"
            os.rename(renamed, dst)
            if (existentes[i] == maior and i < len(existentes)-1):
                maior = existentes[i+1]

            print(f"{existentes[i]} -> {faltando[i]}")
            # print(f"Renomeado {renamed} para {dst}")
            i+=1
        print("Maior final:", maior)

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    dir = Path(f'{path}\\images\\fizz')
    renomear(dir)


## iterdir()
# print(entry.stem) # nome sem extensão
# print(entry) # caminho completo
# print(entry.suffix) # extensão
# print(entry.name) # nome com extensão
# print(entry.resolve()) # nome do arquivo com symlinks e atalhos resolvidos
# print(entry.parent) # diretório pai

## Rename
# my_file = Path("E:\\seaborn_plot\\x.dwt")
# my_file.rename(my_file.with_suffix('.txt'))