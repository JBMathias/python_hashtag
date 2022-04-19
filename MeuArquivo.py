import pandas as  pd
import win32com.client as win32

#importar base de dados
tabela_vendas = pd.read_excel("Vendas.xlsx")

#Visuzalizar a base de dados
pd.set_option('display.max_columns', None)

#Filtrando Colunas
'''tabela_vendas[['ID Loja','Valor Final']]'''

#Faturamento por loja
faturamento = tabela_vendas[['ID Loja','Valor Final']].groupby('ID Loja').sum()

#Quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
# print(quantidade)

#Ticket médio por produto em cada loja
ticket_medio = ((faturamento['Valor Final'] / quantidade['Quantidade'])).to_frame()
ticket_medio = ticket_medio.rename(columns={0:'Ticket Medio'})
# print(ticket_medio)

#Enviar email com o relatório
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'juniormathias.email@gmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de vendas por cada loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html(formatters={'Quantidade': 'R${:,.2f}'.format})}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Medio': 'R${:,.2f}'.format})}


<p>Qualquer dúvida estou a disposição.</p>

<p>Att...</p>
<p>Matias</p>
'''

mail.Send()
print("Email Enviado!")