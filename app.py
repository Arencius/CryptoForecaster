import tkinter as tk
from tkinter.font import Font
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from forecaster import CryptoForecaster
from api.currencies import currency_rate
from datetime import datetime


class App:
    def __init__(self):
        global c
        c = CryptoForecaster()

        self.btc = c.bitcoin_data()
        self.eth = c.ethereum_data()
        self.dash = c.dash_data()

        self.main()

    def main(self):
        ''' Main function. Builds window and initializes all values '''
        global window, canvas
        window = tk.Tk()
        window.title('CryptoForecaster')
        window.geometry('{0}x{1}+0+0'.format(window.winfo_screenwidth(),
                                             window.winfo_screenheight()))  # full-screen window size
        try:
            window.iconbitmap('images/btc.ico')
        except:
            print("Couldn't load an icon")

        # frame for cryptocurrencies buttons
        left_frame = tk.Frame(window, width=100)
        left_frame.pack(side=tk.LEFT)

        # frame for currencies buttons
        right_frame = tk.Frame(window, width=100)
        right_frame.pack(side=tk.RIGHT)

        # canvas
        global figure
        figure = Figure(figsize=(12, 10), facecolor='#eee')

        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.get_tk_widget().pack(side=tk.TOP)

        MODES = [
            ('BITCOIN', 'btc'),
            ('ETHEREUM', 'eth'),
            ('DASH', 'dash'),
            ('USD', 'usd'),
            ('EUR', 'eur'),
            ('PLN', 'pln'),
            ('GBP', 'gbp')
        ]

        global v_cr, v_cu
        v_cr, v_cu = tk.StringVar(), tk.StringVar()
        v_cr.set('btc')  # initialize cryptocurrency choice
        v_cu.set('usd')  # initalize standard currency choice

        row_index = 0
        for text, mode in MODES:
            if row_index < 3:
                radio_button = tk.Radiobutton(left_frame, text=text, value=mode, variable=v_cr,
                                              font=Font(size=11), command=lambda x=mode, y=v_cu.get(): self.display_plot(x, y))
                radio_button.grid(row=row_index, column=0,
                                  padx=(10, 0), pady=5)
            else:
                radio_button = tk.Radiobutton(
                    right_frame, text=text, value=mode, variable=v_cu, font=Font(
                        size=11),
                    command=lambda x=v_cr.get(), y=mode: self.display_plot(x, y))
                radio_button.grid(row=row_index, column=0,
                                  padx=(0, 20), pady=5)
            row_index += 1

        # initialize plot with default values
        self.display_plot('btc', 'usd')

        window.mainloop()

    def display_plot(self, key, cur):
        ''' Computes all necessary values, updates and displays the finished chart.'''
        figure.clear()   # updates canvas
        data, forecasted, title = np.array([]), [], ''

        # variable holding rate of given currency in relation to one dollar
        rate = currency_rate(cur.upper())

        if key == 'btc':
            data = np.array(self.btc) * rate
            forecasted = c.predict(self.btc) * rate
            title = 'BITCOIN'

        elif key == 'eth':
            data = np.array(self.eth) * rate
            forecasted = c.predict(self.eth) * rate
            title = 'ETHEREUM'

        else:
            data = np.array(self.dash) * rate
            forecasted = c.predict(self.dash) * rate
            title = 'DASH'

        # how many data points shall be displayed
        days = np.arange(len(data))

        # creating a plot
        ax = figure.add_subplot(1, 1, 1)
        ax.grid()
        ax.set_ylabel(f'Price in {v_cu.get().upper()}')
        figure.suptitle(title)

        # Setting names of months as a X axis labels
        ax.set_xticks(np.arange(0, 455, 30), minor=False)
        ax.set_xticklabels(c.months_names(), rotation=35)

        ax.scatter(days, data, color='red', s=10)
        ax.plot(days, data)

        self.append_plot(ax, forecasted)  # adds plot with forecasted values

        canvas.draw()

    def append_plot(self, fig, values):
        ''' Appends plot with forecasted values to existing chart. '''
        ci = 1.96 * np.std(values)/np.mean(values)  # 95% confidence interval
        fig.plot(np.arange(365, 455), values)
        fig.fill_between(np.arange(365, 455), (values-(values*ci)),
                         (values+(values*ci)), color='b', alpha=.1)


if __name__ == '__main__':
    App()
