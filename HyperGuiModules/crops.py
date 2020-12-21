#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import logging
import csv
import os
import glob
import math


class crops:
    def __init__(self, crops_frame, listener):
        self.root = crops_frame

        # Listener
        self.listener = listener
        self.add_pt_bool = True

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        
        self.save_tif_bool = False


        self.data_cube_paths = []
        self.data_cube_path_label = None
        self.path_label = None

        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.active_image = "RGB"

        self.save_label = None
        self.automatic_names = True


        self.all_points_remove = None


        self.instant_save_button = None
        self.input_coords_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False
        self.tif_save_path_end = None
        self.current_dc_path = None
        
        self.mouse_x = 320
        self.mouse_y = 240
        self.view_mid = [240, 320]
        
        self.input_pt_title_list = [None for ii in range(100)] 
        self.input_pt_title_x_list = [None for ii in range(100)] 
        self.input_pt_title_y_list = [None for ii in range(100)] 
        self.input_pt_x_list = [None for ii in range(100)]  
        self.input_pt_y_list = [None for ii in range(100)]  
        
        self.save_as_tif_checkbox_value = IntVar()
        


        # coords in dimensions of image, i.e. xrange=[1, 640], yrange=[1, 480]
        self.coords_list = [(None, None) for _ in range(100)]
        self.mask_raw = None

        self._init_widget()

        self.rgb_button.config(foreground="red")
        self.zoom_factor = 1

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.selection_listbox.curselection()[0]
        else: 
            index = self.current_dc_path
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data)
        self._draw_points()
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_instant_save_button()
        self._build_original_image(self.original_image_data)
        self._build_select_superdir_button()
        self._build_select_all_subfolders_button()
        self._build_selection_box()
        self._build_trash_button()

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=0, column=1,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=0, column=2,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=0, column=3,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=0, column=4,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=0, column=5,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_tli(self):
        self.tli_button = make_button(self.root, text='TLI', width=3, command=self.__update_to_tli, row=0, column=6,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_ohi(self):
        self.ohi_button = make_button(self.root, text='OHI', width=3, command=self.__update_to_ohi, row=0, column=7,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------


    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save crops for\nselected Folders', width=12, command=self.__save_crops,
                                               row=26, column=3, columnspan=2, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_trash_button(self):
        self.trash_button = make_button(self.root, text='Clean List', width=9, command=self.__trash_list,
                                               row=26, column=1, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 1, column=0, width=11, outer_pady=(5, 5))
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=26, rowspan=1, column=0, width=11, outer_pady=(5, 5))



    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=0, rowspan=24, padx=(0, 15), pady=(0, 15), height = 35)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------

    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=1, column=1, rowspan=25,
                                             columnspan=8, inner_pady=300, inner_padx=400, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            #data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=1, column=1, columnspan=8, rowspan=25, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=7, figwidth=9)
            self.original_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
            self.original_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
            if self.pop_up:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            
    def __zoom(self, event):
        if self.zoom_factor < 16:
            self.zoom_factor = 2*self.zoom_factor
            self.view_mid[0] = round(self.view_mid[0] + self.mouse_y-240)*2
            self.view_mid[1] = round(self.view_mid[1] + self.mouse_x-320)*2
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480 - 240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()
        
        
    def __dezoom(self, event):
        if self.zoom_factor > 1:
            self.zoom_factor = round(0.5*self.zoom_factor)
            self.view_mid[0] = round((self.view_mid[0] + self.mouse_y-240)*0.5)
            self.view_mid[1] = round((self.view_mid[1] + self.mouse_x-320)*0.5)
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480-240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()
        
        
        
    def __update_mouse_position(self, event):
        pos = self.original_image_graph.axes[0].get_position()
        axesX0 = pos.x0
        axesY0 = pos.y0
        axesX1 = pos.x1
        axesY1 = pos.y1
        canvas = event.widget
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.canvasx
        cx = canvas.winfo_rootx()
        cy = canvas.winfo_rooty()
        minX=width*axesX0
        maxX=width*axesX1
        minY=height*axesY0
        maxY=height*axesY1
        axWidth=maxX-minX
        conversionFactor = 640/axWidth
        Xc=int((event.x-minX)*conversionFactor)
        Yc=int((event.y-minY)*conversionFactor)
        if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
            self.mouse_x = Xc
            self.mouse_y = Yc
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def _draw_points(self):
        copy_data = self.original_image_data.copy()
        if self.add_pt_bool:
            not_none = []
        else:
            not_none = [self.start_choord,(self.start_choord[0], self.end_choord[1]), self.end_choord, (self.end_choord[0], self.start_choord[1])]
        for point in not_none:
            y = int(point[0])
            x = int(point[1])
            for xi in range(-4, 5):
                copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
            for yi in range(-4, 5):
                copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
            idx = not_none.index(point)
            self._draw_a_line(not_none[idx - 1], not_none[idx], copy_data)
           
        left = self.view_mid[1] - 320
        bottom = self.view_mid[0] - 240
        right = left + 640
        top = bottom + 480
        im = Image.fromarray(copy_data)
        im = im.resize((640*self.zoom_factor, 480*self.zoom_factor)) 
        im = im.crop((left, bottom, right, top))
        self._build_original_image(np.array(im))
        
    @staticmethod
    def _draw_a_line(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(113 * val[i]), int(255 * val[i]), int(66 * val[i]))
        return image

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __save_coords(self):
        path = os.path.dirname(self.get_selected_data_cube_path())
        output_path1 = path + "/"+self.listener.output_folder_hypergui+"/mask" + '.csv'
        output_path2 = path + "/"+self.listener.output_folder_hypergui+"/MASK_COORDINATES" + '.csv'
        if os.path.exists(output_path1) or os.path.exists(output_path2):
            yn = messagebox.askquestion ('Verify','Are you sure you want to override mask.csv and MASK_CORDINATES.csv?',icon = 'warning')
            if yn == "yes":
                self.__save_points()
                self.__save_mask()
                self.__save_tif(False)
        else:
            self.__save_points()
            self.__save_mask()
            self.__save_tif(False)
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')

    def __get_coords(self, event):
        if not self.pop_up:
            #x = int((eventorigin.x - 30) * 640 / 296)
            #y = int((eventorigin.y - 18) * 480 / 221)
            #if 0 <= x < 640 and 0 <= y < 480:
            #    self.__add_pt((x, y))
            pos = self.original_image_graph.axes[0].get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            canvas.canvasx
            cx = canvas.winfo_rootx()
            cy = canvas.winfo_rooty()
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            
            Xc = round((self.view_mid[1]+Xc-320)/self.zoom_factor)
            Yc = round((self.view_mid[0]+Yc-240)/self.zoom_factor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
                self.__add_pt((Xc, Yc))

        else:
            x = int((eventorigin.x - 17) * 640 / 770)
            y = int((eventorigin.y - 114) * 480 / 578)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))


    def __add_pt(self, pt):
        if self.add_pt_bool:
            self.start_choord = pt
            self._draw_points()
        else:
            self.end_choord = pt
            self._draw_points()
        self.add_pt_bool = not self.add_pt_bool

    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------

    def __update_to_rgb(self):
        self.active_image = "RGB"
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.RGB)

    def __update_to_sto2(self):
        self.active_image = "STO2"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.STO2)

    def __update_to_nir(self):
        self.active_image = "NIR"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.NIR)

    def __update_to_thi(self):
        self.active_image = "THI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.THI)

    def __update_to_twi(self):
        self.active_image = "TWI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TWI)
        
    def __update_to_tli(self):
        self.active_image = "TLI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="red")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TLI)
        
    def __update_to_ohi(self):
        self.active_image = "OHI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="red")
        self.update_original_image(self.OHI)
      
    def __pop_up_image(self, event=None):
        (self.pop_up_window, self.pop_up_image) = make_popup_image(self.original_image_graph, interactive=True)
        self.pop_up = True
        self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
        self.pop_up_window.protocol("WM_DELETE_WINDOW", func=self.__close_pop_up)
        self.pop_up_window.attributes("-topmost", True)

    def __close_pop_up(self):
        self.pop_up = False
        self.pop_up_window.destroy()


    # ------------------------------------------------- INPUT POP-UP --------------------------------------------------

    def __input_info(self):
        info = self.listener.modules[INFO].input_info
        title = "Coordinate Input Information"
        make_info(title=title, info=info)


    def __update_selected_data_cube(self, event):
        dc_path = self.get_selected_data_cube_path()[0:-12]
        if self.current_dc_path is not self.selection_listbox.curselection()[0]:
            if len(self.selection_listbox.curselection())>0:
                self.current_dc_path = self.selection_listbox.curselection()[0]
            self._update_tif_save_path()
        
        a = Image.open(dc_path +"RGB-Image.png")
        a = np.asarray(a)
        a = a[30:510, 3:643, :3]
        self.RGB = a
        
        b = Image.open(dc_path +"NIR-Perfusion.png")
        b = np.asarray(b)
        b = b[26:506, 4:644, :3]
        self.NIR = b
        
        c = Image.open(dc_path +"TWI.png")
        c = np.asarray(c)
        c = c[26:506, 4:644, :3]
        self.TWI = c
        
        d = Image.open(dc_path +"THI.png")
        d = np.asarray(d)
        d = d[26:506, 4:644, :3]
        self.THI = d
        
        e = Image.open(dc_path +"Oxygenation.png")
        e = np.asarray(e)
        e = e[26:506, 4:644, :3]
        self.STO2 = e
        
        f = Image.open(dc_path +"TLI.png")
        f = np.asarray(f)
        f = f[26:506, 4:644, :3]
        self.TLI = f
        
        g = Image.open(dc_path +"OHI.png")
        g = np.asarray(g)
        g = g[26:506, 4:644, :3]
        self.OHI = g
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
        

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            self.__add_data_cube(sub_dir)
    
    def __add_data_cube_subdirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the OP folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            self.__add_data_cube(sub_dir)


    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if ".dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_cube_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                # Add the new data to current class
                self.data_cube_paths.append(dc_path)

                # Display the data cube
                concat_path = os.path.basename(os.path.normpath(dc_path))
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=18)

    def __get_path_to_dir(self, title):
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path


    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False):
        #contents = os.listdir(path_to_main_folder)
        # Adds the path to the main folder in front for traversal
        #sub_folders = [path_to_main_folder + "/" + i for i in contents if bool(re.match('[\d/-_]+$', i))]
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/", recursive = recursive))
        return sub_folders
        
    def __save_mask(self):
        polygon = [point for point in self.coords_list if point != (None, None)]
        if len(polygon)>0:
            img = Image.new('L', (640, 480), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
            mask_array = np.array(img)
            path = os.path.dirname(self.get_selected_data_cube_path())
            if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                os.mkdir(path + '/'+self.listener.output_folder_hypergui)
            output_path = path + '/'+self.listener.output_folder_hypergui + "/mask" + '.csv'
            np.savetxt(output_path, mask_array, delimiter=",", fmt="%d")
        else:
            pass
        
    def __save_points(self):
        data = self.__get_coords_list()
        if len(data)>0:
            path = os.path.dirname(self.get_selected_data_cube_path())
            if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                os.mkdir(path + '/'+self.listener.output_folder_hypergui)
            output_path = path + '/'+self.listener.output_folder_hypergui + "/MASK_COORDINATES" + '.csv'
            np.savetxt(output_path, data, delimiter=",", fmt="%1.2f")
        else:
            pass
        
    def __get_coords_list(self):
        point_coords = self.coords_list
        data = [[float(point_coords[i][0] + 1), float(point_coords[i][1] + 1)] for i in range(100) if
                point_coords[i] != (None, None)]
        return data
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self.coords_list = [(None, None) for _ in range(100)]
        self.__remove_pt('all')
        
    def __input_info(self):
        info = self.listener.modules[INFO].input_info
        title = "Coordinate Input Information"
        make_info(title=title, info=info)
        
    def __input_coords(self):
        self.coords_window = Toplevel()
        self.coords_window.geometry("+0+0")
        self.coords_window.configure(bg=tkcolour_from_rgb(BACKGROUND))

        # title
        self.input_points_title = make_label_button(self.coords_window, text='Coordinate Input',
                                                    command=self.__input_info, width=14)
        self.input_points_title.grid(columnspan=3)

        # points
        for ii in range(100):
            self.input_pt_title_list[ii], self.input_pt_title_x_list[ii], self.input_pt_title_y_list[ii], self.input_pt_x_list[ii], self.input_pt_y_list[ii] = \
                self.__input_coord_n(ii)

        # go button
        self.go_button = make_button(self.coords_window, text='Go', width=2, command=self.__use_inputted_coords, row=21,
                                     column=3, columnspan=5, inner_pady=5, outer_padx=(15, 15), outer_pady=(7, 15))
        self.all_remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n('all'),
                                         row=0, column=5, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                         highlightthickness=0)
        
    def __input_coord_n(self, num):
        rom = num % 20
        col = math.floor(num/20)*6
        title = make_text(self.coords_window, content="Pt " + str(num) + ': ', bg=tkcolour_from_rgb(BACKGROUND),
                          column=col+0, row=rom + 1, width=6, pady=(0, 3), padx=(15, 0))
        title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+1, row=rom + 1,
                            width=4, pady=(0, 3))
        title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+3, row=rom + 1,
                            width=4, pady=(0, 3), padx=(5, 0))
        input_x = make_entry(self.coords_window, row=rom + 1, column=col+2, width=5, columnspan=1, pady=(0, 3))
        input_y = make_entry(self.coords_window, row=rom + 1, column=col+4, width=5, columnspan=1, padx=(0, 15),
                             pady=(0, 3))
        if self.coords_list[num] != (None, None):
            input_x.insert(END, str(self.coords_list[num][0] + 1))
            input_y.insert(END, str(self.coords_list[num][1] + 1))
            
        remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n(num + 1), row=rom +1,
                         column=col+5, highlightthickness=0)
        return title, title_x, title_y, input_x, input_y
    
    def __use_inputted_coords(self):
        coords = []
        for ii in range(100):
            coords.append([self.input_pt_x_list[ii].get(), self.input_pt_y_list[ii].get()])
        coords = [(int(i[0]) - 1, int(i[1]) - 1) for i in coords if i[0] != '' and i[1] != '']
        if len(coords) > 0:
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            if min(xs) >= 0 and max(xs) < 640 and min(ys) >= 0 and max(ys) < 480:
                coords = coords + [(None,None) for ii in range(100-len(coords))]
                self.coords_list = coords
                self._build_points()
                self._draw_points()
            else:
                messagebox.showerror("Error", "x values must be on the interval [1, 640] and y values must be on the "
                                              "interval \n[1, 480].")
        self.coords_window.destroy()
            
    def __save_crops(self):
        if self.add_pt_bool:
            for folder in self.selection_listbox.curselection():
                self.__save_crop(folder)
    
    def __save_crop(self, folder):
        path = os.path.dirname(self.data_cube_paths[folder])+"/_hypergui_crops"
        if not os.path.exists(path):
            os.mkdir(path)
        lr = (self.start_choord[0], self.end_choord[0])
        up = (self.start_choord[1], self.end_choord[1])
        RGB = Image.fromarray(self.RGB).crop((min(lr), min(up), max(lr), max(up)))
        THI = Image.fromarray(self.THI).crop((min(lr), min(up), max(lr), max(up)))
        TWI = Image.fromarray(self.TWI).crop((min(lr), min(up), max(lr), max(up)))
        NIR = Image.fromarray(self.NIR).crop((min(lr), min(up), max(lr), max(up)))
        STO2 = Image.fromarray(self.STO2).crop((min(lr), min(up), max(lr), max(up)))
        RGB.save(path+"/RGB.png")
        THI.save(path+"/THI.png")
        TWI.save(path+"/TWI.png")
        NIR.save(path+"/NIR.png")
        STO2.save(path+"/STO2.png")
            
        #polygon = [point for point in self.coords_list if point != (None, None)]
        #    if len(polygon) >= 2:
        #        self._update_tif_save_path()
        #        path = os.path.dirname(self.get_selected_data_cube_path())
        #        if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
        #            os.mkdir(path + '/'+self.listener.output_folder_hypergui)
        #        img = Image.new('L', (640, 480), 0)
        #        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
         #       output_path = self.tif_save_path
         #       mask_img = Image.fromarray(((np.array(img)*-1+1)*255).astype("uint8"), 'L')
         ##       mask_img.save(output_path)
         #   else:
          #      print("Draw a mask to save TIF.")
               
    
        
                            
        