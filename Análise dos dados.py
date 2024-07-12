import matplotlib.pyplot as plt


def readAndTreatData():
    file = open("dados.csv", "r")
    data = []
    treatedData = []

    for line in file:
        if "\n" in line:
            newLine = line[:-1]  # 'Corta' o \n no final de cada linha
        else:
            newLine = line  # Caso seja a última linha do arquivo ele vem para cá, para evitar excluir dados importantes com o [:-1]

        data.append(newLine)  # Manda a linha em string sem o \n para a lista 'data'

    file.close()

    # Percorre a lista 'data'. Começa em 1 para evitar pegar o cabeçalho (data[0]):
    i = 1
    while i < len(data):
        # Foram cortadas as vígulas para poder converter números de string para float:
        splitData = data[i].split(",")

        # Converte os números de string para float para facilitar os cálculos posteriormente. Começa em 1 para evitar pegar a data (campo 0):
        n = 1
        while n < len(splitData):
            splitData[n] = float(splitData[n])
            n += 1

        # Manda os dados tratados para uma lista de listas de dados tratados:
        treatedData.append(splitData)
        i += 1

    return treatedData


def viewData(data):
    print(
        "\nO programa permite a visualização dos dados em modo texto dentro de um intervalo de tempo!"
    )
    print(
        "Para isso, você deve inserir um mês e ano de início e um mês e ano de término."
    )
    print(
        "Atenção: o mês deve ser um número de 1 a 12 e o ano deve ser um número de 1961 a 2016."
    )

    startMonth = int(input("\nInsira o mês de início: "))

    while startMonth < 1 or startMonth > 12:
        print("\n> Número do mês inválido! Deve ser um número de 1 a 12")
        startMonth = int(input("> Insira o mês de início: "))

    startYear = int(input("\nInsira o ano de início: "))

    while startYear < 1961 or startYear > 2016:
        print("\n> Número do ano inválido! Deve ser um número de 1961 a 2016")
        startYear = int(input("> Insira o ano de início: "))

    endMonth = int(input("\nInsira o mês de término: "))

    while endMonth < 1 or endMonth > 12:
        print("\n> Número do mês inválido! Deve ser um número de 1 a 12")
        endMonth = int(input("> Insira o mês de término: "))

    endYear = int(input("\nInsira o ano de término: "))

    while (startMonth > endMonth and endYear <= startYear) or endYear < startYear:
        print(
            "\n> Número do ano inválido! Deve ser de uma data posterior à data de início"
        )
        endYear = int(input("> Insira o ano de término: "))

    while endYear < 1961 or endYear > 2016:
        print("\n> Número do ano inválido! Deve ser um número de 1961 a 2016")
        endYear = int(input("> Insira o ano de término: "))

    print(
        "\nAgora escolha quais dados você deseja visualizar para o período informado:"
    )
    print("Digite 0 caso deseje visualizar todos os dados.")
    print("Digite 1 caso deseje visualizar apenas os dados de precipitação.")
    print("Digite 2 caso deseje visualizar apenas os dados de temperatura.")
    print("Digite 3 caso deseje visualizar apenas os dados de umidade e vento.")
    dataType = int(input("Sua escolha: "))

    while dataType < 0 or dataType > 3:
        print("\n> Número inválido! Escolha um número de 0 a 3")
        dataType = int(input("> Sua escolha: "))

    # Campos dos dados:
    fields = [
        "Data ",
        "|| Precip. (mm/m²) ",
        "|| T. Máx. (°C) || T. Mín. (°C) || Horas Insolaradas (h) || T. Média (°C) ",
        "|| Umidade (%) || Vel. Vento (m/s)",
    ]

    # Conforme o que foi selecionado pelo usuário, printa os campos que serão fornecidos:
    if dataType == 0:
        print(f"\n{fields[0]}{fields[1]}{fields[2]}{fields[3]}")
    else:
        print(f"\n{fields[0]}{fields[dataType]}")

    # Percorre a lista 'data' e seleciona cada lista:
    for list in data:
        # Pega a data e separa por '/' para possibilitar obter o mês e o ano:
        splitDate = list[0].split("/")
        month = int(splitDate[1])
        year = int(splitDate[2])

        # Caso o mês e o ano da 'list' esteja entre esse intervalo de datas (fornecidas pelo usuário), printa os itens separando-os por '||':
        if (month >= startMonth and year >= startYear) and (
            month <= endMonth and year <= endYear
        ):
            if dataType == 0:
                print(
                    f"{list[0]} || {list[1]:>5} || {list[2]:>4} || {list[3]:>4} || {list[4]:>4} || {list[5]:>5} || {list[6]:>6} || {list[7]:>10}"
                )  # Printa todos os itens
            elif dataType == 1:
                print(
                    f"{list[0]} || {list[1]:>5}"
                )  # Printa apenas a data e a precipitação
            elif dataType == 2:
                print(
                    f"{list[0]} || {list[2]:>4} || {list[3]:>4} || {list[4]:>4} || {list[5]:>5}"
                )  # Printa os dados relativos à data e à temperatura
            else:
                print(
                    f"{list[0]} || {list[6]:>6} || {list[7]:>10}"
                )  # Printa a data, a umidade e o vento

        # Caso já tenha passado a data de término, não há necessidade de continuar o loop:
        if month > endMonth and year > endYear:
            break

    # Printa os campos fornecidos novamente para facilitar a visualização em listas muito longas:
    if dataType == 0:
        print(f"{fields[0]}{fields[1]}{fields[2]}{fields[3]}")
    else:
        print(f"{fields[0]}{fields[dataType]}")


