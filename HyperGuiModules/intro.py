from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from tkinter import *
import webbrowser


class Introduction:
    def __init__(self, introduction_frame):
        self.root = introduction_frame

        self.number = 1
        self.prev_button = None
        self.next_button = None

        self.title_1 = "Introduction to Hyperspectral Imaging"
        self.title_2 = "The Hyperspectral Camera System"
        self.title_3a = "TIVITA® Tissue Camera Operation"
        self.title_3b = "Data Requirements"
        self.title_4 = "TIVITA® Tissue System Image Calculation"
        self.title_5 = "Purpose of this Software"
        self.title_6 = "HyperGUI© (Hyperspectral Graphical User Interface) Disclaimer"

        self.urls = ['http://diaspective-vision.com', 'https://github.com/icamplis/HyperGui']

        self.text_text_1a = "\n\nHyperGUI© is a freeware Python tool for the extensive analysis and evaluation of " \
                            "hyperspectral data cubes from the TIVITA® Suite software version 1.4.1.5 from the TIVITA® " \
                            "Tissue Hyperspectral Camera from Diaspective Vision GmbH in Germany."
        self.text_text_1b = "\n\nwebsite:   "
        self.text_text_1c = "diaspective-vision.com"
        self.text_text_1d = "\nemail:     office@diaspective-vision.com "
        self.text_text_1e = "\n\nSpectral imaging is a method that has already been extensively used in other " \
                            "industries such as the food industry, geology, oil & gas industry and agriculture; " \
                            "however, it is relatively new to the field of medicine. It is based on the physical " \
                            "principle that different molecules have different characteristic absorbance and " \
                            "reflectance properties much like a spectral “fingerprint” (Figure 1)." \
                            "\n\nWhen measuring the absorbance or reflectance values of only a few specific wavelengths" \
                            " of the electromagnetic spectrum of every pixel within a two dimensional image this is " \
                            "called multispectral imaging. When measuring these values of several specific wavelengths " \
                            "or even continuously over the electromagnetic spectrum this is called hyperspectral " \
                            "imaging." \
                            "\n\nConsequently, when recording an image with a hyperspectral camera, the data received " \
                            "will be in the form of a three dimensional data cube in which every pixel of the two " \
                            "dimensional grid will be associated with a specific optical spectrum (Figure 2) that can " \
                            "then be analysed."

        self.text_text_2 = "\n\nThe hyperspectral camera system that this software has been designed for is the TIVITA® " \
                           "Suite software version 1.4.1.5 from the TIVITA® Tissue Hyperspectral Camera from " \
                           "Diaspective Vision GmbH in Germany (Figure 3). The software will be regularly updated for " \
                           "subsequent TIVITA® Tissue versions."

        self.text_text_3a = "\n\nThe hyperspectral camera works as a line-scanner in the way that the image is scanned " \
                            "in a linear fashion several times while the holographic transmission grating changes over " \
                            "time allowing different wavelengths to pass through the spectral filter (Figure 4).\n\n\n"

        self.text_text_3b = "\n\nThis software is optimized for Python on Apple Mac. " \
                            "\nIt can be downloaded from "
        self.text_text_3c = "github.com/icamplis/HyperGui."
        self.text_text_3d = "\nIn order to be able to use this software the primary data created by the camera" \
                            " system must not be manipulated and in its original form exemplarily displayed on the" \
                            " right (Figure 5)."

        self.text_text_4 = "\n\nThe software of the camera system creates four different index pictures that are " \
                           "calculated from specific wavelength areas as depicted on the right (Figures 6a and 6b):" \
                           "\n- StO2: HSI Tissue Oxygen Saturation		        570-590 nm & 740-780 nm" \
                           "\n- NIR: HSI Tissue Perfusion (Near-Infrared)		 655-735 nm & 825-925 nm" \
                           "\n- THI: HSI Tissue Haemoglobin Index		         530-590 nm & 785-825 nm" \
                           "\n- TWI: HSI Tissue Water Index			              880-900 nm & 955-980 nm" \
                           "\n\nThe formulas used are displayed on the right (Figure 7). The parameters represented " \
                           "by the letter variables are part of the corporate secret and cannot be provided." \
                           "\n\nExemplary images can be seen in Figure 8."

        self.text_text_5 = "\n\nThe purpose of this software is the facilitation of an extensive analysation of the " \
                           "hyperspectral datacube." \
                           "\nEvery analysis can be exported either as .png if it is a graphical result or as .csv " \
                           "if it is a numerical result. " \
                           "\nThis software is particularly suited to analyze the application of dyes, identify " \
                           "limitations and influencing factors of the method, classify tissue and find new " \
                           "formulas for new tissue characteristics." \
                           "\nWhen exporting the CSV files in the 'Data and Sources' window or when choosing the " \
                           "source data for the windows in the drop-down menu in the 'Images and Diagrams' window, " \
                           "the term 'normalized' refers to the fact that data has been shifted and redistributed " \
                           "such that the lowest value is 0 and the highest is 1, with the relative distribution " \
                           "remaining the same. For datasets 'without negative values' the distribution is kept " \
                           "the same and the number 0 remains at the same spot."

        self.text_text_6a = "\n\nHyperGUI© is a freeware Python tool for the extensive analysis and evaluation of " \
                            "hyperspectral data cubes from the TIVITA® Suite software version 1.4.1.5 from the " \
                            "TIVITA® Tissue Hyperspectral Camera from Diaspective Vision GmbH in Germany."
        self.text_text_6b = "\n\nwebsite:   "
        self.text_text_6c = "diaspective-vision.com"
        self.text_text_6d = "\nemail:     office@diaspective-vision.com " \
                            "\n\nVersion 1.1.0" \
                            "\nOpen source hyperspectral data processing and analysis software." \
                            "\n\nThis is not a certified medical product and cannot be used for clinical diagnostics. " \
                            "\nThe creators cannot be held liable for faulty indications and their consequences, " \
                            "neither assume any juridical responsibility nor any liability." \
                            "\n\n\nCand. med. Alexander Studier-Fischer" \
                            "\nUniversity Hospital of Heidelberg" \
                            "\nDepartment of General, Visceral- and Transplantation Surgery" \
                            "\nIm Neuenheimer Feld 110" \
                            "\n69120 Heidelberg, Germany" \
                            "\nalexander@studier-fischer.de" \
                            "\n\nIsabella Camplisson" \
                            "\nCalifornia Institute of Technology" \
                            "\nDepartment of Engineering and Applied Science" \
                            "\n1200 E California Boulevard MSC 161, CA, USA 91125" \
                            "\n\nGuanyue Wu" \
                            "\nUniversity of British Columbia, Faculty of Science" \
                            "\nICICS Computer Science" \
                            "\n2366 Main Mall, Vancouver, BC V6T 1Z4, Canada" \
                            "\n\nPD Dr. med. Felix Nickel, MME" \
                            "\nUniversity Hospital of Heidelberg" \
                            "\nDepartment of General, Visceral- and Transplantation Surgery" \
                            "\nIm Neuenheimer Feld 110" \
                            "\n69120 Heidelberg, Germany" \
                            "\n\nThis software is made available by the provider 'as is' and 'with all faults'. The " \
                            "provider makes no representations or warranties of any kind concerning the safety, " \
                            "suitability or inaccuracies. You are solely responsible for determining whether this " \
                            "graphical user interface is compatible with your equipment and other software installed " \
                            "on your equipment. The provider will not be liable for any damages you may suffer in " \
                            "connection with using, modifying, or distributing this software."

        self.image_box = None
        self.images = []

        self.image_1a = "Schematic comparison of optical properties of specific molecules to a fingerprint."
        self.image_1b = "Schematic illustration of the three-dimensional data cube obtained from hyperspectral imaging."
        self.image_2 = "TIVITA® Tissue Hyperspectral Camera from Diaspective Vision GmbH."
        self.image_3a = "Schematic illustration of the working principles of the line scanner and the holographic " \
                        "transmission grating of the camera system."
        self.image_3b = "Original file arrangement of the TIVITA® Tissue Hyperspectral Camera system."
        self.image_4a = "Illustration of the structure of a TIVITA® Tissue data cube and a schematic illustration " \
                        "indicating which wavelength areas are used to calculate the index pictured. A gastric conduit " \
                        "was chosen as a sample image."
        self.image_4b = "Both formulas used by the software to calculate the four index pictures. The top formula is " \
                        "used for StO2, the bottom formula is used for NIR, THI, and TWI with the different wavelength" \
                        " areas specified in Figures 6a and 6b. The letter variables 'r' and 's' cannot be provided."
        self.image_4c = "Original images from the TIVITA camera system. On the top there is the " \
                        "regular RGB image of the gastric conduit that was chosen as an example. Below that the four " \
                        "index pictures (StO2, NIR, THI and TWI) are displayed."

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self.parse_images()
        self.build_spacer()
        self._build_prev_next()
        self._build_page(self.number)

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def parse_images(self):
        for i in range(1, 8):
            self.images.append(image_to_array('./image0' + str(i) + '.png'))

    def build_spacer(self):
        spacer1 = Text(self.root, height=47)
        spacer1.grid(padx=(25, 0), pady=15, row=0, column=0)
        spacer1.config(state=DISABLED)
        spacer2 = Text(self.root, height=49, width=110)
        spacer2.grid(padx=(0, 25), pady=(15, 0), row=0, column=1)
        spacer2.config(state=DISABLED)

    def _build_page(self, page_num):
        if page_num == 1:
            self._build_page1()
        if page_num == 2:
            self._build_page2()
        if page_num == 3:
            self._build_page3()
        if page_num == 4:
            self._build_page4()
        if page_num == 5:
            self._build_page5()
        if page_num == 6:
            self._build_page6()
        if page_num == 7:
            self._build_page7()
        if page_num == 8:
            self._build_page8()
        if page_num == 8:
            self._build_page9()

    def _build_page1(self):
        # text
        text = Text(self.root, height=28, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_1, ('title', str(0)))
        text.insert(END, self.text_text_1a)
        text.insert(END, self.text_text_1b)
        text.insert(END, self.text_text_1c, ('link0', str(1)))
        text.insert(END, self.text_text_1d)
        text.insert(END, self.text_text_1e)
        text.tag_config('title', foreground='black', underline=True)
        text.tag_config('link0', foreground='blue', underline=True)
        text.tag_bind('link0', '<Button-1>', lambda x: self.__hyperlink(url=self.urls[0]))
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[0], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=2, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 1', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_1a)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(0, 60), row=0, column=1)
        image_text1.config(state=DISABLED)
        image_text2 = Text(self.root, height=2, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text2.insert(END, 'Figure 2', ('tit', str(3)))
        image_text2.insert(END, ' | ' + self.image_1b)
        image_text2.tag_config('tit', foreground='black')
        image_text2.config(state=DISABLED)
        image_text2.grid(padx=(0, 25), pady=(570, 15), row=0, column=1)

    def _build_page2(self):
        # text
        text = Text(self.root, height=7, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_2, ('title', str(0)))
        text.insert(END, self.text_text_2)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[1], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6, original=True,
                   row=0, columnspan=1)
        image_text = Text(self.root, height=2, width=100, wrap=WORD, highlightthickness=0,
                           foreground=tkcolour_from_rgb(GREY))
        image_text.insert(END, 'Figure 3', ('tit', str(1)))
        image_text.insert(END, ' | ' + self.image_1a)
        image_text.tag_config('tit', foreground='black')
        image_text.grid(padx=(0, 25), pady=(660, 0), row=0, column=1)
        image_text.config(state=DISABLED)

    def _build_page3(self):
        # text
        text = Text(self.root, height=15, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_3a, ('title', str(0)))
        text.insert(END, self.text_text_3a)
        text.insert(END, self.title_3b, ('title', str(2)))
        text.insert(END, self.text_text_3b)
        text.insert(END, self.text_text_3c, ('link', str(1)))
        text.insert(END, self.text_text_3d)
        text.tag_config('link', foreground='blue', underline=True)
        text.tag_bind('link', '<Button-1>', lambda x: self.__hyperlink(url=self.urls[1]))
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[2], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=2, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 4', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_3a)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(90, 0), row=0, column=1)
        image_text1.config(state=DISABLED)
        image_text2 = Text(self.root, height=2, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text2.insert(END, 'Figure 5', ('tit', str(3)))
        image_text2.insert(END, ' | ' + self.image_3b)
        image_text2.tag_config('tit', foreground='black')
        image_text2.config(state=DISABLED)
        image_text2.grid(padx=(0, 25), pady=(580, 15), row=0, column=1)

    def _build_page4(self):
        # text
        text = Text(self.root, height=16, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_4, ('title', str(0)))
        text.insert(END, self.text_text_4)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[3], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=3, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 6a', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_4a)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(640, 0), row=0, column=1)
        image_text1.config(state=DISABLED)

    def _build_page5(self):
        # text
        text = Text(self.root, height=16, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_4, ('title', str(0)))
        text.insert(END, self.text_text_4)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[4], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=3, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 6b', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_4a)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(640, 0), row=0, column=1)
        image_text1.config(state=DISABLED)

    def _build_page6(self):
        # text
        text = Text(self.root, height=16, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_4, ('title', str(0)))
        text.insert(END, self.text_text_4)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[5], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=4, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=3, width=100, wrap=WORD, highlightthickness=0,
                          foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 7', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_4b)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(500, 0), row=0, column=1)
        image_text1.config(state=DISABLED)

    def _build_page7(self):
        # text
        text = Text(self.root, height=16, width=70, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_4, ('title', str(0)))
        text.insert(END, self.text_text_4)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 20), pady=15, row=0, column=0)
        # images
        make_image(self.root, self.images[6], column=1, rowspan=1, lower_scale_value=None,
                   upper_scale_value=None, color_rgb=WHITE, figwidth=7.5, figheight=6.5, original=True,
                   row=0, columnspan=1)
        image_text1 = Text(self.root, height=3, width=100, wrap=WORD, highlightthickness=0,
                           foreground=tkcolour_from_rgb(GREY))
        image_text1.insert(END, 'Figure 8', ('tit', str(2)))
        image_text1.insert(END, ' | ' + self.image_4c)
        image_text1.tag_config('tit', foreground='black')
        image_text1.grid(padx=(0, 25), pady=(690, 0), row=0, column=1)
        image_text1.config(state=DISABLED)

    def _build_page8(self):
        # text
        text = Text(self.root, height=10, width=150, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_5, ('title', str(0)))
        text.insert(END, self.text_text_5)
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 260), pady=15, row=0, column=0, columnspan=2)

    def _build_page9(self):
        # text
        text = Text(self.root, height=42, width=150, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, self.title_6, ('title', str(0)))
        text.insert(END, self.text_text_6a)
        text.insert(END, self.text_text_6b)
        text.insert(END, self.text_text_6c, ('link0', str(1)))
        text.insert(END, self.text_text_6d)
        text.tag_config('link0', foreground='blue', underline=True)
        text.tag_bind('link0', '<Button-1>', lambda x: self.__hyperlink(url=self.urls[0]))
        text.tag_config('title', foreground='black', underline=True)
        text.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        text.grid(padx=(25, 260), pady=15, row=0, column=0, columnspan=2)

    def _build_prev_next(self):
        self.prev_button = make_button(self.root, text='Previous', width=9, command=self.__previous, row=10, column=0,
                                       columnspan=2, inner_pady=5, outer_padx=(0, 130), outer_pady=15)
        self.next_button = make_button(self.root, text='Next', width=9, command=self.__next, row=10, column=0,
                                       columnspan=2, inner_pady=5, outer_padx=(130, 0), outer_pady=15)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __previous(self):
        if self.number == 1:
            pass
        else:
            self.build_spacer()
            self.number -= 1
            self._build_page(self.number)

    def __next(self):
        if self.number == 8:
            pass
        else:
            self.build_spacer()
            self.number += 1
            self._build_page(self.number)

    @staticmethod
    def __hyperlink(url):
        webbrowser.open(url, new=1)

