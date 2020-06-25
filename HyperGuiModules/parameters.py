from HyperGuiModules.utility import *


class Parameter:
    def __init__(self, parameter_frame, listener):
        self.root = parameter_frame

        # Listener
        self.listener = listener

        self.r1_text = None
        self.r2_text = None
        self.s1_text = None
        self.s2_text = None
        self.t1_text = None
        self.t2_text = None
        self.u1_text = None
        self.u2_text = None

        self.r1_entry = None
        self.r2_entry = None
        self.s1_entry = None
        self.s2_entry = None
        self.t1_entry = None
        self.t2_entry = None
        self.u1_entry = None
        self.u2_entry = None

        self.r1_value = None
        self.r2_value = None
        self.s1_value = None
        self.s2_value = None
        self.t1_value = None
        self.t2_value = None
        self.u1_value = None
        self.u2_value = None

        self.info_label = None

        self._init_widget()

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_params(self):
        """
        Returns a list of parameters for the recreated image calculations in
        float form: [r1, r2, s1, s2, t1, t2, u1, u2]
        """
        return [self.r1_value, self.r2_value, self.s1_value, self.s2_value, self.t1_value, self.t2_value, self.u1_value,
                self.u2_value]

    # ----------------------------------------------- INITIALIZATION -------------------------------------------------

    def _init_widget(self):
        """
        Initialises the parameter widget by running _build_params() and _build_info_label
        """
        self._build_params()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_info_label(self):
        """
        Builds the information label/button for the widget, placing it in the top left of the widget frame and binding
        it to the __info function.
        """
        self.info_label = make_label_button(self.root, text='Parameter\nSpecification for\n"Recreated Image"',
                                            command=self.__info, width=14)
        self.info_label.grid(columnspan=2, padx=(0, 20))

    def _build_params(self):
        """
        Builds the title and Entry widget for each parameter r1, r2, s1, s2, t1, t2, u1, and u2. For each, a text box
        containing the parameter name is created, followed by an Entry widget to the right of the name. An initial value
        is inserted into the Entry widget and the <Return> event is bound to the __update function.
        """
        # r1
        self.r1_text = make_text(self.root, content='r' + u'\u2081' + ' (StO2): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=1, width=11, padx=(15, 5), pady=(0, 3))
        self.r1_entry = make_entry(self.root, row=1, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.r1_entry.insert(0, str(0.2))
        self.r1_entry.bind('<Return>', self.__update)
        # r2
        self.r2_text = make_text(self.root, content='r' + u'\u2082' + ' (StO2): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=2, width=11, padx=(15, 5), pady=(0, 3))
        self.r2_entry = make_entry(self.root, row=2, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.r2_entry.insert(0, str(-0.03))
        self.r2_entry.bind('<Return>', self.__update)
        # s1
        self.s1_text = make_text(self.root, content='s' + u'\u2081' + ' (NIR): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=3, width=11, padx=(15, 5), pady=(0, 3))
        self.s1_entry = make_entry(self.root, row=3, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.s1_entry.insert(0, str(-0.46))
        self.s1_entry.bind('<Return>', self.__update)
        # s2
        self.s2_text = make_text(self.root, content='s' + u'\u2082' + ' (NIR): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=4, width=11, padx=(15, 5), pady=(0, 3))
        self.s2_entry = make_entry(self.root, row=4, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.s2_entry.insert(0, str(0.45))
        self.s2_entry.bind('<Return>', self.__update)
        # t1
        self.t1_text = make_text(self.root, content='t' + u'\u2081' + ' (THI): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=5, width=11, padx=(15, 5), pady=(0, 3))
        self.t1_entry = make_entry(self.root, row=5, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.t1_entry.insert(0, str(0.4))
        self.t1_entry.bind('<Return>', self.__update)
        # t2
        self.t2_text = make_text(self.root, content='t' + u'\u2082' + ' (THI): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=6, width=11, padx=(15, 5), pady=(0, 3))
        self.t2_entry = make_entry(self.root, row=6, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.t2_entry.insert(0, str(1.55))
        self.t2_entry.bind('<Return>', self.__update)
        # u1
        self.u1_text = make_text(self.root, content='u' + u'\u2081' + ' (TWI): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=7, width=11, padx=(15, 5), pady=(0, 3))
        self.u1_entry = make_entry(self.root, row=7, column=1, width=8, padx=(0, 15), pady=(0, 3))
        self.u1_entry.insert(0, str(0.1))
        self.u1_entry.bind('<Return>', self.__update)
        # u2
        self.u2_text = make_text(self.root, content='u' + u'\u2082' + ' (TWI): ', bg=tkcolour_from_rgb(BACKGROUND),
                                 column=0, row=8, width=11, padx=(15, 5), pady=(0, 15))
        self.u2_entry = make_entry(self.root, row=8, column=1, width=8, padx=(0, 15), pady=(0, 15))
        self.u2_entry.insert(0, str(-0.5))
        self.u2_entry.bind('<Return>', self.__update)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        """
        Gets the widget information stored in the Info module through listener and creates a pop-up window containing
        'info' and titled 'title'
        """
        info = self.listener.modules[INFO].parameter_info
        title = "Parameter Specification Information"
        make_info(title=title, info=info)

    def __update(self, event):
        """
        Reads the parameters r1, r2, s1, s2, t1, t2, u1, u2 as floats and passes them to the listener to update the
        analyses based on the updated parameters.
        """
        self.r1_value = float(self.r1_entry.get())
        self.r2_value = float(self.r2_entry.get())
        self.s1_value = float(self.s1_entry.get())
        self.s2_value = float(self.s2_entry.get())
        self.t1_value = float(self.t1_entry.get())
        self.t2_value = float(self.t2_entry.get())
        self.u1_value = float(self.u1_entry.get())
        self.u2_value = float(self.u2_entry.get())
        self.listener.submit_params()
