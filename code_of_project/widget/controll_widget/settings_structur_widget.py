import tkinter as tk


def get_settings_structur_widget(arguments) -> dict:
    parameter_dic = {
        'bar_chart': {
            # The dimensions[left, bottom, width, height] of the new axes
            'pos_args': [0.04, 0.35, 0.58, 0.6],
            'args': {
                'numeric_value_in_plot': arguments.numeric_values_in_bar_plot,
                'ylabel': 'Integrated Gradient',
                'print_bar_values_in_terminal': False,
                'feature_to_print': ['P02656','P02655','P35542','Q6YHK3','O95497','P04278','P05109','Q15848','P69905','P18065','O95445','P06702','Q08380','Q06033;Q06033-2', 'P0CG47;P0CG48;P62979;P62987','P00918','P54108;P54108-2;P54108-3','P30043','P19823','P18428','P49908','P10643','P19827','P02649','Q16610','P08185','P02747','P09172','O43866','P25311','P29622','P13598','P15169','P02760','P00450','P43652','P01008','O00187','P06396','P02748','P04004','P05156','P22891;P22891-2','P13671', 'Q92954-3','Q96NZ9;Q96NZ9-2;Q96NZ9-3;Q96NZ9-4','P02741', 'P05062','P07477','P37840;P37840-2;P37840-3','P55103', 'Q13790', 'Q14624-2', 'P01011', 'P06276', 'P36955',  'A0A0B4J1V6', 'P05546', 'P06396-2', 'P02743', 'Q15166', 'A0A087WSY4', 'P34096', 'O95932;O95932-2', 'Q96CV9;Q96CV9-2;Q96CV9-3', 'A0A075B6K0', 'A0A075B6R2', 'O43790;P78385;P78386;Q14533', 'A0A075B6H9', 'A0A075B6K2', 'O75083;O75083-3', 'A0A0J9YVY3', 'A0A087WW87;P01614', 'O43707']
            },

        },
        'hist': {
            # The dimensions[left, bottom, width, height] of the new axes
            'pos_args': [0.65, 0.4, 0.25, 0.6],
            'num_axes': 4,
            'distance_between_plots': 0.1,
            'feature_to_plot': 'lep2_pt',
            'args': {
                'bins': arguments.bins_in_histograms,
                'density': arguments.density_histograms
            },
            'show_mean_in_histogram': False

        },
        'slider_when_to_change_transition':
            {
                'pos_args': [0.08, 0.095, 0.45, 0.03],
                'args': {
                    'label': 'When to \n change label',
                    'valmin': 0,
                    'valmax': 1,
                    'valinit': arguments.fraction_change_transition
                }
            },

        'slider_baseline':
            {
                'pos_args': [0.08, 0.055, 0.75, 0.03],
                'args': {
                    'label': 'Lower Bound',
                    'valmin': 0,
                    'valmax': 1,
                    'valinit': arguments.ig_dic_StInGRAI_start_point
                }
            },
        'slider_data_to_explain':
            {
                'pos_args': [0.08, 0.01, 0.75, 0.03],
                'args': {
                    'label': 'Upper Bound',
                    'valmin': 0,
                    'valmax': 1,
                    'valinit': arguments.ig_dic_StInGRAI_stop_point
                }
            },

        'check_buttons_transition': {
            # The dimensions[left, bottom, width, height] of the new axes
            'pos_args': [0.8, 0.1, 0.08, 0.16],
            'args': {
                'labels': (
                    'pos -> pos',
                    'pos -> neg',
                    'neg -> pos',
                    'neg -> neg',

                ),
                'actives': ('signal->signal' in arguments.transitions_to_calculate,
                            'signal->background' in arguments.transitions_to_calculate,
                            'background->signal' in arguments.transitions_to_calculate,
                            'background->background' in arguments.transitions_to_calculate)
            },
        },

        'check_buttons_std': {
            # The dimensions[left, bottom, width, height] of the new axes
            'pos_args': [0.58, 0.10, 0.07, 0.05],
            'args': {
                'labels': (
                    'show std',
                ),
                'actives': ([False])
            },
        },

        'feature_button': {
            'initial': [],
            'pos_args': [0.9, 0, 0.1, 1],
        },
        'textbox_long_path_to_use': {
            'label': {
                'text': 'Load data IG Unsegmented ',
                'width': 25
            },
            # The dimensions[left, bottom, width, height] of the new axes
            'pos_args_label': {
                'side': tk.LEFT,
                'padx': 0,
                'pady': 5
            },
            'textfield': {
                'width': 50
            },
            'initial_str_textfield': '0.0-0.1->0.9-1.0.pkl',
            'pos_args_textfield': {
                'side': tk.LEFT,
                'padx': 5,
                'pady': 5
            }
        },

        'textbox_feature_to_show': {
            'label': {
                'text': 'Feature to show',
                'width': 15
            },

            'pos_args_label': {
                'side': tk.LEFT,
                'padx': 0,
                'pady': 5
            },
            'textfield': {
                'width': 50
            },
            'initial_str_textfield': arguments.how_many_feature_to_show,
            'pos_args_textfield': {
                'side': tk.LEFT,
                'padx': 5,
                'pady': 5
            }
        },

        'button_approach_to_use': {
            # The dimensions[left, bottom, width, height] of the new axes
            'initial': 'IG',
            'pos_args': [0.67, 0.10, 0.11, 0.11],
            'labels': ['$IG_{Seg}$', 'IG']
        },

    }
    return parameter_dic
