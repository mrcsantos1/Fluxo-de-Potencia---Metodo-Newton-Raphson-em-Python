from classNewton import Newton

Circuito1 = Newton()

Circuito1.setBarras(1, 1, 1.05, 0, 0 + 0 * 1j, 0 + 0 * 1j)
Circuito1.setBarras(2, 2, 1, 0, 256.6e6 + 110.2e6 * 1j, 0 + 0 * 1j)
Circuito1.setBarras(3, 2, 1, 0, 138.6e6 + 45.2e6 * 1j, 0 + 0 * 1j)

Circuito1.printBarras()


Circuito1.setSesp()

Circuito1.ligacoes(1, 2, impedancia=0.02+0.04*1j)
Circuito1.ligacoes(1, 3, impedancia=0.01 + 0.03*1j)
Circuito1.ligacoes(2, 3, impedancia=0.0125 + 0.025*1j)

Circuito1.printLigacoes()

Circuito1.solveCircuito(iteracoes=None, listTensao=[2,3], listAng=[2,3], erro=1e-3)

## É melhor fazer outro
