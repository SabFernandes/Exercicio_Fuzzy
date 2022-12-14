# -*- coding: utf-8 -*-
"""Intenção de votos - FUZZY

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1soPQ912_6nShfkb13OK_aprUXxYRIr49
"""

!pip install -U scikit-fuzzy
!pip install -U matplotlib

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl

if __name__ == "__main__":
  print('Exemplo')

  #Variáveis de entrada
  campanha = ctrl.Antecedent(np.arange(0, 101, 1), 'Campanha')
  faixa_etaria = ctrl.Antecedent(np.arange(0, 101, 1), 'Faixa Etária')

  #Variável de saida
  intencao_voto = ctrl.Consequent(np.arange(0, 101, 1), 'Intenção de votos')

  #Variáveis/fuzzyficação - Definições das funções de pertinência

  #Campanha
  campanha['boa'] = fuzz.trapmf(campanha.universe, [0, 0, 30, 50])
  campanha['medio'] = fuzz.trimf(campanha.universe, [30, 50, 70])
  campanha['ruim'] = fuzz.trapmf(campanha.universe, [50, 70, 100, 100])

  #Faixa Etária
  faixa_etaria['jovem'] = fuzz.trapmf(faixa_etaria.universe, [0, 0, 30, 50])
  faixa_etaria['adulto'] = fuzz.trimf(faixa_etaria.universe, [30, 50, 70])
  faixa_etaria['idoso'] = fuzz.trapmf(faixa_etaria.universe, [50, 70, 100, 100])

  #Intenção de votos
  intencao_voto['baixo'] = fuzz.trapmf(intencao_voto.universe, [0, 0, 30, 50])
  intencao_voto['medio'] = fuzz.trimf(intencao_voto.universe, [30, 50, 70])
  intencao_voto['alto'] = fuzz.trapmf(intencao_voto.universe, [50, 70, 100, 100])

  #Visualização das funções de pertinência
  campanha.view()
  faixa_etaria.view()
  intencao_voto.view()

  plt.show()

#definição das regras
  regra1 = ctrl.Rule(campanha['boa'] | faixa_etaria['jovem'], intencao_voto['alto'])
  regra2 = ctrl.Rule(campanha['medio'] & faixa_etaria['adulto'], intencao_voto['medio'])
  regra3 = ctrl.Rule(campanha['ruim'], intencao_voto['baixo'])

  #ativação das regras
  controle_intencao_voto = ctrl.ControlSystem([regra1, regra2, regra3])
  simulador_intencao_voto = ctrl.ControlSystemSimulation(controle_intencao_voto)

  #passa as predições dos modelos para suas respectivas variáveis de entrada
  simulador_intencao_voto.input['Campanha'] = 60
  simulador_intencao_voto.input['Faixa Etária'] = 48

  # calcula a saída do sistema de controle fuzzy
  simulador_intencao_voto.compute()
    
  #agregação - retorna o valor crisp e o gráfico mostrando-o
  print(simulador_intencao_voto.output['Intenção de votos'])
  intencao_voto.view(sim=simulador_intencao_voto)
  plt.show()