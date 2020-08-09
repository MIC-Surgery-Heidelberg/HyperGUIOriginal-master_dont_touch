#Added by by Jan Odenthal, University of Heidelberg, odenthal@stud.uni-heidelberg.de

from HyperGuiModules.utility import *
from tensorflow.python.keras.models import load_model
from PIL import Image
import numpy as np
from sklearn.metrics import auc
import os
import logging
import glob
from tkinter import filedialog
from scipy.ndimage.filters import gaussian_filter
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import copy
import random

class Prediction: 
    def __init__(self, prediction_frame, listener):
        self.root = prediction_frame 
        self.listener = listener 
        self.x_vals = np.arange(500, 1000, 5)
        
        self.gini_map = None 
        self.softmax_map = None 
        self.prediction_map = None 
        self.ground_truth_map = None 
        
        self.gini_RGB = None 
        self.softmax_RGB = None 
        self.prediction_RGB = None 
        self.ground_truth_RGB = None 
        self.current_RGB = None 
        self.save_RGB = None 
        self.RGB = None 
        
        self.interactive_absorption_spec_graph = None
        
        self.model = None 
        
        self.edge_length = None 
        self.gt_dir = None 
        
        self.avGini = None 
        self.avSm = None 
        self.sdGini = None 
        self.sdSm = None 
        self.accuracy = None 
        
        self.image=None 
        self.legend = None
        self.legAx = None
        self.legend_canvas = None
        self.legend_elements = None
        self.leg_selection = 0
        self.first_value = 0
        self.second_value = 0
        self.third_value = 0
        self.y_high = 1
        self.y_low = 0
        
        self.output_path = None
        self.drop_down_legVar = StringVar()
        self.drop_down_var2 = StringVar()

        self.drop_down_var = StringVar()
        self.choices = ['1. Prediction', 
                        '2. Groundtruth',
                        '3. RGB',
                        '4. Gini',
                        '5. Softmax']
        
        self.choices2 = ['0. derivative', 
                        '1. derivative',
                        '2. derivative',
                        ]


        self.organMaskNamesLeft=['empty', ['/*_background.tif', '/*_syringe.tif', '/*_anorganic_artifact.tif', '/*_tube.tif'],  '/*_glove.tif',  '/*_cloth.tif', '/*_abdominal_linen.tif', '/*_metal.tif', '/*_white_compress.tif', '/*_foil.tif','/*_peritoneum.tif','/*_fat.tif', '/*_skin.tif', '/*_bladder.tif']
        self.organMaskNamesRight=['/*_colon.tif', '/*_jejunum.tif', '/*_liver.tif', '/*_spleen.tif', '/*_stomach.tif', '/*_omentum.tif', '/*_gallbladder.tif', '/*_pancreas.tif', '/*_heart.tif', '/*_lung.tif']
        self.organMaskNames = self.organMaskNamesLeft + self.organMaskNamesRight
        for ii in range(len(self.organMaskNames)):
            string = str(self.organMaskNames[ii])
            string = string.replace('.tif', '')
            string = string.replace('/*_', '')
            string = string.replace(']', '')
            string = string.replace('[', '')
            self.organMaskNames[ii]=string


        self.gini_slider = None 
        self.softmax_slider = None 
        self.select_gt_folder_button = None 
        self.text_accuracy = None 
        self.gradient = "og"
        self.absorption_spec = None
        self.absorption_spec_gradient1 = None
        self.absorption_spec_gradient2 = None

        self.prediction_graph = None
        self.RGB_graph = None
        self.axes = None 
        self.axes_external = None
        self.interactive_prediction = None 
        self.interactive_RGB = None 

        self.text_pixel_value = None 

        self.info_label = None 


        
        self.output_path = None
        
        self.all_colors = [(100,100,100), (0,255,0), (0,0,255), (255,170,0), (255,255,0), (0,255,255), (255,0,255), (255,170,170), (120,120,255), (0,255,120), (255,120,120), (255,255,255), (0,120,170), (50,50,200), (30,50,100), (100,50,30), (200,50,90), (120,90,200), (9, 151, 72), (244, 211, 61), (112, 203, 113), (107, 92, 188), (37, 47, 100), (84, 12, 200), (220,20,60), (255,0,0), (0,128,128), (255,215,0), (245,222,179), (188,143,143), (255,69,0), (94,73,168), (188,133,111), (100, 230, 22)]
        self.colors=copy.deepcopy(self.all_colors[0:23])
        
        self.cursor_class = None
        
        self._init_widgets() 

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def update_cube(self):
        self.__update_data()
    
    def update_prediction(self): 
        self._build_prediction_graph()
    
    def update_RGB(self, new_data):
        self.RGB = new_data
        print("Updating")
        self._build_RGB_graph()

    def _init_widgets(self):
        self._build_gini_slider() 
        self._build_select_model_button() 
        self._build_softmax_slider() 
        self._build_info_label()
        self._build_reset_button() 
        self._build_drop_down() 
        self._build_prediction_graph() 
        self._build_RGB_graph() 
        self._build_stats() 
        self._build_pixel_value() 
        self._build_select_gt_folder_button() 
        self._build_accuracy() 
        self._build_legend()
        self._search_stock_model()
        self._build_save_buttons()
        self._build_info_label_gini_softmax()
        self._build_legend_buttons()
        self._build_curve_graph()
        self._build_drop_down2()

    # --------------------------------------------------- GETTERS ----------------------------------------------------


    # ----------------------------------------------- BUILDERS (MISC) -------------------------------------------------

    def _build_save_buttons(self):
        make_button(self.root, text="Change Output Folder", command=self.__select_output, row=8, column=0,
                    outer_padx=15, width=15, height=1, columnspan=1, outer_pady=(0, 10), inner_pady=5)
        make_button(self.root, "Save Image", row=8, column=1, command=self.__save_RGB, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=1)
        make_button(self.root, "Save CSV", row=8, column=5, command=self.__save_CSV, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=1)
        make_button(self.root, "Save Image with Legend", row=8, column=3, command=self.__save_RGB_with_legend, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2, width=20)
    
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Prediction', command=self.__info, width=8)

    def _build_info_label_gini_softmax(self):
        self.gini_label = TButton(self.root, text="Gini", width=8, command=self.__gini_info)
        Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)),
                      bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
        Style().theme_use('default')
        self.gini_label.grid(row=0, column=3, padx=(15, 0), pady=15)
        
        self.soft_label = TButton(self.root, text="Max of Softmax", width=16, command=self.__soft_info)
        Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)),
                      bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
        Style().theme_use('default')
        self.soft_label.grid(row=0, column=4, padx=(15, 0), pady=15)


    def _build_gini_slider(self): 
        self.gini_slider = make_slider(self.root, "", row=0, rowspan=5, column=3, command=self._build_prediction_graph, outer_padx=15, outer_pady=(0, 10), columnspan=1)

    def _build_softmax_slider(self): 
        self.softmax_slider = make_slider(self.root, "", row=0, rowspan=5, column=4, command=self._build_prediction_graph, outer_padx=15, outer_pady=(0, 10), columnspan=1)

    def _build_reset_button(self): 
        self.reset_button = make_button(self.root, "Reset", row=6, column=3, command=self.__reset, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)

    def _build_drop_down(self): 
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__change_mode)
        self.drop_down_menu.configure(highlightthickness=0, width=20,
                                      anchor='w', padx=15)
        self.drop_down_menu.grid(column=1, row=0, columnspan=2, padx=(0, 15))
        
    def _build_drop_down2(self): 
        self.drop_down_var2.set(self.choices2[0])
        self.drop_down_menu2 = OptionMenu(self.root, self.drop_down_var2, *self.choices2, command=self.__set_der)
        self.drop_down_menu2.configure(highlightthickness=0, width=20,
                                      anchor='w', padx=15)
        self.drop_down_menu2.grid(column=7, row=6, columnspan=6, padx=(0, 15))
        
        self.lower_text = make_text(self.root, content="Lower: ", bg=tkcolour_from_rgb(BACKGROUND), column=7, row=8,
                                    width=7, columnspan=1, pady=(0, 10))
        self.lower_input = make_entry(self.root, row=8, column=8, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.y_low))
        
        self.upper_text = make_text(self.root, content="Upper: ", bg=tkcolour_from_rgb(BACKGROUND), column=9, row=8,
                                    width=7, columnspan=1, pady=(0, 10))
        self.upper_input = make_entry(self.root, row=8, column=10, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.y_high))
    
    def _build_select_model_button(self): 
        self.text_pixel_value = make_text(self.root, content="Model:",
                                  bg=tkcolour_from_rgb(BACKGROUND), column=0, row=1, width=10, columnspan=1, padx=0,
                                  state=NORMAL)
        self.select_model_button = make_button(self.root, text="Select model",
                                                   command=self.__select_model, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=2, column=0, width=11, outer_pady=(0, 5))
        
    def _build_select_gt_folder_button(self): 
        self.select_gt_folder_button = make_button(self.root, text="Select GT-Folder",
                                                   command=self.__select_gt_folder, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=3, column=0, width=11, outer_pady=(0, 5))
        
    def _build_pixel_value(self, event=None): 
        string="Pixelvalues"
        if event is not None:
            pos = self.axes.get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480 and self.gini_map is not None and self.softmax_map is not None:
                X  = np.rot90(self.listener.data_cube) 
                #index = np.argmax(self.prediction_map[Yc,Xc,:])
                #index2 = np.argmax(self.ground_truth_map[Yc,Xc,:]) 
                gini = self.gini_map[Yc, Xc]
                softmax = self.softmax_map[Yc, Xc]
                self.cursor_class = np.argmax(self.prediction_map[Yc, Xc, :])
                string = 'x={:.0f}, y={:.0f}; S={:.02f}, G={:.02f}'.format(Xc, Yc, softmax, gini)
                self.absorption_spec = X[Yc, Xc, :]
                self.absorption_spec_gradient1 = np.gradient(self.absorption_spec)
                self.absorption_spec_gradient2 = np.gradient(self.absorption_spec_gradient1)
                self._build_curve_graph()
        self.text_pixel_value = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=1, width=30, columnspan=2, padx=0,
                                  state=NORMAL)
        

        
    def _build_pixel_value_external(self, event=None): 
        string="Pixelvalues"
        if event is not None:
            pos = self.axes_external.get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480 and self.gini_map is not None and self.softmax_map is not None:
                #index = np.argmax(self.prediction_map[Yc,Xc,:])
                #index2 = np.argmax(self.ground_truth_map[Yc,Xc,:]) 
                gini = self.gini_map[Yc, Xc]
                softmax = self.softmax_map[Yc, Xc]
                string = 'x={:.0f}, y={:.0f}; S={:.02f}, G={:.02f}'.format(Xc, Yc, softmax, gini)
        self.text_pixel_value = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=1, width=30, columnspan=2, padx=0,
                                  state=NORMAL)
        
    def _build_accuracy(self): 
        string="ACCURACY"
        if self.accuracy is not None:
            string = 'ACCURACY: ' + str(self.accuracy)
        self.text_accuracy = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=2, width=16, columnspan=2, padx=0,
                                  state=NORMAL)
    def _build_legend(self):
        legend_stringsLeft=['']*12
        legend_stringsRight=['']*10
        for ii in range(len(self.organMaskNamesLeft)):
            string = str(self.organMaskNamesLeft[ii])
            string = string.replace('.tif', '')
            string = string.replace('/*_', '')
            string = string.replace(']', '')
            string = string.replace('[', '')
            legend_stringsLeft[ii]=string
        for ii in range(len(self.organMaskNamesRight)):
            string = str(self.organMaskNamesRight[ii])
            string = string.replace('.tif', '')
            string = string.replace('/*_', '')
            string = string.replace(']', '')
            string = string.replace('[', '')
            legend_stringsRight[ii]=string
        self.legend_elementsLeft = [Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[0], markerfacecolor=(self.colors[0][0]/255, self.colors[0][1]/255, self.colors[0][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label="anorganic rest", markerfacecolor=(self.colors[1][0]/255, self.colors[1][1]/255, self.colors[1][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[2], markerfacecolor=(self.colors[2][0]/255, self.colors[2][1]/255, self.colors[2][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[3], markerfacecolor=(self.colors[3][0]/255, self.colors[3][1]/255, self.colors[3][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[4], markerfacecolor=(self.colors[4][0]/255, self.colors[4][1]/255, self.colors[4][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[5], markerfacecolor=(self.colors[5][0]/255, self.colors[5][1]/255, self.colors[5][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[6], markerfacecolor=(self.colors[6][0]/255, self.colors[6][1]/255, self.colors[6][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[7], markerfacecolor=(self.colors[7][0]/255, self.colors[7][1]/255, self.colors[7][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[8], markerfacecolor=(self.colors[8][0]/255, self.colors[8][1]/255, self.colors[8][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[9], markerfacecolor=(self.colors[9][0]/255, self.colors[9][1]/255, self.colors[9][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[10], markerfacecolor=(self.colors[10][0]/255, self.colors[10][1]/255, self.colors[10][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsLeft[11], markerfacecolor=(self.colors[11][0]/255, self.colors[11][1]/255, self.colors[11][2]/255), markersize=15)]
        self.legend_elementsRight = [Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[0], markerfacecolor=(self.colors[12][0]/255, self.colors[12][1]/255, self.colors[12][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[1], markerfacecolor=(self.colors[13][0]/255, self.colors[13][1]/255, self.colors[13][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[2], markerfacecolor=(self.colors[14][0]/255, self.colors[14][1]/255, self.colors[14][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[3], markerfacecolor=(self.colors[15][0]/255, self.colors[15][1]/255, self.colors[15][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[4], markerfacecolor=(self.colors[16][0]/255, self.colors[16][1]/255, self.colors[16][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[5], markerfacecolor=(self.colors[17][0]/255, self.colors[17][1]/255, self.colors[17][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[6], markerfacecolor=(self.colors[18][0]/255, self.colors[18][1]/255, self.colors[18][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[7], markerfacecolor=(self.colors[19][0]/255, self.colors[19][1]/255, self.colors[19][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[8], markerfacecolor=(self.colors[20][0]/255, self.colors[20][1]/255, self.colors[20][2]/255), markersize=15),
                   Line2D([0], [0], marker='o', color='w', label=legend_stringsRight[9], markerfacecolor=(self.colors[21][0]/255, self.colors[21][1]/255, self.colors[21][2]/255), markersize=15)]
        
        axcolor = 'lightgoldenrodyellow'
        self.legend = Figure(figsize=(4, 3))
        gs = self.legend.add_gridspec(1, 2)
        self.legAxLeft = self.legend.add_subplot(gs[0,0])
        self.legAxRight = self.legend.add_subplot(gs[0,1])
        
        self.legend_elementsLeft = self.legend_elementsLeft[0:11]
        self.legAxLeft.legend(handles=self.legend_elementsLeft, loc='left') 
        self.legAxLeft.axis('off') 

        self.legend_elementsRight = self.legend_elementsRight[0:9]
        self.legAxRight.legend(handles=self.legend_elementsRight, loc='right') 
        self.legAxRight.axis('off') 
        
        self.legend_canvas = FigureCanvasTkAgg(self.legend, master=self.root)
        self.legend_canvas.draw()
        self.legend_canvas.get_tk_widget().grid(column=7, row=0, columnspan=6, rowspan=4, ipady=0, ipadx=0,
                                                        pady=0)
    def _build_legend_buttons(self):
        self.drop_down_legVar.set(self.organMaskNames[0])
        self.drop_down_legend = OptionMenu(self.root, self.drop_down_legVar, *self.organMaskNames, command=self.__change_leg_selection)
        self.drop_down_legend.configure(highlightthickness=0, width=7,
                                      anchor='w', padx=2)
        self.drop_down_legend.grid(column=7, row=4, pady=(5, 5))
        
        self.slider_r = make_slider(self.root, "", row=4, rowspan=1, column=8, command=self.__update_preview, columnspan=1, outer_pady=(5, 5))
        self.slider_b = make_slider(self.root, "", row=4, rowspan=1, column=9, command=self.__update_preview, columnspan=1, outer_pady=(5, 5))
        self.slider_g = make_slider(self.root, "", row=4, rowspan=1, column=10, command=self.__update_preview, columnspan=1, outer_pady=(5, 5))

        
        self.change_color_button = make_button(self.root, "Set", row=4, width=3, column=12, command=self.__set_color, inner_padx=5,
                                        inner_pady=5, outer_padx=(2,2), outer_pady=(5, 5), columnspan=1)
        
        self.preview = Figure(figsize=(0.3, 0.3))
        self.prevAx = self.preview.add_subplot(111)
        self.prev_canvas = FigureCanvasTkAgg(self.preview, master=self.root)
        self.prevAx.set_facecolor((self.slider_r.get()/100, self.slider_b.get()/100, self.slider_g.get()/100))
        self.prevAx.set_position([0, 0, 1, 1])
        self.prev_canvas.draw()
        self.prev_canvas.get_tk_widget().grid(column=11, row=4, columnspan=1, rowspan=1, ipady=0, ipadx=0,
                                                        pady=0)
        
    def _search_stock_model(self):
            model_path = (os.path.dirname(os.path.dirname(__file__)) + "/Models")
            models = glob.glob(model_path + "/*.h5")
            if(len(models) is not 0):
                self.__load_model(models[0])

        

    # ----------------------------------------------- BUILDERS (DATA) -------------------------------------------------

    def _build_stats(self): 

        # mean Gini
        self.mean_text_gini = make_text(self.root, content="GINI = " + str(self.avGini),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=1, row=3, width=12, columnspan=1, padx=0,
                                   state=NORMAL)
        # standard deviation Gini
        self.sd_text_gini = make_text(self.root, content="SD = " + str(self.sdGini), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=2, row=3, width=10, columnspan=1, padx=0, state=NORMAL)
        
        # mean SM
        self.mean_text_sm = make_text(self.root, content="SOFT = " + str(self.avSm),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=1, row=4, width=12, columnspan=1, padx=0,
                                   state=NORMAL)
        # standard deviation SM
        self.sd_text_sm = make_text(self.root, content="SD = " + str(self.sdSm), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=2, row=4, width=10, columnspan=1, padx=0, state=NORMAL)


    # ---------------------------------------------- BUILDERS (GRAPH) ------------------------------------------------

    def _build_prediction_graph(self, event=None):
        # create canvas
        self.prediction_graph = Figure(figsize=(6, 4))
        self.axes = self.prediction_graph.add_subplot(111)
        self.axes.set_aspect(2/3)
        self.prediction_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        self.axes.get_yaxis().set_visible(False)
        self.axes.get_xaxis().set_visible(False)
        if self.current_RGB is not None:
            softmax = self.softmax_slider.get()/100
            gini = self.gini_slider.get()/100
            newImage=np.copy(self.current_RGB)
            if self.gini_map is not None and self.softmax_map is not None:
                newImage[np.where(self.gini_map<gini)]=[0,0,0]
                newImage[np.where(self.softmax_map<softmax)]=[0,0,0]
            im=Image.fromarray(newImage.astype('uint8'), 'RGB')
            self.image = self.axes.imshow(im, interpolation='none')
            self.save_RGB = im
        # draw figure
        self.interactive_prediciton = FigureCanvasTkAgg(self.prediction_graph, master=self.root)
        self.interactive_prediciton.draw()
        self.interactive_prediciton.get_tk_widget().grid(column=3, row=6, columnspan=3, rowspan=2, ipady=5, ipadx=0,
                                                        pady=0)
        self.interactive_prediciton.get_tk_widget().bind('<Motion> ', self._build_pixel_value)
        self.interactive_prediciton.get_tk_widget().bind('<Button-2>', self.__pop_up_prediction)
        self.accuracy=self.__calc_accuracy()
        self._build_accuracy()
        
    def _build_RGB_graph(self, event=None):
        # create canvas
        print("Building")
        self.RGB_graph = Figure(figsize=(6, 4))
        self.axes = self.RGB_graph.add_subplot(111)
        self.axes.set_aspect(2/3)
        self.RGB_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        self.axes.get_yaxis().set_visible(False)
        self.axes.get_xaxis().set_visible(False)
        if self.RGB is not None:
            im=Image.fromarray(self.RGB.astype('uint8'), 'RGB')
            self.image = self.axes.imshow(im, interpolation='none')
        # draw figure
        self.interactive_RGB = FigureCanvasTkAgg(self.RGB_graph, master=self.root)
        self.interactive_RGB.draw()
        self.interactive_RGB.get_tk_widget().grid(column=0, row=6, columnspan=3, rowspan=2, ipady=5, ipadx=0,
                                                        pady=0)
        self.interactive_RGB.get_tk_widget().bind('<Button-2>', self.__pop_up_RGB)
        
    def _build_curve_graph(self):
        self.interactive_absorption_spec_graph = Figure(figsize=(4, 3))
        self.axes_abs = self.interactive_absorption_spec_graph.add_subplot(111)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        # plot absorption spec
        y_low = self.y_low
        y_high = self.y_high
        if self.absorption_spec is not None:
            if self.gradient == "og":
                y_vals = self.absorption_spec
            elif self.gradient == "first":
                y_vals = self.absorption_spec_gradient1
            elif self.gradient == "second":
                y_vals = self.absorption_spec_gradient2
            self.axes_abs.plot(self.x_vals, y_vals, '-', lw=0.5)
            self.axes_abs.grid(linestyle=':', linewidth=0.5)
        if y_low is not None and y_high is not None:
            factor = (y_high - y_low) * 0.05
            y_low -= factor
            y_high += factor
        self.interactive_absorption_spec_graph.set_tight_layout(True)
        #self.axes_abs.set_xlim(left=0, right=1000)
        self.axes_abs.set_ylim(bottom=self.y_low, top=self.y_high)
        # commas and non-scientific notation
        self.axes_abs.ticklabel_format(style='plain')
        self.axes_abs.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
        self.axes_abs.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=7, row=7, columnspan=6, rowspan=1, ipady=5,
                                                              ipadx=0)
        
    @staticmethod
    def format_axis(x, _):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 4))

    # ------------------------------------------------- CALCULATORS --------------------------------------------------
        
    def _draw_prediction(self, prediction, x, y):
      prediction=np.reshape(prediction, (x, y, prediction.shape[1]))
      predictedClasses=np.argmax(prediction, axis=2) #array of shape [rows, columns]
      emptyX=np.where(np.sum(prediction, axis=2)==0)[0]#If all classes are 0, argmax returns 0 for the corresponding pixel. However, 0 also means background (foil, color: gray). Therfore, we get Coordinates of all pixels having 0 for all classes and set them all to black afterwards, to distinguish them from background.
      emptyY=np.where(np.sum(prediction, axis=2)==0)[1]
      imageArray=np.zeros((predictedClasses.shape[0], predictedClasses.shape[1],3)) # array of shape [rows, columns, colorChannels]
      for jj in range(prediction.shape[2]):#For each class (organ)...
          if(jj==0):
              color=self.colors[0] #...pick a RGB-Value; i.e. Gray
          elif(jj==1):
              color=self.colors[1]
          elif(jj==2): 
              color=self.colors[2]                   
          elif(jj==3):
              color=self.colors[3]
          elif(jj==4):
              color=self.colors[4]
          elif(jj==5):
              color=self.colors[5]
          elif(jj==6):
              color=self.colors[6]
          elif(jj==7):
              color=self.colors[7]
          elif(jj==8): 
              color=self.colors[8]
          elif(jj==9):    
              color=self.colors[9]
          elif(jj==10):
              color=self.colors[10]
          elif(jj==11):
              color=self.colors[11]
          elif(jj==12):
              color=self.colors[12]
          elif(jj==13):
              color=self.colors[13]
          elif(jj==14):
              color=self.colors[14]
          elif(jj==15):
              color=self.colors[15]
          elif(jj==16):
              color=self.colors[16]
          elif(jj==17):
              color=self.colors[17]
          elif(jj==18):
              color=self.colors[18]
          elif(jj==19):
              color=self.colors[19]
          elif(jj==20):
              color=self.colors[20]
          elif(jj==21):
              color=self.colors[21]
          elif(jj==22):
              color=self.colors[22]
          elif(jj==23):
              color=self.colors[23]
          x=np.where(predictedClasses==jj)[0] #... and set the color of all pixels predicted as the corresponding class (organ) to this RGB-Value.
          y=np.where(predictedClasses==jj)[1]
          imageArray[x,y,:]=color
      imageArray[emptyX,emptyY,:]=(0,0,0) #Disinguish between "background" (gray) and none; set none black
      return imageArray
    
    def _giniMap(self, pred): 
        giniMap=np.zeros((pred.shape[0], pred.shape[1]))
        row=np.arange(pred.shape[0])
        column=np.arange(pred.shape[1])
        pred = np.sort(pred, axis=2) #values must be sorted
        n = pred.shape[2]#number of array elements
        width=1/n
        x=np.arange(0,1,width)
        pred=np.cumsum(pred, axis=2)
        AUC = np.trapz(pred, axis=2, dx=width)
        ABC = 0.5-AUC
        giniMap = ABC*2
        return giniMap

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------
 
    def __calc_accuracy(self, thresh = True):
        if self.prediction_map is not None and self.ground_truth_map is not None:
            
            if thresh:
                gini = self.gini_slider.get()/100
                softmax = self.softmax_slider.get()/100
            else:
                gini = 0
                softmax =0
            
            flatPred = self.prediction_map.reshape(480*640, self.prediction_map.shape[2])
            
            visibleGT = np.copy(self.ground_truth_map)
            visibleGT[np.where(self.gini_map<gini)[0], np.where(self.gini_map<gini)[1],0] = 1
            visibleGT[np.where(self.softmax_map<softmax)[0], np.where(self.softmax_map<softmax)[1],0] = 1
            flatGT = visibleGT.reshape(480*640, visibleGT.shape[2])
            weights = flatGT[...,0]==0
            weights[np.where(np.sum(flatPred, axis=1)==0)] = False
            maxPixels=np.sum(weights)#Number of unambigiously-labeld Pixels
            if(maxPixels!=0):
                accuracy=np.sum(np.multiply((np.argmax(flatPred, axis=1)==np.argmax(flatGT, axis=1)),weights))/maxPixels
            else:
                accuracy=0
            return accuracy
        else:
            return None
        
    
    def __flat(self, X): 
        X = np.reshape(X, (X.shape[0]*X.shape[1], X.shape[2]))
        return X
        
    def __get_path_to_dir(self, title):  
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askopenfilename(parent=self.root, title=title, initialdir=p, filetypes=[("H5-File", "*.h5")])
        else:
            path = filedialog.askopenfilename(parent=self.root, title=title, filetypes=[("H5-File", "*.h5")])
        return path
    
    def __get_path_to_dir2(self, title):  
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path
    
    def __info(self): 
        info = self.listener.modules[INFO].predic_info
        title = "Prediction Information"
        make_info(title=title, info=info)
        
    def __soft_info(self):
        info = self.listener.modules[INFO].soft_info
        title = "Max of Softmax Information"
        make_info(title=title, info=info)
        
    def __gini_info(self):
        info = self.listener.modules[INFO].gini_info
        title = "Gini Information"
        make_info(title=title, info=info)
    
    def __load_model(self, path):   
        self.model=load_model(path)
        self.edge_length=self.model.input.shape[2]
        self.__update_data()
        self.select_model_button['text'] = os.path.basename(os.path.normpath(path))
    
    def __select_model(self):       
        dc_dir_path = self.__get_path_to_dir("Please select a .h5 file")
        self.__load_model(dc_dir_path)
        
    def __select_gt_folder(self): 
        self.gt_dir = self.__get_path_to_dir2("Please select a directory")
        self.__update_data()

    def __update_data(self): 
        if self.model is not None and self.listener.data_cube is not None:
            self.output_path = os.path.dirname(self.listener.dc_path) + "/_hypergui"
            X  = np.rot90(self.listener.data_cube) 
            X = gaussian_filter(X, (5,5,1))
            imageArrayPred = np.zeros((480, 640, 3))
            pred = np.zeros((480, 640, self.model.output.shape[2]))
            for ii in range(((int)(480/self.edge_length))):
                yMin=ii*self.edge_length
                yMax=yMin+self.edge_length
                for jj in range(((int)(640/self.edge_length))):
                    xMin=jj*self.edge_length
                    xMax=xMin+self.edge_length
                    xChunk=X[yMin:yMax, xMin:xMax,:]
                    xChunk=xChunk[None]
                    predChunk=self.model.predict(xChunk)
                    pred[yMin:yMax, xMin:xMax,:]=np.reshape(predChunk, (self.edge_length, self.edge_length, self.model.output.shape[2]))
                    imageArrayPred[yMin:yMax, xMin:xMax,:]=self._draw_prediction(predChunk[0], self.edge_length, self.edge_length)
            if jj*self.edge_length<640:
                x_vis = 640-(jj*self.edge_length)
                xMin = 640-self.edge_length
                xMax = 640
                for ii in range(((int)(480/self.edge_length))):
                    yMin=ii*self.edge_length
                    yMax=yMin+self.edge_length
                    xChunk=X[yMin:yMax, xMin:xMax,:]
                    xChunk=xChunk[None]
                    predChunk=self.model.predict(xChunk)
                    pred[yMin:yMax, xMin:xMax,:]=np.reshape(predChunk, (self.edge_length, self.edge_length, self.model.output.shape[2]))
                    imageArrayPred[yMin:yMax, xMin:xMax,:]=self._draw_prediction(predChunk[0], self.edge_length, self.edge_length)
            self.prediction_map = pred
            self.prediction_RGB = Image.fromarray(imageArrayPred.astype('uint8'), 'RGB')
            self.gini_map = self._giniMap(pred)
            self.gini_RGB = Image.fromarray((np.moveaxis(np.tile(self.gini_map,(3,1,1)),0,-1)*255).astype('uint8'),'RGB')
            self.softmax_map = np.max(pred, axis=2)
            self.softmax_RGB = Image.fromarray((np.moveaxis(np.tile(self.softmax_map,(3,1,1)),0,-1)*255).astype('uint8'),'RGB')
            self.current_RGB = self.prediction_RGB
            self.avGini=np.mean(self.gini_map) 
            self.avSm=np.mean(self.softmax_map) 
            self.sdGini=np.std(self.gini_map) 
            self.sdSm=np.std(self.softmax_map)
            if self.gt_dir is not None:
                string = self.listener.dc_path.split("/")[-2]
                files = glob.glob(self.gt_dir+"/"+string+"_Y.npy")
                if len(files)==1:
                    file=files[0]
                    Y  = np.load(file)
                    self.ground_truth_map = Y
                    self.ground_truth_RGB=self._draw_prediction(self.__flat(Y), 480, 640)
                else:
                    self.ground_truth_RGB = np.zeros((480, 640, 3))   
                    self.ground_truth_map = np.zeros((480, 640, self.model.output.shape[2])) 
            else:
                self.ground_truth_RGB = np.zeros((480, 640, 3))   
                self.ground_truth_map = np.zeros((480, 640, self.model.output.shape[2]))     
            self._build_stats()
            self.update_prediction()
        
    def __change_mode(self, event): 
        choice = self.drop_down_var.get()[:2]
        if choice == '1.':
            self.current_RGB = self.prediction_RGB
        elif choice == '2.':
            self.current_RGB = self.ground_truth_RGB
        elif choice == '3.':
            self.current_RGB = self.RGB
        elif choice == '4.':
            self.current_RGB = self.gini_RGB
        elif choice == '5.':
            self.current_RGB = self.softmax_RGB
        self.update_prediction()
        
    def __change_leg_selection(self, event): 
        choice = self.drop_down_legVar.get()
        self.leg_selection = self.organMaskNames.index(choice) 
        
    def __update_preview(self, event=None):
        a = self.slider_r.get()/100
        b= self.slider_b.get()/100
        c = self.slider_g.get()/100
        self.prevAx.set_facecolor((a, b, c))
        self.prev_canvas.draw()
        self.prev_canvas.get_tk_widget().grid(column=11, row=4, columnspan=1, rowspan=1, ipady=0, ipadx=0,
                                                        pady=0)

    def __pop_up_prediction(self, event):
        w, i, ax= make_popup_image_external(self.prediction_graph, graphsize=(16, 16))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
        
    def __pop_up_RGB(self, event):        
        w, i, ax= make_popup_image_external(self.RGB_graph, graphsize=(16, 16))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
    
    def __set_color(self):
        a = self.slider_r.get()/100
        b= self.slider_b.get()/100
        c = self.slider_g.get()/100
        code = (int(255*a), int(255*b), int(255*c))
        self.colors[self.leg_selection] = code
        self._build_legend()
        self.__update_data()
        self.__update_preview()
        self.__reset_color_slider()

    def __reset(self):
        self.gini_slider.set(0)
        self.softmax_slider.set(0)
        self._build_prediction_graph()
        
    def __reset_color_slider(self):
        self.slider_r.set(0)
        self.slider_b.set(0)
        self.slider_g.set(0)
        
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)
    
    def __get_naming_info(self):
        model = self.select_model_button['text'][0:-3]
        mode = self.drop_down_var.get()[3::]
        gini = self.gini_slider.get()/100
        sm = self.softmax_slider.get()/100
        return "_prediction_" + mode + "_gini_thresh_" + str(gini) + "_softmax_thresh_" + str(sm) + "_model_" + model
        
    def __save_RGB(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate a prediction to save.")
        else:
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            output_path = self.output_path + "/" + self.__get_naming_info() + '.png'
            logging.debug("SAVING IMAGE" + output_path)
            plt.clf()
            axes = plt.subplot(111)
            axes.imshow(self.save_RGB)
            axes.get_yaxis().set_visible(False)
            axes.get_xaxis().set_visible(False)
            axes.axis('off')
            DPI = plt.gcf().get_dpi()
            plt.gca().set_position([0, 0, 1, 1])
            plt.gca().patch.set_visible(False)
            plt.gcf().patch.set_visible(False)
            plt.gcf().set_size_inches(640.0/float(DPI),480.0/float(DPI))
            plt.savefig(output_path)
            plt.clf()
            
    def __set_der(self, event = None):
        choice = self.drop_down_var2.get()[0]
        if choice == '0':
            self.gradient = "og"
        elif choice == '1':
            self.gradient = "first"
        elif choice == '2':
            self.gradient = "second"
        self.update_prediction()
        
            
    def __save_RGB_with_legend(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate a prediction to save.")
        else:
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            output_path = self.output_path + "/" + self.__get_naming_info() + '_with_legend.png'
            logging.debug("SAVING IMAGE" + output_path)
            plt.clf()
            axes = plt.subplot(1,2,1)
            axes_legend = plt.subplot(1,2,2)
            axes_legend.legend(handles=self.legend_elements, loc='center left', prop={'size': 14}) 
            axes_legend.axis('off') 
            axes.imshow(self.save_RGB)
            axes.get_yaxis().set_visible(False)
            axes.get_xaxis().set_visible(False)
            
            axes.set_position([0, 0, 2/3, 1])
            axes_legend.set_position([2/3, 0, 1 , 1])
            axes.axis('off')
            axes_legend.axis('off')
            axes.patch.set_visible(False)
            axes_legend.patch.set_visible(False)
            
            plt.gcf().patch.set_visible(False)
            
            fig = plt.gcf()
            DPI = fig.get_dpi()
            fig.set_size_inches(640.0/float(DPI) + 320.0/float(DPI), 480.0/float(DPI))
            plt.savefig(output_path)
            plt.clf()
    
    def __save_CSV(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate an optical spectrum to save.")
        else:
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            outputs = np.array([])
            cap = np.array([])
            if self.gt_dir is not None:
                th_accuracy = self.accuracy
                unth_accuracy = self.__calc_accuracy(False)
            else:
                th_accuracy = None
                unth_accuracy = None
            ii = 1
            for organ in self.organMaskNames[1::]:
                totalPx = np.sum(np.sum(self.prediction_map, axis = 2)!=0)
                organPx = np.sum(np.argmax(self.prediction_map, axis = 2)==ii)
                perc = organPx / totalPx
                cap = np.append(cap, str(organ))
                c_name = os.path.basename(os.path.normpath(self.listener.dc_path))[0:19]
                output_path = self.output_path + "/_prediction_" + self.select_model_button['text'][0:-3] + "_on_" + c_name + ".xlsx"
                outputs = np.append(outputs, perc)
                ii=ii+1
            xl = self.__excel_list(cap, outputs, unth_accuracy, th_accuracy, output_path)
    
    def __excel_list(self, array_one, array_two, unthrsh_ac, thrsh_ac, output_path):
        workbook = xlsxwriter.Workbook(output_path)
        row = 0
        col = 0
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 1, 3)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 3)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 3)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 3)
        worksheet.set_column(7, 7, 20)
        worksheet.write(0, 1, 'Organ', bold)
        worksheet.write(0, 3, 'Fraction', bold)
        worksheet.write(0, 5, 'Unthresholded Accuracy', bold)
        worksheet.write(0, 7, 'Thresholded Accuracy', bold)    
        row += 1       
        for idx, i in enumerate(array_one):
            worksheet.write(row + 1, col + 1, i)
            worksheet.write(row + 1, col + 3, array_two[idx])
            row += 1 
        worksheet.write(row + 1, col + 5, unthrsh_ac)
        worksheet.write(row + 1, col + 7, thrsh_ac)
        workbook.close()
    
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)

    def __update_upper_lower(self, event):
        self.y_low = float(self.lower_input.get())
        self.y_high = float(self.upper_input.get())
        self._build_curve_graph()