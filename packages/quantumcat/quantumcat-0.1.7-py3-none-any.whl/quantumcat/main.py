# (C) Copyright Artificial Brain 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from quantumcat.circuit import QCircuit
from quantumcat.utils import providers, constants, helper
from quantumcat.algorithms import GroversAlgorithm
from quantumcat.applications.generator import RandomNumber, Password, OTP


def create_circuit_demo():
    circuit = QCircuit(2)
    circuit.h_gate(0)
    circuit.cx_gate(0, 1)
    circuit.measure_all()
    circuit.draw_circuit(output='mpl', filename='test')
    # counts = circuit.execute(provider=providers.IBM_PROVIDER, repetitions=10)
    # print(counts)
    # print(circuit.compare_results())
    # circuit.plot_bar(counts=counts)


def randInt():
    import numpy as np
    p0 = 2 / 3
    p1 = 1 / 3
    p00 = 1 / 3
    p10 = 1 / 3
    theta0 = 2 * np.arccos(np.sqrt(p0))
    print(theta0)
    theta1 = 2 * np.arccos(np.sqrt(p00 / p0))
    print(theta1)
    theta2 = 2 * np.arccos(np.sqrt(p10 / p1))
    print(theta2)
    qc = circuit_bin4(theta0=theta0, theta1=theta1, theta2=theta2)

    aws_task = qc.execute(provider=providers.AMAZON_PROVIDER,
                          device="arn:aws:braket:::device/qpu/rigetti/Aspen-9",
                          bucket='amazon-braket-output-real-devices', directory='ionq-results')
    aws_task_status = aws_task.state()
    print('ID of task:', aws_task.id)
    print('Status of task:', aws_task_status)
    print(helper.aws_task(aws_task.id))


def circuit_bin4(theta0, theta1, theta2):
    """create |ψ2> state"""
    qc = QCircuit(2)
    qc.ry_gate(theta0, 0)
    qc.x_gate(0)
    qc.ry_gate(theta1/2, 1)
    qc.cx_gate(0, 1)
    qc.ry_gate(-theta1/2, 1)
    qc.cx_gate(0,1)
    qc.x_gate(0)
    qc.ry_gate(theta2/2, 1)
    qc.cx_gate(0, 1)
    qc.ry_gate(-theta2/2, 1)
    qc.cx_gate(0, 1)
    # === expanding |ψ1> into |ψ2> ===
    qc.measure_all()
    return qc


def grovers_demo():
    clause_list_sudoku = [[0, 1], [0, 2], [1, 3], [2, 3]]
    clause_list_light_board = [[0, 1, 3], [1, 0, 2, 4], [2, 1, 5], [3, 0, 4, 6],
                               [4, 1, 3, 5, 7], [5, 2, 4, 8], [6, 3, 7], [7, 4, 6, 8],
                               [8, 5, 7]]

    input_arr = [0, 0, 0, 1, 0, 1, 1, 1, 0]

    grovers_algorithm_unknown_solution = GroversAlgorithm(solution_known='N', clause_list=clause_list_light_board,
                                                          input_arr=input_arr, flip_output=True)

    grovers_algorithm_known_solution = GroversAlgorithm(solution_known='Y', search_keyword=101)

    results = grovers_algorithm_known_solution.execute(repetitions=10, provider=providers.AMAZON_PROVIDER)

    # grovers_algorithm_unknown_solution.draw_grovers_circuit()
    print(results)


def random_number_demo():
    random_number = RandomNumber(length=2, output_type=constants.DECIMAL)\
        .execute(provider=providers.AMAZON_PROVIDER)
    print(random_number)


def run_on_real_device():
    circuit = QCircuit(1)
    circuit.x_gate(0)
    circuit.measure_all()
    # circuit.draw_circuit(provider=providers.GOOGLE_PROVIDER)
    print(circuit.execute(provider=providers.IBM_PROVIDER, repetitions=10,
                          api=constants.IBM_API, device=constants.IBM_DEVICE_NAME))


def braket_demo():
    circuit = QCircuit(1)
    circuit.h_gate(0)
    circuit.measure_all()

    circuit.draw_circuit(provider=providers.AMAZON_PROVIDER)

    print(circuit.execute(provider=providers.AMAZON_PROVIDER))

    # To execute on real quantum device via aws
    # aws_task = circuit.execute(provider=providers.AMAZON_PROVIDER, device='',
    #                       bucket='', directory='')
    # aws_task_status = aws_task.state()
    # print('ID of task:', aws_task.id)
    # print('Status of task:', aws_task_status)
    # print(helper.aws_task(aws_task.id))


def password_demo():
    password = Password(8).generate()
    print(password)


def otp_demo():
    otp = OTP().generate()
    print(otp)


if __name__ == '__main__':
    create_circuit_demo()

