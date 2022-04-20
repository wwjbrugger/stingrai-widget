import numpy as np



class IGPlotsController():
    def __init__(self):
        self.color_numeric_values = ['grey', 'black']
        self.color = {
            'pos -> pos': 'b',
            'neg -> pos': 'tab:orange',
            'pos -> neg': 'g',
            'neg -> neg': 'tab:red'
        }

    def add_multiple_bar_plots(self, ax, parameter, y_values_list, std_y_values, title_bar_plot):
        ax.clear()
        self.ax = ax
        self.offset = -0.4
        self.x_pos = np.arange(len(parameter['xtick_label']))

        bar_instance = []
        for set_nr, _ in enumerate(y_values_list):
            self.width_bar = 0.8 / len(y_values_list)
            temp = ax.bar(x=self.x_pos + self.offset,
                          height=y_values_list[set_nr],
                          align='edge',
                          width=self.width_bar,
                          color = self.color[parameter['legend'][set_nr]],
                          ecolor='grey',
                          yerr=std_y_values[set_nr])
            bar_instance.append(temp[0])
            if parameter['print_bar_values_in_terminal']:
                self.print_results(x_label = parameter['xtick_label'],
                                   values = y_values_list[set_nr],
                                   transition=parameter['legend'][set_nr],
                                   feature_to_print = parameter['feature_to_print'])

            if parameter['numeric_value_in_plot']:
                self._add_numeric_value_in_plot(
                    values=y_values_list[set_nr],
                    std_y_values=std_y_values[set_nr])

            self.offset += self.width_bar
        self._set_label_to_histograms(bar_instance=bar_instance,
                                      legend=parameter['legend'],
                                      xtick_label=parameter['xtick_label'],
                                      y_label=parameter['ylabel'])
        self.ax.set_title(title_bar_plot)
        
    def print_results(self, x_label, values, transition, feature_to_print):
        print(f'---------- {transition}-----------------------')
        for feature in feature_to_print:
            try:
                index_element = x_label.index(feature)
                print(f"{feature} : {str(round(values[index_element],2)).replace('.',',')}")
            except ValueError:
                print(f'{feature}')
        print(f"Features not in feature_to_print list: {list(set(x_label) - set(feature_to_print))}")


    def _set_label_to_histograms(self, bar_instance, legend, xtick_label, y_label):
        ax = self.ax
        ax.legend(tuple(bar_instance), tuple(legend))
        ax.set_xticks(self.x_pos)
        ax.set_xticklabels(xtick_label, verticalalignment='top', horizontalalignment='right', rotation=50)
        ax.set_ylabel(y_label)
        ax.grid()


    def _add_numeric_value_in_plot(self, values, std_y_values):
        values = values
        std_values = std_y_values
        for j, _ in enumerate(values):
            y_pos = values[j]
            if y_pos > 0:
                y_pos += 0.03 + std_values[j]
            else:
                y_pos -= 0.03 + std_values[j]
            self.ax.text(self.x_pos[j] + self.offset, y_pos, str(np.round(values[j], 4)), color=self.color_numeric_values[j % 2],
                         rotation=90,
                         horizontalalignment='center', verticalalignment='center')
