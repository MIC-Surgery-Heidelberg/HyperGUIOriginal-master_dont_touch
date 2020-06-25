from HyperGuiModules.utility import *
import numpy as np
import matplotlib.pyplot as plt
import skimage.color
import os
import logging


class Save:
    def __init__(self, save_frame, listener):
        self.root = save_frame

        # Listener
        self.listener = listener

        self.save_specific_button = None
        self.save_all_button = None

        self.info_label = None

        # Saves
        # by default, nothing is saved
        self.saves = {
            WHOLE_IMAGE_SAVE: False,
            MASKED_IMAGE_SAVE: False,
            STO2_DATA: False,
            NIR_DATA: False,
            TWI_DATA: False,
            THI_DATA: False,
            OG_IMAGE: False,
            OG_RGB_DATA: False,
            OG_STO2_DATA: False,
            OG_NIR_DATA: False,
            OG_TWI_DATA: False,
            OG_THI_DATA: False,
            REC_IMAGE: False,
            REC_IMAGE_WO_SCALE: False,
            WL_DATA: False,
            IDX_DATA: False,
            NEW_IMAGE: False,
            NEW_IMAGE_WO_SCALE: False,
            HISTOGRAM_IMAGE: False,
            HISTOGRAM_IMAGE_WO_SCALE: False,
            HISTOGRAM_EXCEL: False,
            ABSORPTION_SPEC_IMAGE: False,
            ABSORPTION_SPEC_IMAGE_WO_SCALE: False,
            ABSORPTION_SPEC_EXCEL: False,
            PT1: False,
            PT2: False,
            PT3: False,
            PT4: False,
            PT5: False,
            PT6: False,
            PT7: False,
            PT8: False,
            PT9: False,
            PT10: False,
        }

        # The current data cube whose data is being saved.
        # Used to access results from listener
        self.current_result_key = ""
        self.current_result_list = None  # for readability
        self.current_hist_result = None
        self.current_abs_result = None
        self.current_rec_result = None
        self.current_new_result = None
        # The current path to save to
        # i.e the current result key's dirname
        self.current_output_path = ""

        self._init_widgets()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def update_saves(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        # print(self.saves)

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save for Rendered Data Cube Only",
                                                command=self._save_specific, row=1, column=0, outer_pady=(0, 5),
                                                outer_padx=15, width=13, wraplength=120, height=2)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save for All Data Cubes', command=self._save_all, row=2,
                                           column=0, outer_pady=(0, 15), outer_padx=15, width=13, wraplength=120,
                                           height=2)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Save', command=self.__info, width=4)
        self.info_label.grid(padx=(0, 90))

    # --------------------------------------------------- CALLBACKS --------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].save_info
        title = "Save Information"
        make_info(title=title, info=info)

    # ------------------------------------------------ SAVING CALLBACKS ----------------------------------------------

    def _save_specific(self):
        for path, _ in self.listener.results.items():
            selected_paths = self.listener.selected_paths
            if path in selected_paths:
                self._save_to_path(path)

    def _save_all(self):
        for path, _ in self.listener.results.items():
            self._save_to_path(path)

    def _save_to_path(self, path):
        self.current_result_key = path
        self.current_result_list = self.listener.get_result(self.current_result_key)

        self.current_hist_result = self.current_result_list[0]
        self.current_abs_result = self.current_result_list[1]
        self.current_rec_result = self.current_result_list[2]
        self.current_new_result = self.current_result_list[3]

        self.current_output_path = os.path.dirname(path)

        if self.saves[PT1] or self.saves[PT2] or self.saves[PT3] or \
                self.saves[PT4] or self.saves[PT5] or self.saves[PT6] or \
                self.saves[PT7] or self.saves[PT8] or self.saves[PT9] or \
                self.saves[PT10]:
            self.__save_points()

        if self.saves[OG_RGB_DATA] or self.saves[OG_STO2_DATA] or \
                self.saves[OG_NIR_DATA] or self.saves[OG_THI_DATA] or \
                self.saves[OG_TWI_DATA]:
            self.__save_original_image()

        if self.saves[HISTOGRAM_IMAGE] or \
                self.saves[HISTOGRAM_IMAGE_WO_SCALE] or \
                self.saves[HISTOGRAM_EXCEL]:
            self.__save_histogram()

        if self.saves[ABSORPTION_SPEC_IMAGE] or \
                self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE] or \
                self.saves[ABSORPTION_SPEC_EXCEL]:
            self.__save_absorption_spec()

        if self.saves[STO2_DATA] or self.saves[NIR_DATA] or \
                self.saves[TWI_DATA] or self.saves[THI_DATA]:
            self.__save_recreated_image()

        if self.saves[WL_DATA] or self.saves[IDX_DATA]:
            self.__save_new_image()

    # ------------------------------------------------- SAVING HELPERS -----------------------------------------------

    def __save_data(self, data, title, stats=[None, None], fmt=".csv", formatting="%.2f"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING DATA TO " + output_path)
        if stats != [None, None]:
            data = np.clip(data, a_min=stats[0], a_max=stats[1])
        np.savetxt(self.current_output_path + "/" + title + fmt, data, delimiter=",", fmt=formatting)

    def __save_image(self, data, name, is_image_with_scale, is_image_wo_scale, stats, cmap='jet', fmt=".png"):
        if is_image_with_scale:
            title = name[0] + '_with-scale_' + name[1]
            self.__save_image_diagram(data, title, True, cmap, stats, fmt)
        if is_image_wo_scale:
            title = name[0] + '_wo-scale_' + name[1]
            self.__save_image_diagram(data, title, False, cmap, stats, fmt)

    def __save_image_diagram(self, data, title, scale, cmap, stats=[None, None], fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING IMAGE TO " + output_path)
        plt.clf()
        plt.imshow(data, cmap=cmap, vmin=stats[0], vmax=stats[1])
        if not scale:
            plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=300)
        plt.clf()

    @staticmethod
    def remove_masked_vals(data, mask, stats):
        if stats != [None, None]:
            data = np.clip(data, a_min=stats[0], a_max=stats[1])
        arr = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                if mask[i][j]:
                    arr.append(str(''))
                else:
                    arr.append(str(float(data[i][j])))
        return np.rot90(np.asarray(arr).reshape((480, 640)), 3)

    # ------------------------------------------------- ORIGINAL IMAGE -----------------------------------------------

    def __save_points(self):
        point_bools = [self.saves[PT1], self.saves[PT2], self.saves[PT3], self.saves[PT4], self.saves[PT5],
                       self.saves[PT6], self.saves[PT7], self.saves[PT8], self.saves[PT9], self.saves[PT10]]
        data = self.listener.get_coords(point_bools)
        self.__save_data(data, title="MASK_COORDINATES")

    def instant_save_points(self, data, title):
        for path, _ in self.listener.results.items():
            selected_paths = self.listener.selected_paths
            if path in selected_paths:
                output_path = os.path.dirname(path) + "/" + title + '.csv'
                logging.debug("SAVING DATA TO " + output_path)
                np.savetxt(output_path, data, delimiter=",", fmt="%.2f")

    def __save_original_image(self):
        # mask
        mask = None
        if self.saves[MASKED_IMAGE_SAVE]:
            mask = self.listener.get_mask()
        # cmap
        cmap = 'jet'
        if self.listener.modules[ORIGINAL_COLOUR].gs:
            cmap = 'gray'
        # save
        if self.saves[OG_RGB_DATA]:
            # self.__save_og_rgb_image(cmap, mask)
            self.__save_og_data_image(cmap, mask, 'RGB', self.current_hist_result.get_rgb_og())
        if self.saves[OG_STO2_DATA]:
            self.__save_og_data_image(cmap, mask, 'STO2', self.current_hist_result.get_sto2_og())
        if self.saves[OG_NIR_DATA]:
            self.__save_og_data_image(cmap, mask, 'NIR', self.current_hist_result.get_nir_og())
        if self.saves[OG_THI_DATA]:
            self.__save_og_data_image(cmap, mask, 'THI', self.current_hist_result.get_thi_og())
        if self.saves[OG_TWI_DATA]:
            self.__save_og_data_image(cmap, mask, 'TWI', self.current_hist_result.get_twi_og())

    def __save_og_data_image(self, cmap, mask, display, current_result):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info(display, image=False) + '_whole'
            data = current_result
            disp = self.__convert_original_image(data)
            self.__save_data(disp, title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info(display, image=True) + '_whole'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap)
                else:
                    self.__save_image_diagram(disp, title, False, cmap=cmap)

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info(display, image=False) + '_masked'
            data = self.fake_mask_og_image(current_result, np.rot90(mask))
            converted = self.__convert_original_image(current_result)
            disp_data = np.rot90(self.remove_masked_vals(converted, mask=np.rot90(mask), stats=[None, None]))
            self.__save_data(disp_data, title, formatting='%s')

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info(display, image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap)
                else:
                    arr = np.ma.array(converted, mask=np.rot90(mask))
                    self.__save_image_diagram(arr, title, False, cmap=cmap)

    def fake_mask_og_image(self, data, mask):
        for i in range(len(data)):
            for j in range(len(data[i])):
                if mask[i][j]:
                    data[i][j][0] = 255
                    data[i][j][1] = 255
                    data[i][j][2] = 255
        return data

    @staticmethod
    def __convert_original_image(array):
        return np.asarray(rgb_image_to_hsi_array(array))

    # ---------------------------------------------------- HISTOGRAM -------------------------------------------------

    def hist_data_from_spec_num(self, spec_num, masked):
        if spec_num in [1, 2, 3, 4, 5, 6, 7, 8]:
            if masked:
                data = self.current_hist_result.histogram_data_masked.flatten()
                d = np.ma.sort(data)
                index = np.where(d.mask)[0][0]
                return d[:index]
            else:
                return self.current_hist_result.histogram_data.flatten()
        else:
            mask = self.listener.get_mask()
            if masked:
                if spec_num not in [9, 10]:
                    unmasked_data = self.listener.modules[HISTOGRAM].hist_data
                    data = np.ma.array(unmasked_data, mask=mask)
                    d = np.ma.sort(data)
                    index = np.where(d.mask)[0][0]
                    data = d[:index]
                    return data

                else:
                    if self.listener.is_masked:
                        data = self.listener.modules[HISTOGRAM].hist_data
                        print('masked? ' + str(isinstance(data, np.ma.MaskedArray)))
                        d = np.ma.sort(data)
                        index = np.where(d.mask)[0][0]
                        data = d[:index]
                        return data

                    else:
                        data = self.listener.modules[HISTOGRAM].hist_data
                        print('masked? ' + str(isinstance(data, np.ma.MaskedArray)))
                        data = np.ma.array(data, mask=np.rot90(mask))
                        d = np.ma.sort(data)
                        index = np.where(d.mask)[0][0]
                        data = d[:index]
                        return data.data

            else:
                data = self.listener.modules[HISTOGRAM].hist_data
                print(len(data))
                if isinstance(data, np.ma.MaskedArray):
                    print('masked')
                    whole_mask = data.mask.flatten()
                    flat_mask = mask.flatten()
                    unmasked = data.data

                    temp_mask = [whole_mask[i] if not flat_mask[i] else False for i in range(len(whole_mask))]

                    final_mask = np.asarray(temp_mask)
                    data = np.ma.array(unmasked, mask=final_mask)
                    d = np.ma.sort(data)
                    if True in d.mask:
                        index = np.where(d.mask)[0][0]
                        data = d[:index]
                    else:
                        data = d
                return data

    def __save_histogram(self):
        if self.listener.modules[HISTOGRAM].spec_number == -1:
            pass
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.hist_data_from_spec_num(self.listener.modules[HISTOGRAM].spec_number, False)
            self.__save_histogram_graph(data, self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE],
                                        masked=False)
            if self.saves[HISTOGRAM_EXCEL]:
                data = self.hist_data_from_spec_num(self.listener.modules[HISTOGRAM].spec_number, False)
                name = self.listener.get_save_hist_info(scale=True, image=False, masked=False,
                                                        data=data)
                self.__save_histogram_data(data, name, masked=False)

        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.hist_data_from_spec_num(self.listener.modules[HISTOGRAM].spec_number, True)
            self.__save_histogram_graph(data, self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE],
                                        masked=True)
            if self.saves[HISTOGRAM_EXCEL]:
                data = self.hist_data_from_spec_num(self.listener.modules[HISTOGRAM].spec_number, True)
                name = self.listener.get_save_hist_info(scale=True, image=False, masked=True,
                                                        data=data)
                self.__save_histogram_data(data, name, masked=True)

    def __save_histogram_data(self, data, name, masked):
        stats = self.listener.generate_hist_values_for_saving(masked, data)
        (x_low, x_high, y_low, y_high, step) = stats
        start = x_low
        stop = x_high + step
        bins = np.arange(start=start, stop=stop, step=step)
        counts, hist_bins, _ = plt.hist(data, bins=bins)
        counts = np.clip(counts, a_min=y_low, a_max=y_high)
        hist_data = np.stack((bins[:-1], counts)).T
        self.__save_data(hist_data, name, formatting="%.2f")

    def __save_histogram_graph(self, data, is_hist_with_scale, is_hist_wo_scale, masked, fmt=".png"):
        if is_hist_with_scale:
            name = self.listener.get_save_hist_info(scale=True, image=True, masked=masked,
                                                    data=data)
            self.__save_histogram_diagram(data, name, True, masked, fmt=fmt)
        if is_hist_wo_scale:
            name = self.listener.get_save_hist_info(scale=False, image=True, masked=masked,
                                                    data=data)
            self.__save_histogram_diagram(data, name, False, masked, fmt=fmt)

    def __save_histogram_diagram(self, data, title, scale, masked, fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING HISTOGRAM TO " + output_path)
        plt.clf()
        axes = plt.subplot(111)
        stats = self.listener.generate_hist_values_for_saving(masked, data)
        (x_low, x_high, y_low, y_high, step) = stats
        start = x_low
        stop = x_high + step
        print(start, stop, step)
        print(stats)
        print(len(data))
        print(data[:30])
        bins = np.arange(start=start, stop=stop, step=step)
        # plot histogram
        axes.hist(data, bins=bins)
        if self.listener.modules[HISTOGRAM].parametric:
            # plot error bar
            mean_value = np.mean(data)
            sd_value = np.std(data)
            axes2 = axes.twinx()
            axes2.plot([mean_value - sd_value, mean_value + sd_value], [1, 1], 'k-', lw=1)
            axes2.plot([mean_value - sd_value, mean_value - sd_value], [0.9, 1.1], 'k-', lw=1)
            axes2.plot([mean_value + sd_value, mean_value + sd_value], [0.9, 1.1], 'k-', lw=1)
            axes2.plot([mean_value, mean_value], [0.9, 1.1], '#F17E3A', lw=1)
            axes2.set_ylim(bottom=0, top=2)
            axes2.get_yaxis().set_visible(False)
        elif self.listener.modules[HISTOGRAM].non_parametric:
            # plot boxplot
            axes2 = axes.twinx()
            axes2.boxplot(data, vert=False, sym='')
            axes2.get_yaxis().set_visible(False)
        # set axes
        axes.set_xlim(left=x_low, right=x_high)
        axes.set_ylim(bottom=y_low, top=y_high)
        # commas and non-scientific notation
        axes.ticklabel_format(style='plain')
        axes.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[HISTOGRAM].format_axis))
        axes.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[HISTOGRAM].format_axis))
        if scale:
            plt.title(title)
        else:
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    # ------------------------------------------------ ABSORPTION SPEC -----------------------------------------------

    @staticmethod
    def norm(data):
        if np.ma.min(data) < 0:
            data = data + np.abs(np.ma.min(data))
        if np.ma.min(data) > 0:
            data = data - np.abs(np.ma.min(data))
        return data / np.ma.max(data)

    def __save_absorption_spec(self):
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_abs_result.absorption_roi[:, 1]
            print(self.listener.modules[ABSORPTION_SPEC].whole_stats)
            if self.listener.modules[ABSORPTION_SPEC].whole_stats[4]:
                data = self.norm(data)
            self.__save_absorption_spec_graph(data, self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE], masked=False)

            if self.saves[ABSORPTION_SPEC_EXCEL]:
                stats = self.listener.generate_abs_values_for_saving(False, data)
                (x_low, x_high, y_low, y_high, norm) = stats
                print(y_low, y_high)
                data1 = np.arange(x_low // 5 * 5, x_high // 5 * 5 + 5, 5)
                data2 = self.current_abs_result.absorption_roi[:, 1][int((x_low - 500) / 5):int((x_high - 500) / 5) + 1]
                if self.listener.modules[ABSORPTION_SPEC].whole_stats[4]:
                    data2 = self.norm(data2)
                data2 = np.clip(data2, a_min=y_low, a_max=y_high)
                data = np.asarray([data1, data2]).T
                name = self.listener.get_save_abs_info(scale=True, image=False, masked=False, data=data)
                self.__save_data(data, name, formatting="%.5f")

        if self.saves[MASKED_IMAGE_SAVE]:
            print(self.listener.modules[ABSORPTION_SPEC].masked_stats)
            data = self.current_abs_result.absorption_roi_masked[:, 1]
            if self.listener.modules[ABSORPTION_SPEC].masked_stats[4]:
                data = self.norm(data)
            self.__save_absorption_spec_graph(data, self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE], masked=True)

            if self.saves[ABSORPTION_SPEC_EXCEL]:
                stats = self.listener.generate_abs_values_for_saving(True, data)
                (x_low, x_high, y_low, y_high, norm) = stats

                data1 = np.arange(x_low // 5 * 5, x_high // 5 * 5 + 5, 5)
                data2 = self.current_abs_result.absorption_roi_masked[:, 1]
                if self.listener.modules[ABSORPTION_SPEC].masked_stats[4]:
                    data2 = self.norm(data2)
                data2 = np.clip(data2, a_min=y_low, a_max=y_high)
                data = np.asarray([data1, data2]).T
                name = self.listener.get_save_abs_info(scale=True, image=False, masked=True, data=data)
                self.__save_data(data, name, formatting="%.5f")

    def __save_absorption_spec_graph(self, data, is_abspc_with_scale, is_abspc_wo_scale, masked, fmt=".png"):
        if is_abspc_with_scale:
            name = self.listener.get_save_abs_info(scale=True, image=True, masked=masked, data=data)
            self.__save_absorption_spec_diagram(data, name, True, masked, fmt=fmt)
        if is_abspc_wo_scale:
            name = self.listener.get_save_abs_info(scale=False, image=True, masked=masked, data=data)
            self.__save_absorption_spec_diagram(data, name, False, masked, fmt=fmt)

    def __save_absorption_spec_diagram(self, data, title, scale, masked, fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING ABSORPTION SPEC" + output_path)
        plt.clf()
        axes = plt.subplot(111)
        x_vals = np.arange(500, 1000, 5)
        stats = self.listener.generate_abs_values_for_saving(masked, data)
        (x_low, x_high, y_low, y_high, norm) = stats
        # plot absorption spec
        axes.plot(x_vals, data, '-', lw=0.5)
        axes.grid(linestyle=':', linewidth=0.5)
        low = y_low
        high = y_high
        if low is not None and high is not None:
            factor = (high - low) * 0.05
            low -= factor
            high += factor
        axes.set_xlim(left=x_low, right=x_high)
        axes.set_ylim(bottom=low, top=high)
        axes.ticklabel_format(style='plain')
        axes.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[ABSORPTION_SPEC].format_axis))
        axes.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[ABSORPTION_SPEC].format_axis))
        if scale:
            plt.title(title)
        else:
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    # ------------------------------------------------ RECREATED IMAGE -----------------------------------------------

    def __save_recreated_image(self):
        # greyscale or original
        cmap = 'jet'
        if self.listener.modules[RECREATED_COLOUR].gs:
            cmap = 'gray'

        if self.saves[STO2_DATA]:
            self.__save_rec_data_image(cmap, 'STO2', self.current_rec_result.sto2, self.current_rec_result.sto2_masked)
        if self.saves[NIR_DATA]:
            self.__save_rec_data_image(cmap, 'NIR', self.current_rec_result.nir, self.current_rec_result.nir_masked)
        if self.saves[THI_DATA]:
            self.__save_rec_data_image(cmap, 'THI', self.current_rec_result.thi, self.current_rec_result.thi_masked)
        if self.saves[TWI_DATA]:
            self.__save_rec_data_image(cmap, 'TWI', self.current_rec_result.twi, self.current_rec_result.twi_masked)

    def __save_rec_data_image(self, cmap, display, current_result_display, current_result_display_masked):
        scale = [REC_IMAGE, REC_IMAGE_WO_SCALE]
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = np.rot90(current_result_display)
            data_name = self.listener.get_save_rec_info(display, image=False, masked=False,
                                                        path=self.current_result_key)
            image_name = self.listener.get_save_rec_info(display, image=True, masked=False,
                                                         path=self.current_result_key)
            stats = self.listener.generate_rec_values_for_saving(self.current_result_key, display)
            self.__save_data(data, data_name, stats)
            self.__save_image(data, image_name, self.saves[scale[0]], self.saves[scale[1]], stats, cmap=cmap)

        if self.saves[MASKED_IMAGE_SAVE]:
            masked_data = np.rot90(current_result_display_masked)
            data_name = self.listener.get_save_rec_info(display, image=False, masked=True, path=self.current_result_key)
            image_name = self.listener.get_save_rec_info(display, image=True, masked=True, path=self.current_result_key)
            stats = self.listener.generate_rec_values_for_saving(self.current_result_key, display)
            data = np.rot90(self.remove_masked_vals(masked_data, np.rot90(self.listener.get_mask()), stats))
            self.__save_data(data, data_name, [None, None], formatting="%s")
            self.__save_image(masked_data, image_name, self.saves[scale[0]], self.saves[scale[1]], stats, cmap=cmap)

    # ---------------------------------------------------- NEW IMAGE -------------------------------------------------

    def __save_new_image(self):
        # greyscale or original
        cmap = 'jet'
        if self.listener.modules[NEW_COLOUR].gs:
            cmap = 'gray'

        if self.saves[IDX_DATA]:
            self.__save_new_data_image(cmap, 'IDX', self.current_new_result.index, self.current_new_result.index_masked)
        if self.saves[WL_DATA]:
            self.__save_new_data_image(cmap, 'WL', self.current_new_result.get_wl_data(),
                                       self.current_new_result.get_wl_data_masked())

    def __save_new_data_image(self, cmap, display, current_result_display, current_result_display_masked):
        scale = [NEW_IMAGE, NEW_IMAGE_WO_SCALE]
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = np.rot90(current_result_display)
            data_name = self.listener.get_save_new_info(display, image=False, masked=False,
                                                        path=self.current_result_key)
            image_name = self.listener.get_save_new_info(display, image=True, masked=False,
                                                         path=self.current_result_key)
            stats = self.listener.generate_new_values_for_saving(self.current_result_key, display)
            self.__save_data(data, data_name, stats)
            self.__save_image(data, image_name, self.saves[scale[0]], self.saves[scale[1]], stats, cmap=cmap)

        if self.saves[MASKED_IMAGE_SAVE]:
            masked_data = np.rot90(current_result_display_masked)
            data_name = self.listener.get_save_new_info(display, image=False, masked=True, path=self.current_result_key)
            image_name = self.listener.get_save_new_info(display, image=True, masked=True, path=self.current_result_key)
            stats = self.listener.generate_new_values_for_saving(self.current_result_key, display)
            data = np.rot90(self.remove_masked_vals(masked_data, np.rot90(self.listener.get_mask()), stats))
            self.__save_data(data, data_name, [None, None], formatting="%s")
            self.__save_image(masked_data, image_name, self.saves[scale[0]], self.saves[scale[1]], stats, cmap=cmap)
