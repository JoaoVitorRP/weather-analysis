import matplotlib.pyplot as plt
import seaborn as sns


def readAndTreatData():
    file = open("dados.csv", "r")
    data = (
        []
    )  # ["cabeçalho", "data, precip, max, min, horas sol, temp media, umidade, vento", "..."]
    treatedData = []  # [["Ano", float(precip), float(max), ...], [...]] até 2015

    for line in file:
        if "\n" in line:
            newLine = line[:-1]
        else:
            newLine = line

        data.append(newLine)

    file.close()

    i = 1
    while i < len(data):
        splitData = data[i].split(",")

        if "2016" in splitData[0]:
            break

        if "2001" in splitData[0]:
            i += 1
            continue

        n = 0
        while n < len(splitData):
            currentData = splitData[n]

            if n == 0:
                splitData[n] = currentData[-4:]
            else:
                splitData[n] = float(currentData)

            n += 1

        treatedData.append(splitData)
        i += 1

    return treatedData


def plotGraphic(xAxis, yAxis, title, yLabel):
    years = [int(x) for x in list(xAxis)]

    sns.regplot(
        x=years, y=list(yAxis), ci=False, line_kws={"color": "red", "alpha": 0.7}
    )  # Linha de tendência
    plt.plot(years, list(yAxis), marker="o", color="dodgerblue")  # Gráfico

    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel("Ano")

    plt.minorticks_on()

    plt.grid(axis="y", which="major", linewidth=1, alpha=0.75)
    plt.grid(axis="y", which="minor", linewidth=0.3, alpha=0.75)

    plt.grid(axis="x", which="major", linewidth=1, alpha=0.75)
    plt.grid(axis="x", which="minor", linewidth=0.3, alpha=0.75)

    plt.show()


def preciptationGraphic(data):
    preciptationMonthly = {}

    for list in data:
        preciptation = list[1]
        date = list[0]

        if date in preciptationMonthly.keys():
            preciptationMonthly[date] += preciptation
        else:
            preciptationMonthly[date] = preciptation

    plotGraphic(
        preciptationMonthly.keys(),
        preciptationMonthly.values(),
        "Precipitação total por ano - de 1961 a 2015",
        "Precipitação (mm/m²)",
    )


def avgGetter(data, typeIndex):
    dataTypes = [
        "Data",
        "Preciptação",
        "Temperatura máxima",
        "Temperatura mínima",
        "Horas ensolaradas",
        "Temperatura média",
        "Umidade relativa",
        "Velocidade do vento",
    ]
    dataType = dataTypes[typeIndex]

    units = {
        "Data": "Ano",
        "Preciptação": "mm/m²",
        "Temperatura máxima": "°C",
        "Temperatura mínima": "°C",
        "Horas ensolaradas": "h",
        "Temperatura média": "°C",
        "Umidade relativa": "%",
        "Velocidade do vento": "m/s",
    }
    unit = units[dataType]

    sum = {}
    daysCount = {}
    avg = {}

    for list in data:
        year = list[0]

        if year in sum.keys():
            sum[year] += list[typeIndex]
            daysCount[year] += 1
        else:
            sum[year] = list[typeIndex]
            daysCount[year] = 1

        avg[year] = sum[year] / daysCount[year]

    plotGraphic(
        avg.keys(),
        avg.values(),
        f"{dataType} média por ano - de 1961 a 2015",
        f"{dataType} ({unit})",
    )


data = readAndTreatData()
# preciptationGraphic(data)

print("Dados disponíveis para a visualização da média: ")
print(
    "> 1 = Preciptação\n> 2 = Temperatura máxima\n> 3 = Temperatura mínima\n> 4 = Horas ensolaradas\n> 5 = Temperatura média\n> 6 = Umidade relativa\n> 7 = Velocidade do vento"
)
selectedNum = int(input("Escolha um número de 1 a 7: "))

while selectedNum < 1 or selectedNum > 7:
    print(
        f"\n> Tipo inválido: {selectedNum}, deve ser um inteiro entre 1 e 7, incluso!"
    )
    selectedNum = int(input("Escolha um número de 1 a 7: "))

avgGetter(data, selectedNum)