def rainiestMonth(data):
    monthlyRain = {}
    highestPreciptationDate = ""
    highestPreciptation = 0

    for list in data:
        # Pega a data e separa os últimos 7 caracteres para obter MM/AAAA somente:
        date = list[0][-7:]

        precipitation = list[1]

        # Caso não tenha a data no dicionário, cria e adiciona o valor. Caso tenha, soma o valor ao já existente nessa data:
        if date in monthlyRain.keys():
            monthlyRain[date] += precipitation
        else:
            monthlyRain[date] = precipitation

        # Se o valor da precipitação for maior que o maior valor, substitui por ele:
        if monthlyRain[date] > highestPreciptation:
            highestPreciptationDate = date
            highestPreciptation = monthlyRain[date]

    print("\n---------------------------------------------------------")
    print(
        f"\nO mês mais chuvoso dentre todos os dados disponíveis foi {highestPreciptationDate} e a precipitação foi de {highestPreciptation:.2f} mm/m²"
    )


def getLastElevenYearsData(data):
    newData = []

    for list in data:
        # Pega os últimos 4 caracteres da data (ano) e converte para int para possibilitar a comparação:
        year = int(list[0][-4:])

        if year >= 2006:
            newData.append(list)

    return newData


def plotGraphic(xAxis, yAxis, title, xLabel, yLabel):
    plt.bar(xAxis, yAxis, color="lightskyblue")

    plt.title(title)

    plt.xlabel(xLabel)
    plt.xticks(
        rotation=35, ha="right"
    )  # Rotaciona o nome de cada item do eixo x em 35° e posiciona eles na direita

    plt.ylabel(yLabel)

    plt.minorticks_on()  # Adiciona os tracinhos menores no eixo Y
    plt.tick_params(
        axis="x", which="minor", bottom=False
    )  # Remove os tracinhos menores do eixo X

    # Adiciona linhas de grade no eixo Y:
    plt.grid(axis="y", which="major", linewidth=1, alpha=0.75)
    plt.grid(axis="y", which="minor", linewidth=0.3, alpha=0.75)

    plt.show()


def averageLowestTemperature(data):
    monthList = [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]
    monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    average = {}

    print("\n---------------------------------------------------------")
    selectedMonth = int(
        input(
            "\nInsira o número do mês do qual você deseja visualizar a temperatura mínima média: "
        )
    )
    print("")

    while selectedMonth < 1 or selectedMonth > 12:
        print("\n> Número do mês inválido! Deve ser um número de 1 a 12")
        selectedMonth = int(input("> Insira o número do mês: "))

    for list in data:
        # Pega a data e separa por '/' para possibilitar obter o mês e o ano:
        splitDate = list[0].split("/")
        month = int(splitDate[1])
        year = int(splitDate[2])

        lowestTemp = list[3]

        if month == selectedMonth:
            date = f"{monthList[month - 1]}/{year}"

            # Caso seja ano bissexto e o mês selecionado seja Fevereiro, o denominador para o cálculo da média será 29.
            # Se não, será o número correspondente na lista de dias do mês:
            if (
                (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
            ) and selectedMonth == 2:
                denominator = 29
            else:
                denominator = monthDays[selectedMonth - 1]

            # Caso não tenha a data no dicionário, cria e adiciona o valor. Caso tenha, soma o valor ao já existente nessa data:
            if date in average.keys():
                average[date] += lowestTemp / denominator
            else:
                average[date] = lowestTemp / denominator

    sumTemp = 0
    for key in average:
        print(
            f"{key} = {average[key]:.2f}°C"
        )  # Printa os dados na tela no formato mês/AAAA = Temp.

        sumTemp += average[key]  # Soma a temperatura daquela chave em uma variável

    print(
        f"\nMédia geral das temperaturas mínimas médias do mês de {monthList[selectedMonth - 1]} de 2006 a 2016: {(sumTemp/len(average)):.2f}°C"
    )  # Calcula a média e exibe na tela

    # Chama uma função de traçar o gráfico:
    plotGraphic(
        average.keys(),
        average.values(),
        f"Média das temperaturas mínimas no mês de {monthList[selectedMonth - 1]} - de 2006 a 2016",
        "Meses",
        "Temperaturas (°C)",
    )


data = readAndTreatData()  # Pega os dados já tratados
viewData(data)  # Visualização de intervalo de dados em modo texto
rainiestMonth(data)  # Mês mais chuvoso

newData = getLastElevenYearsData(data)  # Pega os dados dos últimos 11 anos
averageLowestTemperature(
    newData
)  # Média da temperatura mínima de um determinado mês (auge do inverno) nos últimos 11 anos (2006 a 2016) + Gráfico de barras + Média geral
