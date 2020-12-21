from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import logging
import csv
import os


class OGColour:
    def __init__(self, original_color_frame, listener):
        self.root = original_color_frame

        # Listener
        self.listener = listener

        self.rgb_button = None
        self.rgb_checkbox = None
        self.rgb_checkbox_value = IntVar()

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = IntVar()

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value = IntVar()

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value = IntVar()

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value = IntVar()

        self.gs = False
        self.gs_dropdown = None
        self.gs_var = StringVar()
        self.gs_choices = ['CS (Colour Scale)', 'GS (Grey Scale)']

        self.mask_to_csv_button = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()

        self.pt1_label = None
        self.pt1_remove = None
        self.pt1_checkbox = None
        self.pt1_checkbox_value = IntVar()

        self.pt2_label = None
        self.pt2_remove = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = IntVar()

        self.pt3_label = None
        self.pt3_remove = None
        self.pt3_checkbox = None
        self.pt3_checkbox_value = IntVar()

        self.pt4_label = None
        self.pt4_remove = None
        self.pt4_checkbox = None
        self.pt4_checkbox_value = IntVar()

        self.pt5_label = None
        self.pt5_remove = None
        self.pt5_checkbox = None
        self.pt5_checkbox_value = IntVar()

        self.pt6_label = None
        self.pt6_remove = None
        self.pt6_checkbox = None
        self.pt6_checkbox_value = IntVar()

        self.pt7_label = None
        self.pt7_remove = None
        self.pt7_checkbox = None
        self.pt7_checkbox_value = IntVar()

        self.pt8_label = None
        self.pt8_remove = None
        self.pt8_checkbox = None
        self.pt8_checkbox_value = IntVar()

        self.pt9_label = None
        self.pt9_remove = None
        self.pt9_checkbox = None
        self.pt9_checkbox_value = IntVar()

        self.pt10_label = None
        self.pt10_remove = None
        self.pt10_checkbox = None
        self.pt10_checkbox_value = IntVar()

        self.all_points_remove = None
        self.all_points_checkbox = None
        self.all_points_checkbox_value = IntVar()

        self.use_mask_button = None
        self.instant_save_button = None
        self.input_coords_button = None
        self.upload_mask_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.input_pt1_title = None
        self.input_pt1_title_x = None
        self.input_pt1_x = None
        self.input_pt1_title_y = None
        self.input_pt1_y = None

        self.input_pt2_title = None
        self.input_pt2_title_x = None
        self.input_pt2_x = None
        self.input_pt2_title_y = None
        self.input_pt2_y = None

        self.input_pt3_title = None
        self.input_pt3_title_x = None
        self.input_pt3_x = None
        self.input_pt3_title_y = None
        self.input_pt3_y = None

        self.input_pt4_title = None
        self.input_pt4_title_x = None
        self.input_pt4_x = None
        self.input_pt4_title_y = None
        self.input_pt4_y = None

        self.input_pt5_title = None
        self.input_pt5_title_x = None
        self.input_pt5_x = None
        self.input_pt5_title_y = None
        self.input_pt5_y = None

        self.input_pt6_title = None
        self.input_pt6_title_x = None
        self.input_pt6_x = None
        self.input_pt6_title_y = None
        self.input_pt6_y = None

        self.input_pt7_title = None
        self.input_pt7_title_x = None
        self.input_pt7_x = None
        self.input_pt7_title_y = None
        self.input_pt7_y = None

        self.input_pt8_title = None
        self.input_pt8_title_x = None
        self.input_pt8_x = None
        self.input_pt8_title_y = None
        self.input_pt8_y = None

        self.input_pt9_title = None
        self.input_pt9_title_x = None
        self.input_pt9_x = None
        self.input_pt9_title_y = None
        self.input_pt9_y = None

        self.input_pt10_title = None
        self.input_pt10_title_x = None
        self.input_pt10_x = None
        self.input_pt10_title_y = None
        self.input_pt10_y = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False

        self.info_label = None

        # coords in dimensions of image, i.e. xrange=[1, 640], yrange=[1, 480]
        self.coords_list = [(None, None) for _ in range(10)]
        self.mask_raw = None

        self._init_widget()

        self.displayed_image_mode = RGB  # RGB by default
        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._draw_points()

    def get_bools(self):
        return [self.get_pt1_checkbox_value(), self.get_pt2_checkbox_value(), self.get_pt3_checkbox_value(),
                self.get_pt4_checkbox_value(), self.get_pt5_checkbox_value(), self.get_pt6_checkbox_value(),
                self.get_pt7_checkbox_value(), self.get_pt8_checkbox_value(), self.get_pt9_checkbox_value(),
                self.get_pt10_checkbox_value()]

    def get_pt1_checkbox_value(self):
        return not bool(self.pt1_checkbox_value.get())

    def get_pt2_checkbox_value(self):
        return not bool(self.pt2_checkbox_value.get())

    def get_pt3_checkbox_value(self):
        return not bool(self.pt3_checkbox_value.get())

    def get_pt4_checkbox_value(self):
        return not bool(self.pt4_checkbox_value.get())

    def get_pt5_checkbox_value(self):
        return not bool(self.pt5_checkbox_value.get())

    def get_pt6_checkbox_value(self):
        return not bool(self.pt6_checkbox_value.get())

    def get_pt7_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())

    def get_pt8_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    def get_pt9_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())

    def get_pt10_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_gs_dropdown()
        self._build_mask_to_csv_button()
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_points()
        self._build_all_points()
        self._build_save()
        self._build_use_mask_button()
        self._build_instant_save_button()
        self._build_edit_coords_button()
        self._build_upload_mask_button()
        self._build_info_label()
        self._build_original_image(self.original_image_data)

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=1, column=0,
                                      columnspan=1, inner_pady=5, outer_padx=(15, 5))
        self.rgb_checkbox = make_checkbox(self.root, "", row=1, column=0, columnspan=1, var=self.rgb_checkbox_value,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.rgb_checkbox.deselect()
        self.rgb_checkbox.bind('<Button-1>', self.__update_rgb_check_status)

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=1, column=1,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.sto2_checkbox = make_checkbox(self.root, "", row=1, column=1, columnspan=1, var=self.sto2_checkbox_value,
                                           inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.sto2_checkbox.deselect()
        self.sto2_checkbox.bind('<Button-1>', self.__update_sto2_check_status)

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=1, column=2,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.nir_checkbox = make_checkbox(self.root, "", row=1, column=2, columnspan=1, var=self.nir_checkbox_value,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.nir_checkbox.deselect()
        self.nir_checkbox.bind('<Button-1>', self.__update_nir_check_status)

    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=1, column=3,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.thi_checkbox = make_checkbox(self.root, "", row=1, column=3, columnspan=1, var=self.thi_checkbox_value,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.thi_checkbox.deselect()
        self.thi_checkbox.bind('<Button-1>', self.__update_thi_check_status)

    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=1, column=4,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5))
        self.twi_checkbox = make_checkbox(self.root, "", row=1, column=4, columnspan=1, var=self.twi_checkbox_value,
                                          inner_padx=0, inner_pady=0, outer_padx=(0, 3), sticky=NE)
        self.twi_checkbox.deselect()
        self.twi_checkbox.bind('<Button-1>', self.__update_twi_check_status)

    # ----------------------------------------------- BUILDERS (POINTS) -----------------------------------------------

    def _build_all_points(self):
        # remove
        self.all_points_remove = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt('all'),
                                             row=1, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                             highlightthickness=0)
        # checkbox
        self.all_points_checkbox = make_checkbox(self.root, "", row=1, column=7, columnspan=1,
                                                 var=self.all_points_checkbox_value, inner_padx=0, inner_pady=0,
                                                 outer_padx=(0, 15), sticky=W)
        self.all_points_checkbox.deselect()
        self.all_points_checkbox.bind('<Button-1>', self.__update_all_points_checked)

    def _build_points(self):
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_pt9()
        self._build_pt10()

    def _build_ptn(self, num, var):
        # label
        # display points on interval [1, max] because ??????
        if self.coords_list[num] == (None, None):
            label = make_text(self.root, content="Pt " + str(num) + ': ' + str(self.coords_list[num]),
                              bg=tkcolour_from_rgb(BACKGROUND), column=5, row=num + 2, width=18, columnspan=1,
                              padx=0, state=NORMAL)
        else:
            label = make_text(self.root,
                              content="Pt " + str(num) + ': ' + str(tuple(x + 1 for x in self.coords_list[num])),
                              bg=tkcolour_from_rgb(BACKGROUND), column=5, row=num + 2, width=18, columnspan=1, padx=0,
                              state=NORMAL)
        # remove
        remove = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt(num + 1), row=num + 2,
                             column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                             highlightthickness=0)
        # checkbox
        checkbox = make_checkbox(self.root, "", row=num + 2, column=7, columnspan=1, var=var, inner_padx=0,
                                 inner_pady=0,
                                 outer_padx=(0, 15), sticky=W)
        return label, remove, checkbox

    def _build_pt1(self):
        # text
        self.pt1_label, self.pt1_remove, self.pt1_checkbox = self._build_ptn(0, self.pt1_checkbox_value)
        self.pt1_checkbox.deselect()
        self.pt1_checkbox.bind('<Button-1>', self.__update_pt1_checked)

    def _build_pt2(self):
        # text
        self.pt2_label, self.pt2_remove, self.pt2_checkbox = self._build_ptn(1, self.pt2_checkbox_value)
        self.pt2_checkbox.deselect()
        self.pt2_checkbox.bind('<Button-1>', self.__update_pt2_checked)

    def _build_pt3(self):
        # text
        self.pt3_label, self.pt3_remove, self.pt3_checkbox = self._build_ptn(2, self.pt3_checkbox_value)
        self.pt3_checkbox.deselect()
        self.pt3_checkbox.bind('<Button-1>', self.__update_pt3_checked)

    def _build_pt4(self):
        # text
        self.pt4_label, self.pt4_remove, self.pt4_checkbox = self._build_ptn(3, self.pt4_checkbox_value)
        self.pt4_checkbox.deselect()
        self.pt4_checkbox.bind('<Button-1>', self.__update_pt4_checked)

    def _build_pt5(self):
        self.pt5_label, self.pt5_remove, self.pt5_checkbox = self._build_ptn(4, self.pt5_checkbox_value)
        self.pt5_checkbox.deselect()
        self.pt5_checkbox.bind('<Button-1>', self.__update_pt5_checked)

    def _build_pt6(self):
        self.pt6_label, self.pt6_remove, self.pt6_checkbox = self._build_ptn(5, self.pt6_checkbox_value)
        self.pt6_checkbox.deselect()
        self.pt6_checkbox.bind('<Button-1>', self.__update_pt6_checked)

    def _build_pt7(self):
        self.pt7_label, self.pt7_remove, self.pt7_checkbox = self._build_ptn(6, self.pt7_checkbox_value)
        self.pt7_checkbox.deselect()
        self.pt7_checkbox.bind('<Button-1>', self.__update_pt7_checked)

    def _build_pt8(self):
        self.pt8_label, self.pt8_remove, self.pt8_checkbox = self._build_ptn(7, self.pt8_checkbox_value)
        self.pt8_checkbox.deselect()
        self.pt8_checkbox.bind('<Button-1>', self.__update_pt8_checked)

    def _build_pt9(self):
        self.pt9_label, self.pt9_remove, self.pt9_checkbox = self._build_ptn(8, self.pt9_checkbox_value)
        self.pt9_checkbox.deselect()
        self.pt9_checkbox.bind('<Button-1>', self.__update_pt9_checked)

    def _build_pt10(self):
        self.pt10_label, self.pt10_remove, self.pt10_checkbox = self._build_ptn(9, self.pt10_checkbox_value)
        self.pt10_checkbox.deselect()
        self.pt10_checkbox.bind('<Button-1>', self.__update_pt10_checked)

    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Original Image', command=self.__info, width=12)
        self.info_label.grid(columnspan=2)

    def _build_gs_dropdown(self):
        self.gs_var.set(self.gs_choices[0])
        self.gs_dropdown = OptionMenu(self.root, self.gs_var, *self.gs_choices, command=self.__update_gs)
        self.gs_dropdown.configure(highlightthickness=0, width=1, anchor='w', padx=15)
        self.gs_dropdown.grid(column=2, row=0, columnspan=1)

    def _build_mask_to_csv_button(self):
        self.mask_to_csv_button = make_button(self.root, text='Mask to CSV', width=8, command=self.__mask_to_csv,
                                              row=0, column=3, columnspan=2, inner_pady=0, outer_padx=5)

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=12, column=0, columnspan=1, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5)
        self.save_checkbox = make_checkbox(self.root, text="", row=12, column=0, var=self.save_checkbox_value,
                                           sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 15),
                                           outer_padx=(54, 0))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_upload_mask_button(self):
        self.upload_mask_button = make_button(self.root, text='Upload mask', width=9, command=self.__upload_mask,
                                              row=12, column=0, columnspan=3, inner_pady=5, outer_padx=(60, 0),
                                              outer_pady=(10, 15))

    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save coords', width=9, command=self.__save_coords,
                                               row=12, column=2, columnspan=3, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))

    def _build_edit_coords_button(self):
        self.input_coords_button = make_button(self.root, text='Edit coords', width=9, command=self.__input_coords,
                                               row=12, column=4, columnspan=2, inner_pady=5, outer_padx=(0, 33),
                                               outer_pady=(10, 15))

    def _build_use_mask_button(self):
        self.use_mask_button = make_button(self.root, text='Use mask', width=9, command=self.__use_coords, row=12,
                                           column=5, columnspan=3, inner_pady=5, outer_padx=(65, 0),
                                           outer_pady=(10, 15))

    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------

    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=2, column=0, rowspan=10,
                                             columnspan=5, inner_pady=80, inner_padx=120, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            if self.gs:
                data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            logging.debug("BUILDING ORIGINAL COLOUR IMAGE...")
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=2, column=0, columnspan=5, rowspan=10, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=2.5, figwidth=3.5,
                           gs=self.gs)
            self.original_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            if self.pop_up:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def _draw_points(self):
        copy_data = self.original_image_data.copy()
        not_none = [i for i in self.coords_list if i != (None, None)]
        for point in not_none:
            y = int(point[0])
            x = int(point[1])
            for xi in range(-4, 5):
                copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
            for yi in range(-4, 5):
                copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
            idx = not_none.index(point)
            self._draw_a_line(not_none[idx - 1], not_none[idx], copy_data)
        self._build_original_image(copy_data)

    @staticmethod
    def _draw_a_line(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(113 * val[i]), int(255 * val[i]), int(66 * val[i]))
        return image

    # --------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].original_info
        title = "Original Image Information"
        make_info(title=title, info=info)

    # ------------------------------------------------------ MASK -----------------------------------------------------

    def __upload_mask(self):
        mask_dir_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file "
                                                                           "containing the coordinates of a mask.")
        if mask_dir_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.__load_mask(mask_dir_path)

    def __load_mask(self, path):
        coords = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                coords.append(((int(float(row[0]) - 1)), (int(float(row[1]) - 1))))
        for i in range(10 - len(coords)):
            coords.append((None, None))
        self.coords_list = coords
        self._build_points()
        self._draw_points()

    def __use_coords(self):
        # produces a 640x480 8-bit mask
        if self.listener.is_masked:
            self.listener.modules[ORIGINAL_COLOUR_DATA].empty_stats()
            self.listener.modules[NEW_COLOUR_DATA].empty_stats()
            self.listener.modules[RECREATED_COLOUR_DATA].empty_stats()
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        self.mask_raw = np.array(img)
        self.mask_raw = np.fliplr(self.mask_raw.T)
        self.listener.submit_mask(np.logical_not(self.mask_raw))

    def __mask_to_csv(self):
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        mask_array = np.array(img)
        path = os.path.dirname(self.listener.current_rendered_result_path)
        print(path)
        output_path = path + "/mask" + '.csv'
        np.savetxt(output_path, mask_array, delimiter=",", fmt="%d")

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __save_coords(self):
        self.listener.instant_save_points()

    def __get_coords(self, eventorigin):
        if not self.pop_up:
            x = int((eventorigin.x - 30) * 640 / 296)
            y = int((eventorigin.y - 18) * 480 / 221)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))
        else:
            x = int((eventorigin.x - 17) * 640 / 770)
            y = int((eventorigin.y - 114) * 480 / 578)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))

    def __remove_pt(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for _ in range(10)]
        else:
            self.coords_list[index - 1] = (None, None)
        self._build_points()
        self._draw_points()

    def __add_pt(self, pt):
        if self.coords_list.count((None, None)) != 0:
            index = self.coords_list.index((None, None))
            self.coords_list[index] = pt
            self._build_points()
            self._draw_points()

    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------

    def __update_to_rgb(self):
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = RGB
        self.listener.broadcast_to_original_image()

    def __update_to_sto2(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = STO2
        self.listener.broadcast_to_original_image()

    def __update_to_nir(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = NIR
        self.listener.broadcast_to_original_image()

    def __update_to_thi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = THI
        self.listener.broadcast_to_original_image()

    def __update_to_twi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.displayed_image_mode = TWI
        self.listener.broadcast_to_original_image()

    def __update_gs(self, event):
        if self.gs_var.get()[:2] == 'CS':
            self.gs = False
            self.update_original_image(self.original_image_data)
        elif self.gs_var.get()[:2] == 'GS':
            self.gs = True
            self.update_original_image(self.original_image_data)

    # ---------------------------------------------- UPDATERS (SAVING) ------------------------------------------------

    def __update_rgb_check_status(self, event):
        value = not bool(self.rgb_checkbox_value.get())
        self.listener.update_saved(OG_RGB_DATA, value)

    def __update_sto2_check_status(self, event):
        value = not bool(self.sto2_checkbox_value.get())
        self.listener.update_saved(OG_STO2_DATA, value)

    def __update_nir_check_status(self, event):
        value = not bool(self.nir_checkbox_value.get())
        self.listener.update_saved(OG_NIR_DATA, value)

    def __update_twi_check_status(self, event):
        value = not bool(self.twi_checkbox_value.get())
        self.listener.update_saved(OG_TWI_DATA, value)

    def __update_thi_check_status(self, event):
        value = not bool(self.thi_checkbox_value.get())
        self.listener.update_saved(OG_THI_DATA, value)

    def __update_save_with_scale_check_status(self, event):
        value = not bool(self.save_checkbox_value.get())
        self.listener.update_saved(OG_IMAGE, value)

    # ---------------------------------------------- UPDATERS (POINTS) ------------------------------------------------

    def __update_all(self, value):
        for point in [PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8, PT9, PT10]:
            self.listener.update_saved(point, value)

    def __update_all_points_checked(self, event):
        value = not bool(self.all_points_checkbox_value.get())
        if value:
            self.pt1_checkbox.select()
            self.pt2_checkbox.select()
            self.pt3_checkbox.select()
            self.pt4_checkbox.select()
            self.pt5_checkbox.select()
            self.pt6_checkbox.select()
            self.pt7_checkbox.select()
            self.pt8_checkbox.select()
            self.pt9_checkbox.select()
            self.pt10_checkbox.select()
        else:
            self.pt1_checkbox.deselect()
            self.pt2_checkbox.deselect()
            self.pt3_checkbox.deselect()
            self.pt4_checkbox.deselect()
            self.pt5_checkbox.deselect()
            self.pt6_checkbox.deselect()
            self.pt7_checkbox.deselect()
            self.pt8_checkbox.deselect()
            self.pt9_checkbox.deselect()
            self.pt10_checkbox.deselect()
        self.__update_all(value)

    def __update_pt1_checked(self, event):
        value = self.get_pt1_checkbox_value()
        self.listener.update_saved(PT1, value)

    def __update_pt2_checked(self, event):
        value = self.get_pt2_checkbox_value()
        self.listener.update_saved(PT2, value)

    def __update_pt3_checked(self, event):
        value = self.get_pt3_checkbox_value()
        self.listener.update_saved(PT3, value)

    def __update_pt4_checked(self, event):
        value = self.get_pt4_checkbox_value()
        self.listener.update_saved(PT4, value)

    def __update_pt5_checked(self, event):
        value = self.get_pt5_checkbox_value()
        self.listener.update_saved(PT5, value)

    def __update_pt6_checked(self, event):
        value = self.get_pt6_checkbox_value()
        self.listener.update_saved(PT6, value)

    def __update_pt7_checked(self, event):
        value = self.get_pt7_checkbox_value()
        self.listener.update_saved(PT7, value)

    def __update_pt8_checked(self, event):
        value = self.get_pt8_checkbox_value()
        self.listener.update_saved(PT8, value)

    def __update_pt9_checked(self, event):
        value = self.get_pt9_checkbox_value()
        self.listener.update_saved(PT9, value)

    def __update_pt10_checked(self, event):
        value = self.get_pt10_checkbox_value()
        self.listener.update_saved(PT10, value)

    # ------------------------------------------------- IMAGE POP-UP --------------------------------------------------

    def __pop_up_image(self, event):
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

    def __input_coord_n(self, num):
        title = make_text(self.coords_window, content="Pt " + str(num) + ': ', bg=tkcolour_from_rgb(BACKGROUND),
                          column=0, row=num + 1, width=6, pady=(0, 3), padx=(15, 0))
        title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=num + 1,
                            width=4, pady=(0, 3))
        title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=num + 1,
                            width=4, pady=(0, 3), padx=(5, 0))
        input_x = make_entry(self.coords_window, row=num + 1, column=2, width=5, columnspan=1, pady=(0, 3))
        input_y = make_entry(self.coords_window, row=num + 1, column=4, width=5, columnspan=1, padx=(0, 15),
                             pady=(0, 3))
        if self.coords_list[num] != (None, None):
            input_x.insert(END, str(self.coords_list[num][0] + 1))
            input_y.insert(END, str(self.coords_list[num][1] + 1))
        return title, title_x, title_y, input_x, input_y

    def __input_coords(self):
        self.coords_window = Toplevel()
        self.coords_window.geometry("+0+0")
        self.coords_window.configure(bg=tkcolour_from_rgb(BACKGROUND))

        # title
        self.input_points_title = make_label_button(self.coords_window, text='Coordinate Input',
                                                    command=self.__input_info, width=14)
        self.input_points_title.grid(columnspan=3)

        # points
        self.input_pt1_title, self.input_pt1_title_x, self.input_pt1_title_y, self.input_pt1_x, self.input_pt1_y = \
            self.__input_coord_n(0)
        self.input_pt2_title, self.input_pt2_title_x, self.input_pt2_title_y, self.input_pt2_x, self.input_pt2_y = \
            self.__input_coord_n(1)
        self.input_pt3_title, self.input_pt3_title_x, self.input_pt3_title_y, self.input_pt3_x, self.input_pt3_y = \
            self.__input_coord_n(2)
        self.input_pt4_title, self.input_pt4_title_x, self.input_pt4_title_y, self.input_pt4_x, self.input_pt4_y = \
            self.__input_coord_n(3)
        self.input_pt5_title, self.input_pt5_title_x, self.input_pt5_title_y, self.input_pt5_x, self.input_pt5_y = \
            self.__input_coord_n(4)
        self.input_pt6_title, self.input_pt6_title_x, self.input_pt6_title_y, self.input_pt6_x, self.input_pt6_y = \
            self.__input_coord_n(5)
        self.input_pt7_title, self.input_pt7_title_x, self.input_pt7_title_y, self.input_pt7_x, self.input_pt7_y = \
            self.__input_coord_n(6)
        self.input_pt8_title, self.input_pt8_title_x, self.input_pt8_title_y, self.input_pt8_x, self.input_pt8_y = \
            self.__input_coord_n(7)
        self.input_pt9_title, self.input_pt9_title_x, self.input_pt9_title_y, self.input_pt9_x, self.input_pt9_y = \
            self.__input_coord_n(8)
        self.input_pt10_title, self.input_pt10_title_x, self.input_pt10_title_y, self.input_pt10_x, self.input_pt10_y = \
            self.__input_coord_n(9)

        # go button
        self.go_button = make_button(self.coords_window, text='Go', width=2, command=self.__use_inputted_coords, row=11,
                                     column=0, columnspan=5, inner_pady=5, outer_padx=(15, 15), outer_pady=(7, 15))

    def __use_inputted_coords(self):
        coords = [(self.input_pt1_x.get(), self.input_pt1_y.get()),
                  (self.input_pt2_x.get(), self.input_pt2_y.get()),
                  (self.input_pt3_x.get(), self.input_pt3_y.get()),
                  (self.input_pt4_x.get(), self.input_pt4_y.get()),
                  (self.input_pt5_x.get(), self.input_pt5_y.get()),
                  (self.input_pt6_x.get(), self.input_pt6_y.get()),
                  (self.input_pt7_x.get(), self.input_pt7_y.get()),
                  (self.input_pt8_x.get(), self.input_pt8_y.get()),
                  (self.input_pt9_x.get(), self.input_pt9_y.get()),
                  (self.input_pt10_x.get(), self.input_pt10_y.get())]
        coords = [(int(i[0]) - 1, int(i[1]) - 1) for i in coords if i[0] != '' and i[1] != '']
        if len(coords) > 0:
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            for i in range(10 - len(coords)):
                coords.append((None, None))
            if min(xs) >= 0 and max(xs) < 640 and min(ys) >= 0 and max(ys) < 480:
                self.coords_list = coords
                self._build_points()
                self._draw_points()
            else:
                messagebox.showerror("Error", "x values must be on the interval [1, 640] and y values must be on the "
                                              "interval \n[1, 480].")
        self.coords_window.destroy()
