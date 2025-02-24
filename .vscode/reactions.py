from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents GUI errors
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
import numbers

app = Flask(__name__)

# Ensure static/images directory exists
if not os.path.exists("static/images"):
    os.makedirs("static/images")

@app.route('/reaction/', methods=['GET', 'POST'])
def reactions():
    if request.method == 'POST':
        selected_order = request.form.get('order')
        try:
            k = float(request.form.get("rate"))
            C0 = float(request.form.get("concentration"))
            time_limit = float(request.form.get("time"))
        except ValueError:
            return render_template('index.html', error="Error: Please enter valid numbers!", order=selected_order)

        plt.clf()  # Clear the plot before each new render
        t = np.linspace(0, time_limit, 1000)

        if selected_order == "zero":
            C = np.maximum(C0 - k * t, 0)  # Zero-order reaction equation
            plt.plot(t, C, label='[A] (Concentration)', color='b')
            plt.title('Zero-Order Reaction Kinetics')

        elif selected_order == "one":
            def first_order_reaction(t, C):
                return -k * C

            solution = solve_ivp(first_order_reaction, (0, time_limit), [C0], t_eval=t, method='RK45')
            plt.plot(solution.t, solution.y[0], label='[A] (Concentration)', color='b')
            plt.title('First-Order Reaction Kinetics')

        elif selected_order == "two":
            def second_order_reaction(t, C):
                return -k * C**2

            solution = solve_ivp(second_order_reaction, (0, time_limit), [C0], t_eval=t, method='RK45')
            plt.plot(solution.t, solution.y[0], label='[A] (Concentration)', color='b')
            plt.title('Second-Order Reaction Kinetics')

        else:
            return render_template('index.html', error="Error: Invalid reaction order!", order=selected_order)

        # Final plot settings
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (mol/L)')
        plt.legend()
        plt.grid()
        plt.savefig('static/images/figure.png')

        return render_template('index.html', order=selected_order, rate=k, concentration=C0, time=time_limit)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=False)
