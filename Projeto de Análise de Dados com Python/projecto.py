
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas import Series, DataFrame
from datetime import datetime, date, time

"""
Notas sobre alguns usos.
Quando uso o groupby usei a notação com ponto(.),
exemplo Dados_combinados.groupby('gender').total_price
Podeiria usar e é mais aconselhado a usar
Dados_combinados.groupby('gender')['total_price'] isto porque é um
acesso à coluna usando um operador de indexação e é mais seguro e
funciona em todos os casos, especialmente quando:

-O nome da coluna contém espaços ou caracteres especiais

-O nome da coluna é igual a um método do DataFrame (como 'mean', 'count', etc.)

-Quando se programa de forma genérica (o nome da coluna está numa variável)
Já com ponto temos um aceeso à coluna como se fosse uma propiedade e é
mais limpo visualmente, mas com limitações:

-Só funciona se o nome da coluna for um identificador válido em Python
(sem espaços, sem caracteres especiais)

-Não funciona se o nome da coluna tiver conflito com
métodos existentes do Pandas (ex:falharia se houvesse
uma coluna chamada 'mean'
Dados_combinados.groupby('gender').mean)


"""


data_Sales = pd.read_csv('sales_data.csv')
#print(data_Sales)
data_Customers = pd.read_csv('customers.csv')
#print(data_Customers)

#Cria um DataFrame para o dados de Sales
dt_sales = pd.DataFrame(data_Sales)
#print(dt_sales,'\n') #verificar  dataframe
#print(dt_sales.head(),'\n') #mostra as primeiras 5 linhas de dados
#print(dt_sales.info(),'\n')
#print(dt_sales.describe(),'\n')
#print(dt_sales['order_date'],'\n')
#Adiciona uma coluna month extraindo o mês da coluna order_date
dt_sales['month'] = pd.to_datetime(dt_sales['order_date']).dt.month
print(dt_sales['month'],'\n')
print(dt_sales.head(), '\n')


#Cria um DataFrame para os dados de customers

dt_customers = pd.DataFrame(data_Customers)
#print(dt_customers, '\n') #verificar  dataframe
print(dt_customers.head(),'\n') #mostra as primeiras 5 linhas de dados
#print(dt_customers.info(),'\n')
#print(dt_customers.describe(),'\n')


#Estatística básica


"""
para os clintes únicos podia usar qualquer um dos DataFrames,
teria só de usar a coluna customer_id e a ordem de mostragem
seria apenas diferente mas usando short() resolvia. Não vale muito a pena
"""

#print(pd.unique(dt_sales['customer_id']))
print(pd.unique(dt_customers['customer_id']), '\n')
#numero toral de pedidos/encomendas
print("O número total de pedidos foi " ,dt_sales['order_id'].count(), '\n')
#produtos pedidos
print(pd.unique(dt_sales['product_id']), '\n')

print("Média do total de preços " ,dt_sales['total_price'].mean(), '\n')
print("Mediana do total de preços " ,dt_sales['total_price'].median(), '\n')
print("Desvio Padrão do total de preços " ,dt_sales['total_price'].std(), '\n')





#Agregações

"""
Aqui agrupei os produtos por order_id e assim obtive quantas vezes
cada produto foi encomendado
"""
grupo_product_por_order = dt_sales.groupby('product_id').order_id.count()

dict_product_por_order = {f'{k}': v for k, v in grupo_product_por_order.to_dict().items()}

#print(grupo_product_por_order, '\n')
print("O produto mais encomendado foi:")
print(max(dict_product_por_order.items(), key=lambda t: t[1]), '\n')


"""
Aqui agrupei os produtos por quantidade e assim obtive o produto
mais vendido por quantidade
"""

grupo_product_quantity = dt_sales.groupby('product_id').quantity.sum()

dict_product_quantity = {f'{k}': v for k, v in grupo_product_quantity.to_dict().items()}

#print(grupo_product_quantity, '\n')
print("O produto mais vendido por quantidade foi:")
print(max(dict_product_quantity.items(), key=lambda t: t[1]), '\n')


"""
Total de vendas por mês
"""
print("Total de vendas por mês:")
print(dt_sales.value_counts("month"), '\n')
    
"""
Top 5 clientes que mais gastaram
"""
grupo_customer_total_price = dt_sales.groupby('customer_id').total_price.sum()
#dict_customer_total_price = {f'{k}': v for k, v in grupo_customer_total_price.to_dict().items()}
# nlargest uma função pandas dá-me os 5,neste caso, valores mais altos
print("Top 5 clientes que mais gastaram: \n")
print(grupo_customer_total_price.nlargest(5), '\n')

