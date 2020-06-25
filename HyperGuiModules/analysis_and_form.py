from HyperGuiModules.utility import *
from tkinter import messagebox
import os, sys, subprocess


class AnalysisAndForm:
    def __init__(self, analysis_and_form_frame, listener):
        self.root = analysis_and_form_frame

        # Listener
        self.listener = listener

        self.upper_wavelength_text = None
        self.lower_wavelength_text = None
        self.wavelength_entry = None
        self.wavelength_value = None
        self.wavelength_upper_text = None
        self.wavelength_upper_entry = None
        self.wavelength_upper_value = None
        self.wavelength_lower_text = None
        self.wavelength_lower_entry = None
        self.wavelength_lower_value = None

        self.idx_title = None
        self.idx1_button = None
        self.idx2_button = None
        self.idx3_button = None
        self.idx4_button = None
        self.idx5_button = None
        self.idx6_button = None
        self.idx7_button = None
        self.idx8_button = None

        self.info_label = None

        # State vars
        self.normal = True  # True by default
        self.absorbance = True

        self._init_widget()

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_wavelength(self):
        lower = self.wavelength_lower_entry.get()
        upper = self.wavelength_upper_entry.get()
        return int((float(lower) - 500) / 5), int((float(upper) - 500) / 5)

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_idx_title()
        self._build_buffer()
        self._build_idxs()
        self._build_edit_idxs()
        self._build_wavelength_title()
        self._build_wavelength_text()
        self._build_wavelength_upper_entry()
        self._build_wavelength_lower_entry()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Analysis Settings\nfor "New Image"', command=self.__info,
                                            width=14)
        self.info_label.grid(columnspan=4)

    def _build_wavelength_title(self):
        self.idx_title = make_text(self.root, content="Wavelength:", bg=tkcolour_from_rgb(BACKGROUND), column=0,
                                   row=1, width=11, columnspan=8, pady=(0, 10))

    def _build_wavelength_text(self):
        self.lower_wavelength_text = make_text(self.root, content="Lower Wavelength: ",
                                               bg=tkcolour_from_rgb(BACKGROUND), column=0, row=3, width=19,
                                               columnspan=4, pady=0)
        self.upper_wavelength_text = make_text(self.root, content="Upper Wavelength: ",
                                               bg=tkcolour_from_rgb(BACKGROUND), column=0, row=4, width=19,
                                               columnspan=4, pady=(5, 0))

    def _build_wavelength_lower_entry(self):
        self.wavelength_lower_entry = make_entry(self.root, row=3, column=4, width=15, pady=0, columnspan=4)
        self.wavelength_lower_entry.insert(0, str(500))
        self.wavelength_lower_entry.bind('<Return>', self.__update_wavelength)

    def _build_wavelength_upper_entry(self):
        self.wavelength_upper_entry = make_entry(self.root, row=4, column=4, width=15, pady=(5, 0), columnspan=4)
        self.wavelength_upper_entry.insert(0, str(500))
        self.wavelength_upper_entry.bind('<Return>', self.__update_wavelength)

    def _build_idx_title(self):
        self.idx_title = make_text(self.root, content="Individual Index:", bg=tkcolour_from_rgb(BACKGROUND), column=0,
                                   row=5, width=17, columnspan=8, pady=(10, 5))

    def _build_buffer(self):
        self.buffer = make_text(self.root, content=" ", bg=tkcolour_from_rgb(BACKGROUND), column=0,
                                row=10, width=17, columnspan=8, pady=(0, 5))

    def _build_idxs(self):
        self.idx1_button = make_button(self.root, text='1', command=lambda: self.__idxn(1), row=6, column=0,
                                       outer_pady=(5, 0), outer_padx=(15, 5), width=1)
        self.idx2_button = make_button(self.root, text='2', command=lambda: self.__idxn(2), row=6, column=1,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx3_button = make_button(self.root, text='3', command=lambda: self.__idxn(3), row=6, column=2,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx4_button = make_button(self.root, text='4', command=lambda: self.__idxn(4), row=6, column=3,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx5_button = make_button(self.root, text='5', command=lambda: self.__idxn(5), row=6, column=4,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx6_button = make_button(self.root, text='6', command=lambda: self.__idxn(6), row=6, column=5,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx7_button = make_button(self.root, text='7', command=lambda: self.__idxn(7), row=6, column=6,
                                       outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx8_button = make_button(self.root, text='8', command=lambda: self.__idxn(8), row=6, column=7,
                                       outer_pady=(5, 0), outer_padx=(5, 15), width=1)

        self.idx9_button = make_button(self.root, text='9', command=lambda: self.__idxn(9), row=8, column=0,
                                       outer_pady=(5, 0), outer_padx=(15, 5), width=1)
        self.idx10_button = make_button(self.root, text='10', command=lambda: self.__idxn(10), row=8, column=1,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx11_button = make_button(self.root, text='11', command=lambda: self.__idxn(11), row=8, column=2,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx12_button = make_button(self.root, text='12', command=lambda: self.__idxn(12), row=8, column=3,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx13_button = make_button(self.root, text='13', command=lambda: self.__idxn(13), row=8, column=4,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx14_button = make_button(self.root, text='14', command=lambda: self.__idxn(14), row=8, column=5,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx15_button = make_button(self.root, text='15', command=lambda: self.__idxn(15), row=8, column=6,
                                        outer_pady=(5, 0), outer_padx=5, width=1)
        self.idx16_button = make_button(self.root, text='16', command=lambda: self.__idxn(16), row=8, column=7,
                                        outer_pady=(5, 0), outer_padx=(5, 15), width=1)
        self.idx1_button.config(foreground="red")
        self.index_selected = 1  # Use index no.1 by default

    def _build_edit_idxs(self):
        make_button(self.root, text='edit', command=lambda: self.__open_index(1), row=7, column=0,
                    outer_pady=(5, 5), outer_padx=(12, 0), width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(2), row=7, column=1,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(3), row=7, column=2,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(4), row=7, column=3,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(5), row=7, column=4,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(6), row=7, column=5,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(7), row=7, column=6,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(8), row=7, column=7,
                    outer_pady=(5, 5), outer_padx=(0, 12), width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(9), row=9, column=0,
                    outer_pady=(5, 5), outer_padx=(12, 0), width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(10), row=9, column=1,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(11), row=9, column=2,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(12), row=9, column=3,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(13), row=9, column=4,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(14), row=9, column=5,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(15), row=9, column=6,
                    outer_pady=(5, 5), outer_padx=0, width=3, inner_padx=0, inner_pady=1)
        make_button(self.root, text='edit', command=lambda: self.__open_index(16), row=9, column=7,
                    outer_pady=(5, 5), outer_padx=(0, 12), width=3, inner_padx=0, inner_pady=1)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].analysis_form_info
        title = "Analysis Settings Information"
        make_info(title=title, info=info)

    def __idxn(self, n):
        self.listener.submit_index(n)
        buttons = [self.idx1_button, self.idx2_button, self.idx3_button, self.idx4_button,
                   self.idx5_button, self.idx6_button, self.idx7_button, self.idx8_button,
                   self.idx9_button, self.idx10_button, self.idx11_button, self.idx12_button,
                   self.idx13_button, self.idx14_button, self.idx15_button, self.idx16_button]
        for i in range(len(buttons)):
            if i + 1 == n:
                buttons[i].config(foreground="red")
            else:
                buttons[i].config(foreground="black")

    def __update_wavelength(self, event):
        lower = float(self.wavelength_lower_entry.get())
        upper = float(self.wavelength_upper_entry.get())
        if lower < 500 or lower > 995 or lower % 5 != 0:
            messagebox.showerror("Error", "Wavelength values must be on interval [500, 995] in 5nm steps.")
        elif upper < 500 or upper > 995 or upper % 5 != 0:
            messagebox.showerror("Error", "Wavelength values must be on interval [500, 995] in 5nm steps.")
        (wav1, wav2) = self.get_wavelength()
        wavelength = tuple((wav1, wav2))
        self.listener.submit_wavelength(wavelength)

    @staticmethod
    def __open_index(num):
        filename = './AnalysisModules/Indices/index_' + str(num) + '.py'
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
