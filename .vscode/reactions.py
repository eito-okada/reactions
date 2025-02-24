# import stuff
from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

app = Flask(__name__)

# for stability when generating image
if not os.path.exists("static/images"):
    os.makedirs("static/images")

@app.route('/reaction/', methods=['GET', 'POST']) # route page to /reaction/ and fetch data from form
def reactions():
    if request.method == 'POST':
        selected_order = request.form.get('order')
        try: # get the numbers from form
            k = float(request.form.get("rate"))
            C0 = float(request.form.get("concentration"))
            time_limit = float(request.form.get("time"))
        except ValueError: # error handling for non numeral inputs and stuff
            return render_template('index.html', error="Error: Please enter valid numbers!", order=selected_order)

        plt.clf()
        t = np.linspace(0, time_limit, 1000) # create 1000 time points between user input and 0

        if selected_order == "zero":
            C = np.maximum(C0 - k * t, 0)  # Zero-order reaction solution
            # plotting
            plt.plot(t, C, label='[A] (Concentration)', color='b')
            plt.title('Zero-Order Reaction Kinetics')

        elif selected_order == "one":
            # First-order reaction equation
            def first_order_reaction(t, C):
                return -k * C 
            # plotting
            solution = solve_ivp(first_order_reaction, (0, time_limit), [C0], t_eval=t, method='RK45')
            plt.plot(solution.t, solution.y[0], label='[A] (Concentration)', color='b')
            plt.title('First-Order Reaction Kinetics')

        elif selected_order == "two":
            # Second-order reaction equation
            def second_order_reaction(t, C):
                return -k * C**2
            # plotting
            solution = solve_ivp(second_order_reaction, (0, time_limit), [C0], t_eval=t, method='RK45')
            plt.plot(solution.t, solution.y[0], label='[A] (Concentration)', color='b')
            plt.title('Second-Order Reaction Kinetics')

        else:
            return render_template('index.html', error="Error: Invalid reaction order!", order=selected_order) # error handling

        # other plot settings
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (mol/L)')
        plt.legend()
        plt.grid()
        plt.savefig('static/images/figure.png')

        # return page to flask app, send back some numbers for use in form values
        return render_template('index.html', order=selected_order, rate=k, concentration=C0, time=time_limit)

    return render_template('index.html')

# was true during making, just left it here
if __name__ == "__main__":
    app.run(debug=False)
