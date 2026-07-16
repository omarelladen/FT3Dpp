# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np


class SystemClassifier:
    def __init__(self, app):
        self.app = app

        self.sys_empty = True
        self.sys_integrator = False
        self.sys_integrator_zeros = False
        self.sys_stable = True
        self.sys_causal = True

    def info(self):
        if self.sys_empty:
            msg = "Sistema vazio."
        elif self.sys_integrator:
            if self.sys_integrator_zeros:
                msg = (
                    "O sistema se comporta como um possível integrador digital"
                )
            else:
                msg = (
                    "O sistema se comporta como um integrador digital"
                )
        elif not self.sys_causal:
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

            if self.sys_stable:
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

        if zeros.num_elements() == 0 and poles.num_elements() == 0:
            text = ""
            bg = None
            self.sys_empty = True
        else:
            self.sys_empty = False

            self.sys_integrator = True
            if poles.num_elements() == 0:
                self.sys_integrator = False
            for pair_p in poles.list:
                p1 = pair_p[0]
                x = p1.real
                y = p1.imag
                if x != 1 or y != 0:
                    self.sys_integrator = False
                    break
            if self.sys_integrator:
                if zeros.num_elements() > 0:
                    self.sys_integrator_zeros = True
                    text = "Integrador com constante"
                    bg = "green"
                else:
                    self.sys_integrator_zeros = False
                    text = f"Integrador de grau {poles.num_elements()}"
                    bg = "green"

            elif zeros.num_elements() > poles.num_elements():
                text = "Sistema Irrealizável"
                bg = "red"
                self.sys_causal = False
            else:
                self.sys_causal = True
                self.sys_stable = True
                for pair_p in poles.list:
                    p1 = pair_p[0]
                    x = p1.real
                    y = p1.imag
                    r = np.sqrt(x**2 + y**2)
                    if r >= 1:
                        text = "Sistema Realizável e Instável"
                        self.sys_stable = False
                        bg = "red"
                        break
                if self.sys_stable:
                    text = "Sistema Realizável e Estável"
                    bg = "green"

        return text, bg
