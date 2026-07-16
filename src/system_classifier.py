# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np


class SystemClassifier:
    def __init__(self, app):
        self.app = app

        self.empty = True
        self.integrator = False
        self.integrator_k = False
        self.stable = True
        self.causal = True
        self.trivial = False

    def info(self):
        if self.empty:
            msg = "Sistema vazio."
        elif self.trivial:
            msg = ("Sistema trivial, pois todos os polos e zeros se cancelam")
        elif self.integrator:
            if self.integrator_k:
                msg = (
                    "O sistema se comporta como um possível integrador digital"
                )
            else:
                msg = (
                    "O sistema se comporta como um integrador digital"
                )
        elif not self.causal:
            msg = (
                "O sistema é irrealizável (não causal), pois o grau do "
                "denominador da Função de Transferência é menor que o "
                "grau do numerador."
                "\n\n"
                "Por isso, as respostas ao impulso e ao degrau unitário "
                "não serão exibidas."
            )
        else:
            msg = (
                "O sistema é realizável (causal), pois o grau do "
                "denominador da Função de Transferência é maior ou "
                "igual ao o grau do numerador."
            )

            if self.stable:
                msg += (
                    "\n\n"
                    "O sistema é estável, pois todos os seus polos estão "
                    "dentro da circunferência de raio unitário."
                )
            else:
                msg += (
                    "\n\n"
                    "O sistema é instável, pois pelo menos um de seus "
                    "polos está fora ou sobre a circunferência de raio "
                    "unitário."
                )

        return msg

    def update(self):
        poles = self.app.poles
        zeros = self.app.zeros

        self.trivial = False
        self.empty = False
        self.integrator = True
        self.integrator_k = False
        self.causal = True
        self.stable = True

        if zeros.num_elements() == 0 and poles.num_elements() == 0:
            text = ""
            bg = None
            self.empty = True
        else:
            if poles.num_elements() == 0:
                self.integrator = False

            for pair_p in poles.list:
                p1 = pair_p[0]
                x = p1.real
                y = p1.imag
                if x != 1 or y != 0:
                    self.integrator = False
                    break

            if zeros.num_elements() > poles.num_elements():
                text = "Sistema Irrealizável"
                bg = "red"
                self.causal = False
            elif self.integrator:
                if zeros.num_elements() > 0:
                    degree = poles.num_elements()

                    only_zeros_1_0 = True  # only at (1,0)
                    for pair in zeros.list:
                        z = pair[0]
                        if z.real == 1 and z.imag == 0:
                            degree -= 1
                        else:
                            only_zeros_1_0 = False
                            break

                    if only_zeros_1_0:
                        if degree == 0:
                            self.trivial = True
                            text = ""
                            bg = None
                        elif degree > 0:
                            text = f"Integrador de grau {degree}"
                            bg = "green"
                        else:  # more zeros than poles at (1,0)
                            self.integrator_k = True
                            text = "Integrador com constante"
                            bg = "green"
                    else:
                        self.integrator_k = True
                        text = "Integrador com constante"
                        bg = "green"
                else:
                    text = f"Integrador de grau {poles.num_elements()}"
                    bg = "green"
            else:
                for pair_p in poles.list:
                    p1 = pair_p[0]
                    x = p1.real
                    y = p1.imag
                    r = np.sqrt(x**2 + y**2)
                    if r >= 1:
                        text = "Sistema Realizável e Instável"
                        self.stable = False
                        bg = "red"
                        break
                if self.stable:
                    text = "Sistema Realizável e Estável"
                    bg = "green"

        return text, bg
