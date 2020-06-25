from HyperGuiModules.utility import *


class RecreatedColourData:
    def __init__(self, recreated_color_data_frame, listener):
        self.root = recreated_color_data_frame

        # Listener
        self.listener = listener

        self.data = None
        self.stats_data = None

        self.calc_button = None

        self.mean_text = None
        self.mean_value = ''
        self.sd_text = None
        self.sd_value = ''
        self.median_text = None
        self.median_value = ''
        self.iqr_text = None
        self.iqr_value = ''
        self.min_text = None
        self.min_value = ''
        self.max_text = None
        self.max_value = ''

        self.info_label = None

        self._init_widget()

    # ----------------------------------------------- INITIALIZATION -------------------------------------------------

    def update_calc(self):
        data = self.listener.get_current_rec_data().flatten()
        self.stats_data = [i for i in data if i != '--']
        self._calc_data()
        self._build_data()

    def _init_widget(self):
        self._build_data()
        self._build_calc_button()
        self._build_info_label()

    def empty_stats(self):
        self.mean_value = ''
        self.sd_value = ''
        self.median_value = ''
        self.iqr_value = ''
        self.min_value = ''
        self.max_value = ''
        self._build_data()

    # ------------------------------------------------- CALCULATOR ---------------------------------------------------

    def _calc_data(self):
        self.mean_value = np.round(np.ma.mean(self.stats_data), 4)
        self.sd_value = np.round(np.ma.std(self.stats_data), 4)
        self.median_value = np.round(np.ma.median(self.stats_data), 4)
        self.iqr_value = (np.round(np.quantile(self.stats_data, 0.25), 4), round(np.quantile(self.stats_data, 0.75), 4))
        self.min_value = np.round(np.ma.min(self.stats_data), 4)
        self.max_value = np.round(np.ma.max(self.stats_data), 4)

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Recreated Data', command=self.__info, width=12)

    def _build_data(self):
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=0, row=1, width=25, columnspan=2,
                                   padx=(3, 15), state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=2, width=25, columnspan=2, padx=(3, 15), state=NORMAL)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value),
                                     bg=tkcolour_from_rgb(BACKGROUND), column=0, row=3, width=25, columnspan=2,
                                     padx=(3, 15), state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(BACKGROUND),
                                  column=0, row=4, width=25, columnspan=2, padx=(3, 15), state=NORMAL)
        # min
        self.min_text = make_text(self.root, content="Min = " + str(self.min_value), bg=tkcolour_from_rgb(BACKGROUND),
                                  column=0, row=5, width=25, columnspan=2, padx=(3, 15), state=NORMAL)
        # max
        self.max_text = make_text(self.root, content="Max = " + str(self.max_value), bg=tkcolour_from_rgb(BACKGROUND),
                                  column=0, row=6, width=25, columnspan=2, padx=(3, 15), pady=(0, 15), state=NORMAL)

    def _build_calc_button(self):
        self.calc_button = make_button(self.root, text="CALC", row=0, column=1, columnspan=1, command=self.update_calc,
                                       inner_padx=3, inner_pady=0, outer_padx=(10, 15), outer_pady=15, width=5)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].recreated_data_info
        title = "Recreated Data Information"
        make_info(title=title, info=info)
