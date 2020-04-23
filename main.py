
from classNewton import Newton

_3Barras = Newton()  # Esta linha instancia a classe "Newton", criada em outro arquivo.
_3BarrasPV = Newton()


"""
Instanciação das barras através do método "setBarras". Seguem a seguinte ordem: 

Barra, Código da barra, Tensão na barra [pu], Ângulo da tensão [graus], Carga [P + Qj] (VA), Geração [P + Qj] (VA)

Mais informações sobre este e outros métodos podem ser obtidos no arquivo "classNewton". 

"""
# _3Barras.setBarras(1, 1, 1.05, 0, 0 + 0 * 1j, 0 + 0 * 1j)
# _3Barras.setBarras(2, 2, 1.00, 0, 256.6e6 + 110.2e6 * 1j, 0 + 0 * 1j)
# _3Barras.setBarras(3, 2, 1.00, 0, 138.6e6 + 45.2e6 * 1j, 0 + 0 * 1j)

# _3BarrasPV.setBarras(1, 1, 1.05, 0, 0 + 0 * 1j, 0 + 0 * 1j)
# _3BarrasPV.setBarras(2, 2, 1.00, 0, 400e6 + 250e6 * 1j, 0 + 0 * 1j)
# _3BarrasPV.setBarras(3, 3, 1.04, 0, 0 + 0 * 1j, 200e6 + 0 * 1j)


# _3Barras.printBarras()  # Método utilizado para printar os valores atuais nas barras.

# _3Barras.setSesp()  # Método utilizado para setar os valores Especificados de Potência em cada barra.


# """
# Instanciação das ligações de cada barra através do método "ligacoes". Mais informações sobre este 
# método podem ser obtidas no arquivo "classNewton". 
# """
# _3Barras.ligacoes(1, 2, impedancia=0.02 + 0.04j)
# _3Barras.ligacoes(1, 3, impedancia=0.01 + 0.03j)
# _3Barras.ligacoes(2, 3, impedancia=0.0125 + 0.025j)

# _3Barras.printLigacoes()  # Método utilizado para printar as ligações do sistema.

# _3Barras.solveCircuito(iteracoes=None, listTensao=[2, 3], listAng=[2, 3], erro=1e-3)



# """
# Cálculo do fluxo de potência em todo o circuito através do método "FluxoS". 
# Para visualizar os valores das tensões em cada barra, basta passar o parâmetro "printTensao" como 
# True. 
# Para visualizar os valores das correntes em cada ligação, basta passar o parâmetro "pintCorrentes" 
# como True. 
# Caso não queira, basta não passar nenhum parâmetro. 
# """
# _3Barras.FluxoS(printTensao=True, printCorrentes=True)

# _3Barras.Perdas()  # Cálculo das perdas totais no circuito através do método "Perdas". É o
# # somatório do passo 10 da aula

# _3Barras.plotDados(tensao=True, ang=True)  # Plotagem das convergências dos valores de tensão e
# # de ângulo.

# _3Barras.printBarras()


# _3BarrasPV.printBarras()  # Método utilizado para printar os valores atuais nas barras.


# _3BarrasPV.setSesp()  # Método utilizado para setar os valores Especificados de Potência em cada barra.

# """
# Instanciação das ligações de cada barra através do método "ligacoes". Mais informações sobre este 
# método podem ser obtidas no arquivo "classNewton". 
# """
# _3BarrasPV.ligacoes(1, 2, impedancia=0.02 + 0.04j)
# _3BarrasPV.ligacoes(1, 3, impedancia=0.01 + 0.03j)
# _3BarrasPV.ligacoes(2, 3, impedancia=0.0125 + 0.025j)


# _3BarrasPV.printLigacoes()  # Método utilizado para printar as ligações do sistema.


# _3BarrasPV.solveCircuito(iteracoes=None, listTensao=[2], listAng=[2, 3], erro=1e-3)

# """
# Cálculo do fluxo de potência em todo o circuito através do método "FluxoS". 
# Para visualizar os valores das tensões em cada barra, basta passar o parâmetro "printTensao" como 
# True. 
# Para visualizar os valores das correntes em cada ligação, basta passar o parâmetro "pintCorrentes" 
# como True. 
# Caso não queira, basta não passar nenhum parâmetro. 
# """
# _3BarrasPV.FluxoS(printTensao=True, printCorrentes=True)

# _3BarrasPV.Perdas()  # Cálculo das perdas totais no circuito através do método "Perdas". É o
# # somatório do passo 10 da aula

# _3BarrasPV.plotDados(tensao=True, ang=True)  # Plotagem das convergências dos valores de tensão e
# # de ângulo.

# _3BarrasPV.printBarras()




# Avaliacao = Newton()  # Esta linha instancia a classe "Newton", criada em outro arquivo.

