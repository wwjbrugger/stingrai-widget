import matplotlib.pyplot as plt
import logging
from matplotlib.widgets import Slider, CheckButtons, RadioButtons, TextBox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Widget:
    def __init__(self,
                 arguments,
                 structure_widget,
                 bar_plot_obj_StInGRAI,
                 feature_histogram_obj_StInGRAI,
                 bar_plot_obj_unsegmented,
                 feature_histogram_obj_unsegmented):
        self.structure_widget = structure_widget

        self.bar_plot_obj_StInGRAI = bar_plot_obj_StInGRAI
        self.feature_histogram_obj_StInGRAI = feature_histogram_obj_StInGRAI
        self.bar_plot_obj_unsegmented = bar_plot_obj_unsegmented
        self.feature_histogram_obj_unsegmented = feature_histogram_obj_unsegmented

        self.bar_plot_obj = bar_plot_obj_StInGRAI
        self.feature_histogram_obj = feature_histogram_obj_StInGRAI

        self.fig = plt.figure(figsize=(15, 8))

        # add fields in plot
        axcolor = 'lightgoldenrodyellow'
        self.ax_bar = self.fig.add_axes(self.structure_widget['bar_chart']['pos_args'])

        self.ax_hist = self.add_axes_for_hist()

        self.add_slider_when_to_change_transition(axcolor)

        self.add_slider_to_controll_borders_for_StInGRAI(axcolor)

        self.add_button_which_transition_to_show()

        self.add_button_show_std()

        self.add_buttons_use_StInGRAI_or_unsegmented()

        # add text fields with tk_kinter. The text option of plt is slowly.
        tk_root = self.bind_tk_kinter_to_plt()

        self.add_field_for_file_name_unsegmented(tk_root)

        self.add_field_to_select_which_features_to_show(tk_root)

        # update bar plot after selecting which features should be shown in bar plot
        self.update_bar_plot()
        self.add_button_which_feature_to_show_in_histogram()
        self.update_feature_in_histogram(feature_expression=self.feature_button.value_selected)

        self.fig.canvas.draw_idle()
        # print('save figure')
        # self.fig.savefig(fname='/home/jbrugger/Desktop/delete_me/sceenshot_500.png', dpi=1000)
        tk_root.mainloop()



    def add_field_to_select_which_features_to_show(self, tk_root):
        label_feature_to_show = tk.Label(tk_root, **self.structure_widget['textbox_feature_to_show']['label'])
        label_feature_to_show.pack(**self.structure_widget['textbox_feature_to_show']['pos_args_label'])
        entry_label_features_to_show = tk.Entry(tk_root,
                                                **self.structure_widget['textbox_feature_to_show']['textfield'])
        entry_label_features_to_show.insert(0,
                                            self.structure_widget['textbox_feature_to_show']['initial_str_textfield'])
        entry_label_features_to_show.pack(**self.structure_widget['textbox_feature_to_show']['pos_args_textfield'])
        entry_label_features_to_show.bind("<Return>", self.update_textbox_features_to_show)

    def add_field_for_file_name_unsegmented(self, tk_root):
        self.add_textfield_for_path_unsegmented(tk_root)

    def add_slider_when_to_change_transition(self, axcolor):
        ax_when_to_change_transition = plt.axes(self.structure_widget['slider_when_to_change_transition']['pos_args'],
                                                facecolor=axcolor)
        self.slider_when_to_change_transition = Slider(ax_when_to_change_transition,
                                                       **self.structure_widget['slider_when_to_change_transition'][
                                                           'args'])
        self.slider_when_to_change_transition.on_changed(self.update_slider)

    def add_slider_to_controll_borders_for_StInGRAI(self, axcolor):
        ax_baseline = plt.axes(self.structure_widget['slider_baseline']['pos_args'], facecolor=axcolor)
        self.slider_baseline = Slider(ax_baseline, **self.structure_widget['slider_baseline']['args'])
        self.slider_baseline.on_changed(self.update_slider)
        ax_data_to_explain = plt.axes(self.structure_widget['slider_data_to_explain']['pos_args'], facecolor=axcolor)
        self.slider_data_to_explain = Slider(ax_data_to_explain, slidermin=self.slider_baseline,
                                             **self.structure_widget['slider_data_to_explain']['args'])
        self.slider_data_to_explain.on_changed(self.update_slider)

    def add_button_which_transition_to_show(self):
        ax_check_transition = self.fig.add_axes(self.structure_widget['check_buttons_transition']['pos_args'])
        self.check_transition = CheckButtons(ax_check_transition,
                                             **self.structure_widget['check_buttons_transition']['args'])
        self.check_transition.on_clicked(self.update_transition_used)

    def add_button_show_std(self):
        ax_check_std = self.fig.add_axes(self.structure_widget['check_buttons_std']['pos_args'])
        self.check_std = CheckButtons(ax_check_std, **self.structure_widget['check_buttons_std']['args'])
        self.check_std.on_clicked(self.update_show_std)

    def add_button_which_feature_to_show_in_histogram(self):
        if self.bar_plot_obj.feature_in_barplot == []:
            self.update_bar_plot()
        self.ax_feature_button = plt.axes(self.structure_widget['feature_button']['pos_args'])
        index_to_active = self.select_index_to_show_in_histogram(self.structure_widget['feature_button']['initial'])
        feature_to_plot = self.bar_plot_obj.feature_in_barplot[index_to_active]
        self.feature_histogram_obj_StInGRAI.feature_to_plot = feature_to_plot
        self.feature_histogram_obj_unsegmented.feature_to_plot = feature_to_plot
        self.feature_button = RadioButtons(self.ax_feature_button,
                                           labels=self.bar_plot_obj.feature_in_barplot,
                                           active=index_to_active
                                           )

        self.feature_button.on_clicked(self.update_feature_in_histogram)

    def add_buttons_use_StInGRAI_or_unsegmented(self):
        ax_approach_to_use = plt.axes(self.structure_widget['button_approach_to_use']['pos_args'])
        self.approach_to_use = RadioButtons(ax_approach_to_use,
                                            labels=self.structure_widget['button_approach_to_use']['labels'],
                                            active=self.structure_widget['button_approach_to_use']['labels'].index(
                                                self.structure_widget['button_approach_to_use']['initial'])
                                            )
        self.approach_to_use.on_clicked(self.update_approach_to_use),
        self.update_approach_to_use(approach_to_use=self.structure_widget['button_approach_to_use']['initial'])

    def add_textfield_for_path_unsegmented(self, tk_root):
        label_ig_long = tk.Label(tk_root, **self.structure_widget['textbox_long_path_to_use']['label'])
        label_ig_long.pack(**self.structure_widget['textbox_long_path_to_use']['pos_args_label'])
        entry_ig_long = tk.Entry(tk_root, **self.structure_widget['textbox_long_path_to_use']['textfield'])
        entry_ig_long.insert(0, self.structure_widget['textbox_long_path_to_use']['initial_str_textfield'])
        entry_ig_long.pack(**self.structure_widget['textbox_long_path_to_use']['pos_args_textfield'])
        entry_ig_long.bind("<Return>", self.update_textbox_long_path_to_use)
        self.entry_ig_long = entry_ig_long

    def bind_tk_kinter_to_plt(self):
        root = tk.Tk()
        root.wm_title("stingrai-widget")
        canvas = FigureCanvasTkAgg(self.fig, root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return root

    def add_axes_for_hist(self):
        full_window_args = self.structure_widget['hist']['pos_args']
        single_window_args = full_window_args.copy()
        height_total = full_window_args[3] - self.structure_widget['hist']['distance_between_plots']
        height_sub = height_total / self.structure_widget['hist']['num_axes']
        free_space_between_sub = self.structure_widget['hist']['distance_between_plots'] / \
                                 self.structure_widget['hist']['num_axes']
        single_window_args[3] = height_sub
        ax_list = []
        for i in range(self.structure_widget['hist']['num_axes']):
            ax = self.fig.add_axes(single_window_args)
            ax_list.append(ax)
            single_window_args[1] += height_sub + free_space_between_sub
        return ax_list

    def update_slider(self, val):
        self.slider_data_to_explain.val = round(self.slider_data_to_explain.val, 3)
        self.bar_plot_obj_StInGRAI.stop_point = self.slider_data_to_explain.val
        self.feature_histogram_obj_StInGRAI.stop_point = self.slider_data_to_explain.val

        self.slider_baseline.val = round(self.slider_baseline.val, 3)
        self.bar_plot_obj_StInGRAI.start_point = self.slider_baseline.val
        self.feature_histogram_obj_StInGRAI.start_point = self.slider_baseline.val

        self.bar_plot_obj_StInGRAI.fraction_change_transition = self.slider_when_to_change_transition.val
        self.feature_histogram_obj_StInGRAI.fraction_change_transition = self.slider_when_to_change_transition.val
        if self.bar_plot_obj == self.bar_plot_obj_StInGRAI:
            self.update_bar_plot()
            self.redraw_histogram_feature_buttons()
            self.fig.canvas.draw_idle()

    def update_bar_plot(self):
        self.bar_plot_obj.calculate_explanations_of_transitions()
        self.bar_plot_obj.plot_cumulated_explanation(
            ax=self.ax_bar,
            bar_chart_parameter=self.structure_widget['bar_chart']
        )

    def update_transition_used(self, label):
        label_dic = {
            'pos -> pos': 'signal->signal',
            'neg -> pos': 'background->signal',
            'pos -> neg': 'signal->background',
            'neg -> neg': 'background->background'
        }
        transition_set = set(self.bar_plot_obj.transition_list)
        label_old = label_dic[label]
        if label_old in transition_set:
            transition_set.remove(label_old)
        else:
            transition_set.add(label_old)

        self.update_transition_list_in_both_approaches(transition_set)

        self.update_bar_plot()
        self.redraw_histogram_feature_buttons()
        self.fig.canvas.draw_idle()

    def update_transition_list_in_both_approaches(self, transition_set):
        self.bar_plot_obj_unsegmented.transition_list = list(transition_set)
        self.feature_histogram_obj_unsegmented.transition_list = list(transition_set)
        self.bar_plot_obj_StInGRAI.transition_list = list(transition_set)
        self.feature_histogram_obj_StInGRAI.transition_list = list(transition_set)

    def update_show_std(self, label):
        self.bar_plot_obj_unsegmented.show_std = not self.bar_plot_obj_unsegmented.show_std
        self.bar_plot_obj_StInGRAI.show_std = not self.bar_plot_obj_StInGRAI.show_std
        self.update_bar_plot()
        self.fig.canvas.draw_idle()

    def update_feature_in_histogram(self, feature_expression):
        self.feature_histogram_obj_StInGRAI.feature_to_plot = feature_expression
        self.feature_histogram_obj_unsegmented.feature_to_plot = feature_expression

        self.feature_histogram_obj.get_all_paths_of_one_feature()
        self.feature_histogram_obj.plot_histograms(
            ax_list=self.ax_hist
        )
        self.fig.canvas.draw_idle()

    def update_textbox_long_path_to_use(self, event):  # folder_name
        input = event.widget.get()
        all_folder_loaded = list(self.bar_plot_obj_unsegmented.ig_dics.keys())
        if input in all_folder_loaded:
            self.bar_plot_obj_unsegmented.key_of_ig_dic = input
            self.feature_histogram_obj_unsegmented.key_of_ig_dic = input
            self.update_bar_plot()
            self.redraw_histogram_feature_buttons()
            self.fig.canvas.draw_idle()
        else:
            logging.info(msg=f'{input} is not in the loaded files\n'
                             f'{self.bar_plot_obj_unsegmented.key_of_ig_dic} is preserved')
            self.entry_ig_long.insert(len(input), '!not_found!')

    def update_approach_to_use(self, approach_to_use):
        if approach_to_use == 'StInGRAI':
            self.bar_plot_obj = self.bar_plot_obj_StInGRAI
            self.feature_histogram_obj = self.feature_histogram_obj_StInGRAI
        elif approach_to_use == 'IG Unsegmented':
            self.bar_plot_obj = self.bar_plot_obj_unsegmented
            self.feature_histogram_obj = self.feature_histogram_obj_unsegmented
        else:
            raise ValueError(f"{approach_to_use} does not exist as approach")

        self.update_bar_plot()
        self.redraw_histogram_feature_buttons()
        self.fig.canvas.draw_idle()

    def update_textbox_features_to_show(self, event):
        input = event.widget.get()
        self.bar_plot_obj_unsegmented.feature_to_show = input
        self.bar_plot_obj_StInGRAI.feature_to_show = input
        self.update_bar_plot()
        self.redraw_histogram_feature_buttons()
        self.fig.canvas.draw_idle()

    def redraw_histogram_feature_buttons(self):
        try:
            self.ax_feature_button.clear()
            old_value_selected = self.feature_button.value_selected
            index_to_active = self.select_index_to_show_in_histogram(old_value_selected)
            self.feature_button = RadioButtons(self.ax_feature_button,
                                               labels=self.bar_plot_obj.feature_in_barplot,
                                               active=index_to_active
                                               )
            self.feature_button.on_clicked(self.update_feature_in_histogram)
            self.update_feature_in_histogram(feature_expression=self.feature_button.value_selected)
        except AttributeError as e :
            logging.error('Something went wrong with redrawing the buttons to select which feature should be drawn')
            logging.error('This does not have to be a probleme. Maybe this method was called to early.')
            logging.error(f'Here is the error: \n {e}')


    def select_index_to_show_in_histogram(self, old_value_selected):
        if type(old_value_selected) == int:
            index_to_active = old_value_selected
        elif old_value_selected in self.bar_plot_obj.feature_in_barplot:
            index_to_active = self.bar_plot_obj.feature_in_barplot.index(old_value_selected)
        else:
            index_to_active = 0
        return index_to_active
