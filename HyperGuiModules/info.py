from HyperGuiModules.utility import *
import webbrowser


class Info:
    def __init__(self, info_frame, listener):
        self.root = info_frame
        self.listener = listener
        self.info_button = None
        self.info_text = None

        # INFORMATION
        self.info1 = "\n\nHyperGUI© is a freeware Python tool for the extensive analysis and evaluation of " \
                     "hyperspectral data cubes from the TIVITA® Suite software version 1.4.1.5 from the " \
                     "TIVITA® Tissue Hyperspectral Camera from Diaspective Vision GmbH in Germany."
        self.info2 = "\n\nwebsite:   "
        self.info3 = "diaspective-vision.com"
        self.info4 = "\nemail:     office@diaspective-vision.com " \
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
        self.source_output_info = "This window allows to select the source datacubes for the analysis. The source data " \
                                  "has to be provided in its original file structure the way it is saved by the TIVITA® " \
                                  "Tissue Hyperspectral Camera (that means stored in a folder that contains the " \
                                  "Datacube (.dat) as well as the 5 PNGs: RGB-Image.png, Oxygenation.png, " \
                                  "NIR-Perfusion.png, THI.png and TWI.png as depicted in Figure 5 of the introduction)." \
                                  "\n\nDepending on one’s preference the folder containing these 6 elements can be " \
                                  "selected individually via 'Select Data Directory'. Alternatively - for the purpose " \
                                  "of analyzing several datacubes in the same fashion at the same time - a separate " \
                                  "folder can be created previously that contains a number of primary data folders " \
                                  "and then be selected with the option 'Select Data Superdirectory'. Single primary " \
                                  "data folders can then be removed by 'Remove Data Cube'." \
                                  "\n\nAfter your datacube(s) is displayed in the white box you have to select it for " \
                                  "rendering before you continue with 'Images and Diagrams'."
        self.analysis_form_info = "In this window the analysis settings for the 'New Image' can be specified. In case " \
                                  "that only a certain area of the spectrum is interesting, this area can be " \
                                  "specified in the text boxes for lower and upper wavelength (between 500 - 995 nm). " \
                                  "In case one not only wants to visualize simple wavelength areas, but also wants to " \
                                  "perform mathematical operations - much like the original mathematical formulas for " \
                                  "StO2, NIR, THI and TWI - there are placeholders for 8 formulas that can be selected " \
                                  "and modified. " \
                                  "\n\nThese formulas can be modified depending on the need or scientific " \
                                  "deliberations by clicking on “edit”. The formula has to be written in Python. " \
                                  "The notation has to be read as following:" \
                                  "\nx[:,:,:] means all the values in all x and y dimensions and through all the " \
                                  "wavelengths" \
                                  "\nx[2,7,13] means only the value of pixel x=2+1=3 and y=7+1=8 at wavelength " \
                                  "500+(5*13)=565 nm" \
                                  "\nx[2:8,8:200,0:50] means the values of the pixels x=(3 to 9) and y=(9 to 201) at " \
                                  "the wavelengths 500 to 750 nm" \
                                  "\n\nThe pixel in the upper left hand corner is [0,0,:], the pixel in the lower " \
                                  "right hand corner is [640,480,:]."
        self.csv_info = "This window allows to save all of the numerical information in .csv files with 480 rows" \
                        " and 640 columns in accordance to the pixel distribution of 480 x 640 in the original" \
                        " recordings." \
                        "\n\nNormalization of datasets is performed by stretching or compressing the original values " \
                        "into a scale from 0 to 1. The addition 'without negative values' describes the fact that in " \
                        "these datasets all the values are removed that used to be negative in the original file " \
                        "(so either in the '1. Original Reflectance' or '2.Original Absorbance')."
        self.save_info = "This window allows to save all of the features of the 'Images and Diagrams' window that" \
                         " have a tick in the blue boxes. These features can either be saved for the selected" \
                         " datacube in the 'Source and Output' window by 'Save for Selected Data Cube Only'." \
                         " Alternatively, these features can be saved for all of the datacubes - in case that" \
                         " several data cubes were uploaded - by 'Save for All Data Cubes'."
        self.parameter_info = "In this window, the letter variables for the formulas depicted in Figure 7 of the" \
                              " introduction that are used for the creation of the index pictures can be specified." \
                              " For research purposes these can be enquired from Diaspective Vision."
        self.original_info = "This window uploads the original pngs and allows to mask a specific area of interest" \
                             " with a 9-point freehand selection tool for further analysis. After having marked" \
                             " the specific area, the button 'Use mask' has to be selected in order for the further" \
                             " analysis steps to work. \n\nRight click maximizes the image."
        self.input_info = "Here you can input coordinates manually. Make sure that your values are integers " \
                          "(they will be rounded if not), and that your x values are in the interval [0, 640] " \
                          "and your y values are in the interval [0, 480]. Press 'Go' when you are ready to upload " \
                          "your coordinates."
        self.original_data_info = "This window gives the parametric and non-parametric statistics of the original " \
                                  "image either for the whole image or for the masked region."
        self.recreated_info = "This window allows to recreate the index images from the TIVITA® Tissue Hyperspectral" \
                              " Camera system with the parameters specified in 'Parameter Specification for" \
                              " \"Recreated Image\"'. The purpose of this window is to comprehend what the images" \
                              " - according to the formulas - would look like and to compare them to the original" \
                              " pngs in the window above." \
                              "\n\nThe source data can be specified by the drop-down menu." \
                              "\n\nRight click maximizes the image." \
                              "\n\n'Lower' and 'Upper' are the numerical limits over which the the colour scale or " \
                              "gray scale is equally distributed. These limits are the maximum and minimum value of " \
                              "the calculated pictures by default ('OG'). They can be changed to be the normalized " \
                              "values (everything divided by the maximum value) ('NORM') or chosen freely similar to " \
                              "the idea of choosing different window sizes for CT scans in order to visualize" \
                              " different aspects."
        self.recreated_data_info = "This window gives the parametric and non-parametric statistics of the recreated " \
                                   "image either for the whole image or for the masked region."
        self.new_info = "This window allows to create a new colour-coded image that is able to visualize high and " \
                        "low hyperspectral values. " \
                        "\n\nWhen 'WL' is selected, the images are calculated from the mean hyperspectral values " \
                        "specified by the lower and upper wavelength specified in the 'Analysis Settings for \"New " \
                        "Image\"' window. " \
                        "\n\nWhen “IDX” is selected, the images are calculated from the hyperspectral values" \
                        " that are applied to the formula chosen in the Analysis Settings for \"New Image\"' window." \
                        "\n\nThe source data can be specified by the drop-down menu." \
                        "\n\nRight click maximizes the image." \
                        "\n\n'Lower' and 'Upper' are the numerical limits over which the the colour scale or gray " \
                        "scale is equally distributed. These limits are the maximum and minimum value of the " \
                        "calculated pictures by default ('OG'). They can be changed to be the normalized values " \
                        "(everything divided by the maximum value) ('NORM') or chosen freely similar to the idea " \
                        "of choosing different window sizes for CT scans in order to visualize different aspects."
        self.new_data_info = "This window gives the parametric and non-parametric statistics of the new image " \
                             "either for the whole image or for the masked region."
        self.diagram_info = "This window allows to specify whether all the statistics and graphs should be " \
                            "calculated for the whole image or the masked region specified in the 'Original Image'" \
                            " window through the 9-point freehand selection tool."
        self.hist_info = "This window gives a histogram of the hyperspectral recording. The x-axis is the " \
                         "hyperspectral value and the y-axis is the absolute frequency. A boxplot can be " \
                         "overblended into the histogram either depicting parametric ('P' with mean and " \
                         "standard-deviation) or non-parametric ('NP' with median, interquartile range and minimum " \
                         "& maximum) distribution characteristics." \
                         "\n\nThe source data can be specified by the drop-down menu." \
                         "\n\nThe scales and step size can be adjusted with the text boxes on the right; the area " \
                         "where the local minimum and maximum should be identified can be specified with the text " \
                         "boxes for the lower x value ('Lower') and upper x value ('Upper')." \
                         "\n\nRight click maximizes the diagram."
        self.abspec_info = "This window depicts the optical spectrum of the hyperspectral recording. " \
                           "\n\nThe source data can be specified by the drop-down menu." \
                           "\n\nThe scales can be adjusted with the text boxes on the right; the area where the " \
                           "local minimum and maximum should be identified can be specified with the text boxes for " \
                           "the lower x value ('Lower') and upper x value ('Upper')." \
                           "\n\nRight click maximizes the diagram."
        self.colour_info = "This window gives a first impression of the colour and gray scales that were used. The " \
                           "colour scale is the 'Jetscale' from Python which has also been used for the original " \
                           "index pictures from the TIVITA® Tissue Hyperspectral Camera. Blue means low value and " \
                           "red means high value. For every of the three image windows the used scale can be " \
                           "specified by a drop-down menu."
        self.hist_calc_info = "This window allows to perform basic mathematical operations on histograms that have " \
                              "been saved previously. It is mainly thought to enable a baseline subtraction, but " \
                              "can be used for other calculations as well. By default the saving folder for the " \
                              "newly 'Calculated Histogram' will be the same folder from which the 'First Histogram' " \
                              "has been pulled. However, this can be changed via 'Select Output Folder'."
        self.spec_calc_info = "This window allows to perform basic mathematical operations on optical spectrums that " \
                              "have been saved previously. It is mainly thought to enable a baseline subtraction, but " \
                              "can be used for other calculations as well. By default the saving folder for the " \
                              "newly 'Calculated Optical Spectrum' will be the same folder from which the 'First " \
                              "Optical Spectrum' has been pulled. However, this can be changed via 'Select Output " \
                              "Folder'."

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_info_button()
        self._build_info_text()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_info_button(self):
        self.info_label = make_label_button(self.root, text='App Info', command=self.__info, width=8)
        self.info_label.grid(padx=(0, 40))

    def _build_info_text(self):
        text = "*click on the section titles to find further information about that specific widget"
        self.info_text = Text(self.root, height=6, width=19, highlightthickness=0, wrap=WORD,
                              bg=tkcolour_from_rgb(BACKGROUND))
        self.info_text.insert(END, text)
        self.info_text.config(state="disabled")
        self.info_text.grid(row=1, column=0, padx=15)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        # create the toplevel window with title and place in top left of screen
        window = Toplevel()
        window.title("App Information")
        window.geometry("+0+0")
        # create textbox and insert info
        text = Text(window, height=45, width=100, wrap=WORD, highlightthickness=0, foreground=tkcolour_from_rgb(GREY))
        text.insert(END, "App Information", ('title', str(0)))
        text.insert(END, self.info1)
        text.insert(END, self.info2)
        text.insert(END, self.info3, ('link', str(0)))
        text.insert(END, self.info4)
        text.tag_config('link', foreground='blue', underline=True)
        text.tag_bind('link', '<Button-1>', lambda x: self.__hyperlink(url='http://diaspective-vision.com'))
        text.tag_config('title', foreground='black', underline=True)
        # disable text, add padding and make resizable False
        text.config(state="disabled")
        text.grid(padx=5, pady=5)
        window.resizable(width=False, height=False)

    @staticmethod
    def __hyperlink(url):
        webbrowser.open(url, new=1)