#Visualização

# Extrair o ano e mês do DataFrame
lista_ano = pd.to_datetime(dt_sales['order_date']).dt.year.tolist()
lista_mes = pd.to_datetime(dt_sales['order_date']).dt.month.tolist()

# Criar a lista de datas no formato m-yyyy
lista_datas = [f"{lista_mes[i]}-{lista_ano[i]}" for i in range(len(lista_ano))]

# Criar a série com as contagem
serie_data_por_order = pd.Series(lista_datas).value_counts()

# Converter os índices para datetime para depois ordenar cronologicamente
serie_data_por_order.index = pd.to_datetime(serie_data_por_order.index, format='%m-%Y')
serie_data_por_order = serie_data_por_order.sort_index()

# Converte os índices de volta para o formato m-yyyy
serie_data_por_order.index = serie_data_por_order.index.strftime('%m-%Y')

#print(serie_data_por_order)

# Criar o gráfico de linhas
plt.figure(figsize=(12, 6))
serie_data_por_order.plot(kind='line', marker='o', linestyle='-', color='steelblue')
# Coloca os valores das datas no eixo do x para se perceber melhor
#plt.xticks(rotation=45, ha='right')-(tinha usado assim ficar melhor como está)
plt.xticks(ticks=range(len(serie_data_por_order)), labels=serie_data_por_order.index, rotation=45, ha='right')

