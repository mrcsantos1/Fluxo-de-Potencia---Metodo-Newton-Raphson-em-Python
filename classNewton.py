"""
Programa desenvolvido por Marcos Alves dos Santos -- 201710421.

Este é o arquivo secundário, no qual consta a classe "Newton", cujos métodos e atributos são 
utilizados no arquivo principal "main".

Todos os valores já estão definidos de acordo com o exercício avaliativo no arquivo "main".
"""

import cmath as cmt
import math as mt

import matplotlib.pyplot as plt
import numpy as np


class Newton:
    def __init__(self):
        self.Sbase = 100e6
        self.Vbase = 230e3
        self.__dados = dict()
        self.__Sesp = dict()
        self.__Ligacoes = dict()
        self.__ybus = []
        self.__SresiduoPQ = dict()
        self.__SresiduoPV = dict()
        self.__J1 = []
        self.__J2 = []
        self.__J3 = []
        self.__J4 = []
        self.__Jacob = []
        self.__listTensao = []
        self.__listAng = []
        self.__PeQ = []
        self.__Sfolga = []
        self.__fluxoS = dict()
        self.count = 0
        self.__tensaoPlot = dict()
        self.__angPlot = dict()
        self.__control = bool()
        self.__x = []
        self.__I = dict()
        self.__V = dict()
        self.__S = dict()
        self.__nPQ = int()
        self.__nPV = int()
        self.__Sbarras = dict()
        self.__ResiduoP = []
        self.__ResiduoQ = []
        self.__deltaPeQ = []
        self.__Perdas = 0

    def setBarras(self, barra, code, tensao, ang, carga, geracao):
        """
        Este método é utilizado apenas para setar (adicionar/atualizar) os valores iniciais de cada barra do
        sistema.
        :param barra: Representa o número de cada barra.
        :param code: Representa o tipo de cada barra (1 : Tensão e Ângulo; 2 : P e Q; 3 : P e V).
        :param tensao: Módulo da tensão na barra.
        :param ang: Valor do ângulo de fase cada barra. Colocá-lo em GRAUS. 
        :param carga: P e Q de carga em cada barra.
        :param geracao: P e Q de geração em cada barra.

        :return: Este método não retorna nada. Apenas modifica/seta os valores para o algoritmo. 
        """
        self.__dados[barra] = {'code': code, 'tensao': tensao, 'ang': mt.radians(ang),
                               'carga': (carga / self.Sbase), 'geracao': (geracao / self.Sbase)}
        self.__tensaoPlot[barra] = [tensao]
        self.__angPlot[barra] = [ang]

    def printBarras(self):
        """
        Método utilizado para printar todos os valores em cada barra.
        """
        print('\n\n=============================== DADOS: =================================')
        for i in self.__dados:
            print(self.__dados[i])
        print('========================================================================')

    def setSesp(self):
        """
        Método utilizado para calcular a potência especificada em cada barra. Os valores
        são printados automaticamente.
        """
        for i in self.__dados:
            if self.__dados[i]['code'] == 2:
                self.__Sesp[i] = {'Pesp': np.real(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga']),
                                  'Qesp': float(
                                      np.imag(self.__dados.get(i)['geracao']) - np.imag(self.__dados.get(i)['carga']))
                                  }
            elif self.__dados[i]['code'] == 3:
                self.__Sesp[i] = {'Pesp': np.real(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga']),
                                  'Qesp': float(
                                      np.imag(self.__dados.get(i)['geracao']) - np.imag(self.__dados.get(i)['carga']))
                                  }
        print('\n\n=============================== Sesp: =================================')
        print(self.__Sesp, ' pu')
        print('========================================================================')

    def ligacoes(self, barra1, barra2, impedancia=None, admitancia=None):
        """
        Método utilizado para setar as ligações entre cada barra.

        :param barra1: Barra de origem.
        :param barra2: Barra destino.
        :param impedancia: Valor em PU da impedância.
        :param admitancia: Valor em PU da admitância.

        É necessário informar um valor de admitância ou de impedância.
        """
        if impedancia is None:
            impedancia = 1 / admitancia
        elif admitancia is None:
            admitancia = 1 / impedancia
        else:
            return 'ERRO! É NECESSÁRIO INFORMAR O VALOR DE IMPEDÂNCIA OU DE ADMITÂNCIA DA LINHA! '

        self.__Ligacoes[(barra1, barra2)] = {'Impedância': impedancia,
                                             'Admitância': admitancia}

    def printLigacoes(self):
        """
        Método utilizado para printar as ligações do circuito.
        """
        print('\n\n====================================== Ligações: =============================================')
        for i in self.__Ligacoes:
            print('Ligação = ', i, '\t', self.__Ligacoes[i])
        print('==============================================================================================')

    def __printYbus(self):
        """
        Método privado utilizado apenas para printar os valores da matriz ybus.
        """
        print('\n\n============================= YBUS: ====================================')
        for i in self.__ybus: print(i)
        print('========================================================================')

    def ybus(self):
        """
        Método utilizado para calcular a matriz ybus. O cálculo é feito com base no que foi
        visto em aula.
        """
        for i in range(len(self.__dados)):
            lin = []
            for j in range(len(self.__dados)):
                if i == j:

                    lin.append(0)
                else:
                    if self.__Ligacoes.__contains__(tuple([i + 1, j + 1])):
                        lin.append(-self.__Ligacoes.get(tuple([i + 1, j + 1]))['Admitância'])
                    elif self.__Ligacoes.__contains__(tuple([j + 1, i + 1])):
                        lin.append(-self.__Ligacoes.get(tuple([j + 1, i + 1]))['Admitância'])
                    else:
                        lin.append(0)
            for j in range(len(self.__dados)):
                if i == j:
                    lin[j] = -1 * sum(lin)
            self.__ybus.append(lin)

        self.__printYbus()

        for i in self.__dados:
            if self.__dados.get(i)['code'] == 2:
                self.__nPQ += 1
            elif self.__dados.get(i)['code'] == 3:
                self.__nPV += 1

    def Sinjetada(self):
        """
        Método utilizado para calcular as potências injetadas no circuito conforme o passo
        número 2 da aula 16. E seta os valores de delta P e de delta Q, conforme o passo
        número 3 da aula 16.
        """
        self.__Sinjetada = dict()
        self.__deltaPeQ = []
        self.__ResiduoP = []
        self.__ResiduoQ = []

        for i in self.__dados:
            soma1 = []
            soma2 = []
            if self.__dados[i]['code'] != 1:
                for j in self.__dados:
                    soma1.append(  # Apenas Potência ATIVA
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.cos(np.angle(self.__ybus[i - 1][j - 1]) - self.__dados.get(i)['ang'] + self.__dados.get(j)[
                            'ang'])
                    )
                    soma2.append(  # Apenas Potência REATIVA
                        -abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.sin(np.angle(self.__ybus[i - 1][j - 1]) - self.__dados.get(i)['ang'] + self.__dados.get(j)[
                            'ang']) * 1j
                    )

                self.__ResiduoP.append(np.real(
                    self.__Sesp.get(i)['Pesp'] - sum(soma1)))  # Lista com os valores de cada barra != da barra |V| phi
                if self.__dados[i]['code'] == 2:
                    self.__ResiduoQ.append(np.imag((self.__Sesp.get(i)['Qesp']) * 1j - sum(soma2)))

        for i in range(len(self.__ResiduoP)):
            self.__deltaPeQ.append(self.__ResiduoP[i])
        for i in range(len(self.__ResiduoQ)):
            self.__deltaPeQ.append(self.__ResiduoQ[i])  # SEM O j

        for i in self.__deltaPeQ: print(i)

    def __setJ1(self, listAng, nPQ, nPV):
        """
        Método privado utilizado para calcular a submatriz J1 da matriz Jacobiana.

        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)
        :param nPQ: Número de barras PQ.
        :param nPV: Número de barras PV.
        :return: Retorna a submatriz J1.
        """
        self.__J1 = np.ones((nPQ + nPV, nPQ + nPV))

        mainDiagonal = []
        outDiagonal = []
        for i in listAng:
            soma = []
            for j in range(1, len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
            mainDiagonal.append(sum(soma))

        for i in listAng:
            for j in listAng:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
        m = 0
        for i in range(len(listAng)):
            # m = 0
            for j in range(len(listAng)):
                if i == j:
                    self.__J1[i][j] = np.real(mainDiagonal[j])
                else:
                    self.__J1[i][j] = np.real(outDiagonal[m])
                    m += 1
        return self.__J1

    def __setJ2(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado utilizado para calcular a submatriz J2 da matriz Jacobiana.

        :param listTensao: Lista de tensões a serem calculadas no circuito. (Barras PQ)
        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)
        :param nPQ: Número de barras PQ.
        :param nPV: Número de barras PV.
        :return: Retorna a submatriz J2.
        """
        self.__J2 = np.ones((nPQ + nPV, nPQ))

        mainDiagonal = []
        outDiagonal = []

        for i in listAng:
            soma = []
            a = 0
            for j in range(1, len(self.__dados) + 1, 1):

                if i != j:
                    soma.append(
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
            a = (2 * abs(self.__dados.get(i)['tensao']) * abs(self.__ybus[i - 1][i - 1]) *
                 cmt.cos(cmt.phase(self.__ybus[i - 1][i - 1]))
                 )
            mainDiagonal.append(a + sum(soma))

        for i in listAng:
            for j in listTensao:
                if i != j:
                    outDiagonal.append(
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
        m = 0
        for i in range(nPQ + nPV):
            k = nPV
            for j in range(nPQ):
                if i < nPV:
                    self.__J2[i][j] = np.real(outDiagonal[m])
                    m += 1
                elif i >= nPV:
                    if i - nPV == j:
                        self.__J2[i][j] = np.real(mainDiagonal[j + nPV])
                        k += 1
                    else:
                        self.__J2[i][j] = np.real(outDiagonal[m])
                        m += 1

        return self.__J2

    def __setJ3(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado utilizado para calcular a submatriz J3 da matriz Jacobiana.

        :param listTensao: Lista de tensões a serem calculadas no circuito. (Barras PQ)
        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)
        :param nPQ: Número de barras PQ.
        :param nPV: Número de barras PV.
        :return: Retorna a submatriz J3.
        """
        self.__J3 = np.ones((nPQ, nPQ + nPV))

        mainDiagonal = []
        outDiagonal = []
        for i in listAng:
            soma = []
            for j in range(1, len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
            mainDiagonal.append(sum(soma))
        for i in listAng:
            for j in listAng:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
        # m = 0
        k = (len(listAng) + len(listTensao))

        for i in range(nPQ):
            for j in range(nPQ + nPV):
                if j < nPV:
                    # print('k = ', k)
                    self.__J3[i][j] = np.real(outDiagonal[k])
                    k += 1
                elif j >= nPV:
                    if j - nPV == i:
                        self.__J3[i][j] = np.real(mainDiagonal[i + nPV])
                    else:
                        self.__J3[i][j] = np.real(outDiagonal[k])
                        k += 1
        return self.__J3

    def __setJ4(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado utilizado para calcular a submatriz J4 da matriz Jacobiana.

        :param listTensao: Lista de tensões a serem calculadas no circuito. (Barras PQ)
        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)
        :param nPQ: Número de barras PQ.
        :param nPV: Número de barras PV.
        :return: Retorna a submatriz J4.
        """
        self.__J4 = np.ones((nPQ, nPQ))

        mainDiagonal = []
        outDiagonal = []
        for i in listAng:
            soma = []
            a = 0
            for j in range(1, len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
            a = (2 * abs(self.__dados.get(i)['tensao']) * abs(self.__ybus[i - 1][i - 1]) *
                 cmt.sin(cmt.phase(self.__ybus[i - 1][i - 1]))
                 )
            mainDiagonal.append(-a - sum(soma))
        for i in listAng:
            for j in listTensao:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i - 1][j - 1]) -
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang'])
                    )
        k = nPQ + nPV + 1
        for i in range(nPQ):
            for j in range(nPQ):
                if i == j:
                    self.__J4[i][j] = np.real(mainDiagonal[j + nPV])
                else:
                    self.__J4[i][j] = np.real(outDiagonal[k])
                    k += 1
        return self.__J4

    def setJacob(self, listTensao, listAng):
        """
        Método utilizado para calcular a matriz Jacobiana.

        :param listTensao: Lista de tensões a serem calculadas no circuito. (Barras PQ)
        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)

        Printa a matriz Jacobiana.
        """

        nPQ = 0
        nPV = 0
        for i in self.__dados:
            if self.__dados.get(i)['code'] == 2:
                nPQ += 1
            elif self.__dados.get(i)['code'] == 3:
                nPV += 1

        self.__Jacob = []
        self.__listTensao = listTensao
        self.__listAng = listAng
        nXn = len(listTensao) + len(listAng)

        J1 = self.__setJ1(listAng, nPQ, nPV)  # (nPQ  + nPV) X (nPQ + nPV)
        J2 = self.__setJ2(listTensao, listAng, nPQ, nPV)  # (nPQ  + nPV) X (nPQ)
        J3 = self.__setJ3(listTensao, listAng, nPQ, nPV)  # (nPQ) X (nPQ + nPV)
        J4 = self.__setJ4(listTensao, listAng, nPQ, nPV)  # (nPQ) X (nPQ)

        self.__Jacob = np.zeros((nXn, nXn))

        for i in range(nXn):
            h = []
            k = []
            if i < len(J1):
                for j in range(len(J1[i])): h.append(J1[i][j])
                for j in range(len(J2[i])): h.append(J2[i][j])
                # geral[i] = np.hstack(h)
                self.__Jacob[i] = np.hstack(h)
            elif i >= len(J1):
                m = i - len(J1)
                for j in range(len(J3[m])): k.append(J3[m][j])
                for j in range(len(J4[m])): k.append(J4[m][j])
                # geral[i] = np.hstack(k)
                self.__Jacob[i] = np.hstack(k)

        print('\n\n==================== MATRIZ JACOBIANA: ===========================')
        print('\nJ1 = ')
        for i in J1: print(i)
        print('\nJ2 = ')
        for i in J2: print(i)
        print('\nJ3 = ')
        for i in J3: print(i)
        print('\nJ4 = ')
        for i in J4: print(i)
        print('\nJACOB = ')
        for i in self.__Jacob: print(i)
        print('========================================================================')

    def linearSystem(self):
        """
        Método utilizado para calcular os resultados do sistema linear do passo 6 da aula 13.
        O sistema é do tipo:
            [delta P delta Q] = [Jacobiana] . [Resultado]
        """
        self.__x = []
        self.__x = np.linalg.solve(self.__Jacob, self.__deltaPeQ)
        deucerto = np.allclose(np.dot(self.__Jacob, self.__x), self.__deltaPeQ)
        print('\n\t\tDEU CERTO? ', deucerto)
        # print('\n\n==== RESULTADO VETOR "x" ÂNG,|V| (Linear System) DA ÚLTIMA ITERAÇÃO: ==========')
        # print('===============================================================================')
        # for i in self.__x:
        #     print('ang ou tensão = ', i)
        # print('===============================================================================')
        ang = []
        tens = []
        for i in range(len(self.__x)):
            if i < (self.__nPQ + self.__nPV):
                ang.append(self.__x[i])
            else:
                tens.append(self.__x[i])
        m = 0
        for i in range(len(self.__dados)):
            if self.__dados.get(i + 1)['code'] != 1:
                # print('float(np.real(ang[m])) = ', float(np.real(ang[m])))
                self.__dados[i + 1]['ang'] += float(np.real(ang[m]))
                self.__angPlot[i + 1].append(self.__dados[i + 1]['ang'])
                m += 1
        m = 0
        for i in range(len(self.__dados)):
            if self.__dados.get(i + 1)['code'] == 2:
                # print('float(np.real(tens[m])) = ', float(np.real(tens[m])))
                self.__dados[i + 1]['tensao'] += float(np.real(tens[m]))
                self.__tensaoPlot[i + 1].append(self.__dados[i + 1]['tensao'])
                m += 1

    def NovaInjecao(self):
        """
        Método utilizado para calcular o novo valor de Injeção de potência aparente nas
        barras de folga e PV. (P e Q nas de folga e Q nas PV).
        Cálculo feito conforme o passo 9 da aula 13.
        """
        self.__Sbarras = dict()
        for i in self.__dados:
            soma1 = []
            soma2 = []
            if self.__dados[i]['code'] != 2:
                for j in self.__dados:
                    soma1.append(  # Apenas Potência ATIVA
                        abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.cos(np.angle(self.__ybus[i - 1][j - 1]) - self.__dados.get(i)['ang'] + self.__dados.get(j)[
                            'ang'])
                    )
                    soma2.append(  # Apenas Potência REATIVA
                        -abs(self.__ybus[i - 1][j - 1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.sin(np.angle(self.__ybus[i - 1][j - 1]) - self.__dados.get(i)['ang'] + self.__dados.get(j)[
                            'ang']) * 1j
                    )
            if self.__dados[i]['code'] == 1:
                self.__Sbarras[i] = {'P': np.real(sum(soma1)), 'Q': np.real(sum(soma2))}
            elif self.__dados[i]['code'] == 3:
                self.__Sbarras[i] = {'P': 0, 'Q': np.imag(sum(soma2))}

        for i in self.__dados:
            if self.__dados[i]['code'] == 1:
                self.__dados[i]['geracao'] = self.__Sbarras.get(i)['P'] + self.__Sbarras.get(i)['Q'] * 1j
            elif self.__dados[i]['code'] == 3:
                self.__dados[i]['geracao'] = np.real(self.__dados.get(i)['geracao']) + self.__Sbarras.get(i)['Q'] * 1j
        # print('self.__Sbarras = \n', self.__Sbarras)

    def solveCircuito(self, erro=None, iteracoes=None, listTensao=None, listAng=None):
        """
        Método genérico utilizado para 'resolver' o circuito.

        :param erro: Valor do erro utilizado para parar as iterações.
        :param iteracoes: Número de iterações que se deseja repetir o cálculo.
            Obs.: Deve-se passar ou um número de iterações ou um número para o erro.
        :param listTensao: Lista de tensões a serem calculadas no circuito. (Barras PQ)
        :param listAng: Lista de ângulos a serem calculados no circuito. (Barras PQ e PV)
        """
        self.__listTensao = listTensao
        self.__listAng = listAng
        self.count = 1
        self.ybus()
        self.Sinjetada()
        self.setJacob(listTensao=self.__listTensao, listAng=self.__listAng)
        self.linearSystem()

        if iteracoes is None and erro is not None:
            pEq = list(map(abs, self.__deltaPeQ))
            teste = list(map(lambda m: True if (m < erro) else False, pEq))
            stop = teste.count(False)
            while True:
                self.Sinjetada()
                self.setJacob(listTensao=self.__listTensao, listAng=self.__listAng)
                self.linearSystem()
                self.count += 1
                pEq = list(map(abs, self.__deltaPeQ))
                teste = list(map(lambda m: True if (m < erro) else False, pEq))
                stop = teste.count(False)
                # print('\n\nstop = ', stop, '\n\n')
                if stop == 0:
                    break
        elif iteracoes is not None and erro is None:
            while self.count < iteracoes:
                self.Sinjetada()
                self.setJacob(listTensao=self.__listTensao, listAng=self.__listAng)
                self.linearSystem()
                self.count += 1
                pEq = list(map(abs, self.__deltaPeQ))
                teste = list(map(lambda m: True if (m < erro) else False, pEq))
                stop = teste.count(False)

        self.NovaInjecao()
        # self.printBarras()
        if iteracoes is not None:
            print('\n======================= N° DE ITERAÇÕES = ', self.count)
        elif erro is not None:
            print('CONVERGIU PARA UM ERRO DE ', erro, ' .')
            print('CONVERGIU EM ', self.count, ' ITERAÇÕES. ')

    def __printTensao(self):
        """
        Método utilizado para printar os valores das tensões em cada barra. Em pu.
        """
        print('============================ TENSÕES: =======================================')
        for i in self.__V:
            print('Barra: \t', i, '\tTENSÃO = \t', self.__V.get(i), '\t[pu]')
        print('===============================================================================')

    def Tensoes(self, print=None):
        """
        Método utilizado para calcular as tensões em cada barra.
        O cálculo é feito a partir dos valores em pu e dos ângulos das tensões, os quais são
        oriundos das iterações do método "solveCircuito()".

        :param print: Caso dejese-se mostrar os valores das tensões em cada barra, deve-se passar
        True para o parâmetro "print".
        """
        self.__V = dict()
        for i in self.__dados:
            self.__V[i] = cmt.rect(self.__dados.get(i)['tensao'],
                                   self.__dados.get(i)['ang'])
        if print:
            self.__printTensao()

    def __printCorrentes(self):
        """
        Método utilizado para printar as correntes em cada ligação.
        """
        print('============================ CORRENTES: =======================================')
        for i in self.__I:
            print('Ligação: \t', i, '\tCorrente = \t', self.__I.get(i), '\t[pu]')
        print('===============================================================================')

    def Correntes(self, print=None):  # Correntes calculadas considerando os ângulos das tensões.
        """
        Método utilizado para calcular os valores das correntes em cada linha.
        O cálculo é feito para todas as barras. Portanto, nas barras que não há ligação,
        o resultado deve ser 0. As correntes que representam ligações com as mesmas barras,
        seus valores são calculados como o somatório de todas as correntes da barra sob análise.

        :param print: Caso dejese-se mostrar os valores das correntes, deve-se passar
        True para o parâmetro "print".
        """
        self.__I = dict()
        self.Tensoes(print=None)
        for i in self.__dados:
            soma = []
            for j in self.__dados:
                if i == j:
                    continue
                else:
                    self.__I[(i, j)] = ((self.__V.get(i) - self.__V.get(j)) * self.__ybus[i - 1][j - 1])
                soma.append(((self.__V.get(i) - self.__V.get(j)) * self.__ybus[i - 1][j - 1]))
            self.__I[(i, i)] = sum(soma)
        if print:
            self.__printCorrentes()

    def FluxoS(self, printTensao=None, printCorrentes=None):
        """
        Método responsável por calcular o fluxo de potência em todas as ligações do sistema.
        Cálculo baseado no passo 10 da aula 13.

        :param printTensao: Caso dejese-se mostrar os valores das tensões em cada barra, deve-se passar
        True para o parâmetro "print".
        :param printCorrentes: Caso dejese-se mostrar os valores das correntes, deve-se passar
        True para o parâmetro "print".
        """
        self.__fluxoS = dict()
        self.Tensoes(print=printTensao)
        self.Correntes(print=printCorrentes)
        for i in self.__I:
            a = i[0]
            self.__fluxoS[i] = self.__V.get(a) * np.conjugate(self.__I.get(i))
        print('======================== Fluxo de Potência: ===================================')
        for i in self.__fluxoS:
            print('Ligação: \t', i, '\tFluxo = \t', self.__fluxoS.get(i), '\t[pu]')
        print('===============================================================================')
        for i in self.__dados:
            if self.__dados.get(i)['code'] != 2:
                self.__dados[i]['geracao'] = -self.__fluxoS.get((i, i))

    def Perdas(self):
        """
        Método utilizado para calcular as perdas do circuito.
        O cálculo é realizado pela soma de todas as potências, conforme o passo 10 da aula 13.
        """
        self.__Perdas = 0
        perdas = []
        for i in self.__fluxoS:
            perdas.append(self.__fluxoS.get(i))
        self.__Perdas = sum(perdas)
        print('\n\nPerdas = \t', self.__Perdas, '\t[pu]')

    def __plotTensao(self):
        """
        Método privado utilizado apenas para plotar a convergência da tensão.
        """
        x = self.count
        barras = []
        y = []
        for i in self.__dados:
            if self.__dados.get(i)['code'] == 2:
                barras.append(i)
        for i in barras:
            y.append(self.__tensaoPlot.get(i))
        for i in range(len(barras)):
            plt.subplot(len(barras), 1, i + 1)
            plt.plot(range(x + 1), y[i])
            plt.title('Variação da tensão na barra ' + str(barras[i]) + ' X Número de iterações')
            plt.xlabel('Número de iterações ')
            plt.ylabel('Tensão na barra ' + str(barras[i]) + ' pu')
            plt.grid(True)
        plt.tight_layout()
        plt.show()

    def __plotAng(self):
        """
        Método privado utilizado apenas para plotar a convergência do ângulo das tensões nas barras.
        """
        x = self.count
        barras = []
        y = []
        for i in self.__dados:
            if self.__dados.get(i)['code'] != 1:
                barras.append(i)
        for i in barras:
            y.append(self.__angPlot.get(i))
        for i in range(len(barras)):
            plt.subplot(len(barras), 1, i + 1)
            plt.plot(range(x + 1), y[i])
            plt.title('Variação do ângulo na barra ' + str(barras[i]) + ' X Número de iterações')
            plt.xlabel('Número de iterações ')
            plt.ylabel('Ângulo na barra ' + str(barras[i]) + ' [rad]')
            plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plotDados(self, tensao=None, ang=None):
        """
        Método utilizado para plotar a convergência das tensões e dos ângulos calculados pelo algoritmo.

        :param tensao: Para plotar a tensão, deve-se passar "True" para este parâmetro.
        :param ang: Para plotar o ângulo, deve-se passar "True" para este parâmetro.
        """
        if tensao:
            self.__plotTensao()
        if ang:
            self.__plotAng()
