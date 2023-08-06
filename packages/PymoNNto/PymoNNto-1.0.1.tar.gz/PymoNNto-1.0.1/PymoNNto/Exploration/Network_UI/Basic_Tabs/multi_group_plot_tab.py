from PymoNNto.Exploration.Network_UI.TabBase import *

class multi_group_plot_tab(TabBase):

    def __init__(self, variables, title='Multi Group', timesteps=500):
        super().__init__(title)
        self.timesteps = timesteps

        self.original_variables=variables
        self.variables = [] #{var1:0, var2:0, var3:1, variable:group}
        self.curve_numbers = []
        self.plot_variables = []
        for i, var in enumerate(self.original_variables):#grouped togerther with var1|var2
            splitted=var.split('|')
            for v in splitted:
                self.variables.append(v)
            self.curve_numbers.append(len(splitted))
            self.plot_variables.append(splitted)

    def add_recorder_variables(self, neuron_group, Network_UI):
        for var in self.variables:
            Network_UI.add_recording_variable(neuron_group, 'n.'+var, timesteps=self.timesteps)
            Network_UI.add_recording_variable(neuron_group, 'np.mean(n.'+var+')', timesteps=self.timesteps)


    def initialize(self, Network_UI):
        self.main_tab = Network_UI.Next_Tab(self.title)

        self.net_var_curves = [{} for _ in range(len(Network_UI.neuron_visible_groups))]
        for plot_indx, curves_per_plot in enumerate(self.curve_numbers):

            stretch=1
            if plot_indx==0:
                stretch=2

            curves = Network_UI.Add_plot_curve(stretch=stretch, number_of_curves=len(Network_UI.neuron_visible_groups)*curves_per_plot, return_list=True, x_label='t (iterations)', y_label='Network average ' + self.original_variables[plot_indx]) #, lines=lines

            for gi in range(len(Network_UI.neuron_visible_groups)):
                for ci,var in enumerate(self.plot_variables[plot_indx]):
                    self.net_var_curves[gi][var] = curves[curves_per_plot*gi+ci]

        Network_UI.Next_H_Block()

        self.neuron_var_curves = {}
        for plot_indx, curves_per_plot in enumerate(self.curve_numbers):

            stretch = 1
            if plot_indx == 0:
                stretch = 2

            curves = Network_UI.Add_plot_curve(stretch=stretch, number_of_curves=1+curves_per_plot, colors=[Network_UI.neuron_select_color], legend=False, x_label='t (iterations)', y_label='Neuron ' + self.original_variables[plot_indx])

            for ci, var in enumerate(self.plot_variables[plot_indx]):
                self.neuron_var_curves[var] = curves[ci]

        if Network_UI.group_display_count > 1:
            Network_UI.Next_H_Block()

            self.group_sliders = []
            for group_index in range(Network_UI.group_display_count):
                self.group_sliders.append(QSlider(1))  # QtCore.Horizontal
                self.group_sliders[-1].setMinimum(0)
                self.group_sliders[-1].setMaximum(100)
                self.group_sliders[-1].setSliderPosition(100)
                self.group_sliders[-1].mouseReleaseEvent = Network_UI.static_update_func
                self.group_sliders[-1].setToolTip('scale neuron-group plots up and down (only visualization)')

                Network_UI.Add_element(self.group_sliders[-1])


    def update(self, Network_UI):
        if self.main_tab.isVisible():

            lg=len(Network_UI.neuron_visible_groups)

            for i, group_tag in enumerate(Network_UI.neuron_visible_groups):
                if len(Network_UI.network[group_tag]) > 0:
                    group=Network_UI.network[group_tag, 0]
                    if hasattr(self, 'group_sliders'):
                        squeeze= self.group_sliders[i].sliderPosition() / 100
                    else:
                        squeeze = 1

                    for var in self.variables:

                        try:
                            net_data = group['np.mean(n.'+var+')', 0, 'np'][-self.timesteps:]
                            iterations = group['n.iteration', 0, 'np'][-self.timesteps:]
                            self.net_var_curves[i][var].setData(iterations, net_data * squeeze, pen=group.color)
                        except:#else:
                            self.net_var_curves[i][var].clear()

                        #maybe better to generalize and do everything with recorders a|b => a and b are plotted in same graph and can eighter be a vector variable, a scalar variable or a number



            group = Network_UI.network[Network_UI.neuron_select_group, 0]

            for var in self.variables:
                try:#if hasattr(group, var):
                    neuron_data = group['n.' + var, 0, 'np'][-self.timesteps:].astype(def_dtype)
                    iterations = group['n.iteration', 0, 'np'][-self.timesteps:]
                    if len(neuron_data.shape) > 1:
                        neuron_data = neuron_data[:, Network_UI.neuron_select_id]
                    self.neuron_var_curves[var].setData(iterations, neuron_data)
                except:  #else:
                    self.neuron_var_curves[var].clear()