# Ajustes de layout e estética
plt.title('Número de Pedidos por Mês', fontsize=16)
plt.xlabel('Mês-Ano', fontsize=12)
plt.ylabel('Número de Pedidos', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()


plt.show()

#Gráfico de barras: Top 10 produtos por receita

grupo_product_total_price = dt_sales.groupby('product_id').total_price.sum()
# Ordenar para exibir os 10 produtos mais vendidos
top_products = grupo_product_total_price.nlargest(10)

# style
plt.style.use('classic')

#  Criar figura e eixo com fundo cinza
fig, ax = plt.subplots(figsize=(16,8))
ax.set_facecolor('#E6E6E6')

# Gride e aparência
ax.set_axisbelow(True)
ax.grid(color='w', linestyle='solid')

for spine in ax.spines.values():
    spine.set_visible(False)

ax.xaxis.tick_bottom()
ax.yaxis.tick_left()
ax.tick_params(colors='gray', direction='out', labelsize=12)

for tick in ax.get_xticklabels():
    tick.set_color('gray')
for tick in ax.get_yticklabels():
    tick.set_color('gray')

# Plot do histograma
ax.bar(top_products.index.astype(str), top_products.values,
        edgecolor='#E6E6E6',color='#EE6666', width=0.4)

# Títulos e rótulos
ax.set_title('Top 10 Produtos por Total de Vendas', color='gray',fontsize=18)
ax.set_xlabel('ID do Produto', color='gray',fontsize=16)
ax.set_ylabel('Total de Vendas', color='gray',fontsize=16)
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

#Histograma: Distribuição de idades dos clientes

grupo_idade_customer = dt_customers.groupby('age').customer_id

idades = dt_customers['age']
# Toma o menor e o maior valor da idade
idade_min = idades.min()
idade_max = idades.max()

# Cria os bins de 4 em 4 anos, garantindo que o máximo seja coberto
bins = np.arange(idade_min, idade_max + 5, 5)

# Estilo clássico
plt.style.use('classic')

# Criar figura e eixo
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor('#E6E6E6')

# Grid e estilo visual
ax.set_axisbelow(True)
ax.grid(color='w', linestyle='solid')
for spine in ax.spines.values():
    spine.set_visible(False)
ax.xaxis.tick_bottom()
ax.yaxis.tick_left()
ax.tick_params(colors='gray', direction='out')
for tick in ax.get_xticklabels():
    tick.set_color('gray')
for tick in ax.get_yticklabels():
    tick.set_color('gray')

# Plot do histograma
counts, bins_edges, patches = ax.hist(idades, bins=bins,
                            edgecolor='#E6E6E6', color='#EE6666',rwidth=0.8)

#Ajustar o limite do eixo X para eliminar espaços antes da primeira barra
ax.set_xlim(bins[0], bins[-1])
# Criar labels tipo "20-24", "24-28" ...
labels = [f'{int(bins[i])}-{int(bins[i+1]-1)}' for i in range(len(bins)-1)]

# Para posicionar o tick no centro do bin, calcular os centros
bin_centers = 0.5 * (bins[:-1] + bins[1:])

# Ajustar ticks e labels no eixo X
ax.set_xticks(bin_centers)
ax.set_xticklabels(labels, rotation=45, fontsize=10, color='gray')

# Títulos e rótulos
ax.set_title('Distribuição de Idades dos Clientes',color='gray',fontsize=16)
ax.set_xlabel('Idade', color='gray',fontsize=14)
ax.set_ylabel('Número de Clientes', color='gray',fontsize=14)

plt.tight_layout()
plt.show()

#Merge e Análise Avançada

Dados_combinados = pd.merge(dt_sales, dt_customers, on='customer_id')



grupo_gender_total_price = Dados_combinados.groupby('gender').total_price.mean()

# Encontrar o gênero com maior média de gastos
genero_maior_gasto = grupo_gender_total_price.idxmax() ##retorna o índice
valor_maior_gasto = grupo_gender_total_price.max()


print("Média de gastos por gênero:")
print(grupo_gender_total_price)
print(f"\nO gênero que mais gastou em média foi: {genero_maior_gasto} com {valor_maior_gasto:.2f}€ \n")

#cidades que têm os clientes mais valiosos
grupo_city_total_price = Dados_combinados.groupby('city').total_price.sum()

# Cidades com maior valor médio de compras
cidades_mais_valiosas_media = Dados_combinados.groupby('city').total_price.mean().sort_values(ascending=False)
print("Média de gastos por cidade:")
print(cidades_mais_valiosas_media.head(10), '\n')

# Cidades que mais geram receita no total
cidades_mais_valiosas_total = Dados_combinados.groupby('city').total_price.sum().sort_values(ascending=False)
print("Total de gastos por cidade:")
print(cidades_mais_valiosas_total.head(10),'\n')

# Selecionar a cidade com maior valor médio
top_cidade_media = cidades_mais_valiosas_media.idxmax()

# Selecionar a cidade com maior volume total
top_cidade_total = cidades_mais_valiosas_total.idxmax()

print(f"Cidade com clientes que mais gastam em média: {top_cidade_media}")
print(f"Cidade que mais contribui para a facturação total: {top_cidade_total}\n")

#cidades_mais_valiosas_media.head(10).plot(kind='bar', title='Média de gastos por cidade')
#plt.ylabel('Valor médio')
#plt.show()

#Padrões sazonais

Dados_combinados['year'] =  pd.to_datetime(Dados_combinados['order_date']).dt.year
# Agrupar por mês e calcular o total de vendas
vendas_por_mes = Dados_combinados.groupby(['year', 'month']).total_price.sum().reset_index()

# Visualização
plt.figure(figsize=(12, 6))
for year in vendas_por_mes['year'].unique():
    dados_ano = vendas_por_mes[vendas_por_mes['year'] == year]
    plt.plot(dados_ano['month'], dados_ano['total_price'], label=year, marker='o')

plt.title('Vendas Mensais por Ano')
plt.xlabel('Mês')
plt.ylabel('Total de Vendas (€)')
plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
plt.legend()
plt.grid(True)
plt.show()

# Calcular médias mensais independente do ano
media_mensal = Dados_combinados.groupby('month').total_price.mean().reset_index()

plt.figure(figsize=(12, 6))
plt.bar(media_mensal['month'], media_mensal['total_price'])
plt.title('Média de Vendas por Mês (Todos os Anos)')
plt.xlabel('Mês')
plt.ylabel('Média de Vendas (€)')
plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
plt.grid(True)
plt.show()

# Calcular variação percentual mensal em relação à média anual
media_anual = Dados_combinados.groupby('year').total_price.mean()
vendas_por_mes['var_percentual'] = vendas_por_mes.apply(
    lambda row: (row['total_price'] / media_anual[row['year']] - 1) * 100, axis=1)

# Média da variação percentual por mês
var_percentual_media = vendas_por_mes.groupby('month').var_percentual.mean()

plt.figure(figsize=(12, 6))
plt.bar(var_percentual_media.index, var_percentual_media.values)
plt.title('Variação Percentual Média das Vendas por Mês em Relação à Média Anual')
plt.xlabel('Mês')
plt.ylabel('Variação Percentual (%)')
plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
plt.axhline(0, color='red', linestyle='--')
plt.grid(True)
plt.show()

# Filtrar apenas dados de dezembro
dezembro_data = Dados_combinados[Dados_combinados['month'] == 12]

# Vendas totais por ano em dezembro
dezembro_por_ano = dezembro_data.groupby('year').total_price.sum()

# Comparação com a média mensal do ano
media_mensal_ano = Dados_combinados.groupby('year').total_price.mean()
comparacao_dezembro = (dezembro_por_ano / media_mensal_ano) * 100

print("Comparação das vendas de dezembro com a média mensal do ano:")
print(comparacao_dezembro)