# """
# Instanciação das barras através do método "setBarras". Seguem a seguinte ordem: 

# Barra, Código da barra, Tensão na barra [pu], Ângulo da tensão [graus], Carga [P + Qj] (VA), Geração [P + Qj] (VA)

# Mais informações sobre este e outros métodos podem ser obtidos no arquivo "classNewton". 

# """
# Avaliacao.setBarras(1, 1, 1.07, 0, 0 + 0 * 1j, 0 + 0 * 1j)
# Avaliacao.setBarras(2, 3, 1.05, 0, 0 + 0 * 1j, 50e6 + 0 * 1j)
# Avaliacao.setBarras(3, 3, 1.05, 0, 0 + 0 * 1j, 50e6 + 0 * 1j)
# Avaliacao.setBarras(4, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)
# Avaliacao.setBarras(5, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)
# Avaliacao.setBarras(6, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)

# Avaliacao.printBarras()  # Método utilizado para printar os valores atuais nas barras.

# Avaliacao.setSesp()  # Método utilizado para setar os valores Especificados de Potência em cada barra.

# """
# Instanciação das ligações de cada barra através do método "ligacoes". Mais informações sobre este 
# método podem ser obtidas no arquivo "classNewton". 
# """
# Avaliacao.ligacoes(1, 2, impedancia=0.1 + 0.2j)
# Avaliacao.ligacoes(1, 4, impedancia=0.05 + 0.2j)
# Avaliacao.ligacoes(1, 5, impedancia=0.08 + 0.3j)
# Avaliacao.ligacoes(2, 3, impedancia=0.05 + 0.25j)
# Avaliacao.ligacoes(2, 4, impedancia=0.05 + 0.1j)
# Avaliacao.ligacoes(2, 5, impedancia=0.1 + 0.3j)
# Avaliacao.ligacoes(2, 6, impedancia=0.07 + 0.2j)
# Avaliacao.ligacoes(3, 5, impedancia=0.12 + 0.26j)
# Avaliacao.ligacoes(3, 6, impedancia=0.02 + 0.1j)
# Avaliacao.ligacoes(4, 5, impedancia=0.2 + 0.4j)
# Avaliacao.ligacoes(5, 6, impedancia=0.1 + 0.3j)

# Avaliacao.printLigacoes()  # Método utilizado para printar as ligações do sistema.

# """
# Resolução do problema através do método "solveCircuito". Os parâmetros deste método são: 
#     * iteracoes     --> Caso queira definir um número exato de iterações para o cálculo. 
#     * erro          --> Caso queira definir um erro esfecífico para o teste de parada do 
#                         algoritmo (se não quiser definir o número de iterações). 
#     * listTensao    --> Deve-se passar o número das barras que se deseja saber a tensão (Barras PQ). 
#     * listAng       --> Deve-se passar o número das barras que se deseja saber o ângulo (Barras PQ e PV).
# """
# Avaliacao.solveCircuito(iteracoes=None, listTensao=[4, 5, 6], listAng=[2, 3, 4, 5, 6], erro=1e-13)

# """
# Cálculo do fluxo de potência em todo o circuito através do método "FluxoS". 
# Para visualizar os valores das tensões em cada barra, basta passar o parâmetro "printTensao" como 
# True. 
# Para visualizar os valores das correntes em cada ligação, basta passar o parâmetro "pintCorrentes" 
# como True. 
# Caso não queira, basta não passar nenhum parâmetro. 
# """
# Avaliacao.FluxoS(printTensao=True, printCorrentes=True)

# Avaliacao.Perdas()  # Cálculo das perdas totais no circuito através do método "Perdas". É o
# # somatório do passo 10 da aula

# Avaliacao.plotDados(tensao=True, ang=True)  # Plotagem das convergências dos valores de tensão e
# # de ângulo.

# Avaliacao.printBarras()




Exemplo = Newton() 

Exemplo.setBarras(1, 1, 1.05, 0.00, 0 + 0 * 1j, 0 + 0 * 1j)
Exemplo.setBarras(2, 2, 1.00, 0.00, 400e6 + 250e6 * 1j, 0 + 0 * 1j)
Exemplo.setBarras(3, 3, 1.04, 0.00, 0 + 0 * 1j, 200e6 + 0 * 1j)

Exemplo.printBarras()
Exemplo.setSesp()

Exemplo.ligacoes(1, 2, impedancia=0.02 + 0.04j)
Exemplo.ligacoes(1, 3, impedancia=0.01 + 0.03j)
Exemplo.ligacoes(2, 3, impedancia=0.0125 + 0.025j)

Exemplo.printLigacoes()

Exemplo.solveCircuito(iteracoes=None, listTensao=[2], listAng=[2,3], erro=0.001)
