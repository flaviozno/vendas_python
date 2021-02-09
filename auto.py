import pandas as pd

tabela_vendas = pd.read_excel("") #path da planilha

tabela_faturamento = tabela_vendas[["ID Loja","Valor Final"]].groupby("ID Loja").sum()
tabela_faturamento = tabela_faturamento.sort_values(by="Valor Final", ascending=False)

tabela_qtd = tabela_vendas[["ID Loja","Quantidade"]].groupby("ID Loja").sum()
tabela_qtd = tabela_qtd.sort_values(by="Quantidade", ascending=False)

ticket_medio = (tabela_faturamento["Valor Final"] / tabela_qtd["Quantidade"]).to_frame()
ticket_medio = ticket_medio.rename(columns={0: "Ticket Médio"})

tabela_completa = tabela_faturamento.join(tabela_qtd).join(ticket_medio)

def enviar_email(nome_da_loja, tabela):
  import smtplib
  import email.message

  server = smtplib.SMTP('smtp.gmail.com:587')  
  corpo_email = f"""
  <p>Prezados,</p>
  <p>Segue relatório de vendas</p>
  {tabela.to_html()}
  <p>Qualquer duvida estou à disposição</p>
  """
    
  msg = email.message.Message()
  msg['Subject'] =  f"Relatório de Vendas - {nome_da_loja}"
    
  # Fazer antes (apenas na 1ª vez): Ativar Aplicativos não Seguros.
    # Gerenciar Conta Google -> Segurança -> Aplicativos não Seguros -> Habilitar
  # Caso mesmo assim dê o erro: smtplib.SMTPAuthenticationError: (534,
  # Você faz o login no seu e-mail e depois entra em: https://accounts.google.com/DisplayUnlockCaptcha
  msg['From'] = 'from@gmail.com'
  msg['To'] = 'to@gmail.com'
  password = "password"
  msg.add_header('Content-Type', 'text/html')
  msg.set_payload(corpo_email )
    
  s = smtplib.SMTP('smtp.gmail.com: 587')
  s.starttls()
  # Login Credentials for sending the mail
  s.login(msg['From'], password)
  s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
  print('Email enviado')

lista_lojas = tabela_vendas["ID Loja"].unique()
for loja in lista_lojas:
  tabela_loja = tabela_vendas.loc[tabela_vendas["ID Loja"] == loja,["ID Loja","Quantidade", "Valor Final"]]
  tabela_loja = tabela_loja.groupby("ID Loja").sum()
  tabela_loja["Ticket Medio"] = tabela_loja["Valor Final"] / tabela_loja["Quantidade"]
  enviar_email(loja,tabela_loja)
