from HyperGuiModules.utility import *

np.set_printoptions(threshold=sys.maxsize)

RGB_FILE = "_RGB-Image.png"
STO2_FILE = "_Oxygenation.png"
NIR_FILE = "_NIR-Perfusion.png"
THI_FILE = "_THI.png"
TWI_FILE = "_TWI.png"


class HistogramAnalysis:
    def __init__(self, path, data_cube, wavelength, specs, listener, mask=None):

        self.listener = listener

        # inputs
        self.path = path
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.absorbance = bool(specs[0])
        self.normal = not bool(specs[1])
        self.negative = bool(specs[2])

        # calculated generally
        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None
        self.x_reflectance_masked = None
        self.x_reflectance_masked_w = None

        # specific to module
        self.rgb_og = None
        self.sto2_og = None
        self.nir_og = None
        self.thi_og = None
        self.twi_og = None
        self.histogram_data = None
        self.histogram_data_masked = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_histogram_data()

    # --------------------------------------------------- UPDATERS ----------------------------------------------------

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def update_absorbance(self, new_absorbance):
        self.absorbance = new_absorbance
        self.analysis()

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_rgb_og(self):
        filename = str(self.path[:-13]) + RGB_FILE
        self.rgb_og = image_to_array(filename)
        chopped = self.rgb_og[30:510, 3:643, :3]
        reshaped = self.ensure_shape(chopped)
        print(reshaped.shape)
        return reshaped

    def get_sto2_og(self):
        filename = str(self.path[:-13]) + STO2_FILE
        self.sto2_og = image_to_array(filename)
        chopped = self.sto2_og[26:506, 4:644, :3]
        print(chopped.shape)
        return chopped

    def get_nir_og(self):
        filename = str(self.path[:-13]) + NIR_FILE
        self.nir_og = image_to_array(filename)
        chopped = self.nir_og[26:506, 4:644, :3]
        print(chopped.shape)
        return chopped

    def get_thi_og(self):
        filename = str(self.path[:-13]) + THI_FILE
        self.thi_og = image_to_array(filename)
        chopped = self.thi_og[26:506, 4:644, :3]
        print(chopped.shape)
        return chopped

    def get_twi_og(self):
        filename = str(self.path[:-13]) + TWI_FILE
        self.twi_og = image_to_array(filename)
        chopped = self.twi_og[26:506, 4:644, :3]
        print(chopped.shape)
        return chopped

    def ensure_shape(self, data):
        arr = np.asarray(data.shape)
        g = arr.copy()
        arr.sort()
        i1 = np.where(g == arr[1])[0][0]
        i2 = np.where(g == arr[2])[0][0]
        i3 = np.where(g == arr[0])[0][0]
        return np.moveaxis(data, [i1, i2, i3], [0, 1, 2])

    # ------------------------------------------------- CALCULATORS --------------------------------------------------

    def _calc_histogram_data(self):
        if self.absorbance:
            self.histogram_data = self.x2
            if self.mask is not None:
                self.histogram_data_masked = self.x_absorbance_masked
        else:
            self.histogram_data = self.x1
            if self.mask is not None:
                self.histogram_data_masked = self.x_reflectance_masked

    # --------------------------------------------- GENERAL CALCULATORS ----------------------------------------------

    def _calc_general(self):
        self.__calc_x1()
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def __calc_x1(self):
        neg = 0
        # normalise
        if self.normal and not self.absorbance:
            data = self.data_cube
            if np.ma.min(self.data_cube) < 0:
                neg = np.abs(np.ma.min(data))
                data = data + np.abs(np.ma.min(data))
            if np.ma.min(self.data_cube) > 0:
                data = data - np.abs(np.ma.min(data))
            neg = neg / np.ma.max(data)
            self.x1 = data / np.ma.max(data)
        else:
            self.x1 = self.data_cube
        # mask negatives
        if self.negative:
            self.x1 = np.ma.array(self.x1, mask=self.x1 < neg)

    def __calc_x_reflectance(self):
        self.x_reflectance = self.x1

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_reflectance_w = np.mean(self.x_reflectance[:, :, wav_lower:wav_upper+1], axis=2)
        else:
            self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength[0]]

        if self.mask is not None:
            mask = np.array([self.mask.T] * 100).T
            self.x_reflectance_masked = np.ma.array(self.x_reflectance[:, :, :], mask=mask)
            # self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(max(0, min(self.wavelength)), 0))
                wav_upper = int(round(min(max(self.wavelength), 99), 0))
                self.x_reflectance_masked_w = np.ma.array(np.mean(self.x_reflectance[:, :, wav_lower:wav_upper+1],
                                                                  axis=2), mask=self.mask)
            else:
                self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)

    def __calc_x2(self):
        self.x2 = -np.ma.log(self.x1)
        self.x2 = np.ma.array(self.x2, mask=~np.isfinite(self.x2))
        neg = 0
        # normalise
        if self.normal and self.absorbance:
            data = self.x2
            if np.ma.min(self.x2) < 0:
                neg = np.abs(np.ma.min(data))
                data = data + np.abs(np.ma.min(data))
            if np.ma.min(self.x2) > 0:
                data = data - np.abs(np.ma.min(data))
            neg = neg / np.ma.max(data)
            self.x2 = data / np.ma.max(data)
        # mask negatives
        if self.negative:
            self.x2 = np.ma.array(self.x2, mask=self.x2 < neg)

    def __calc_x_absorbance(self):
        self.x_absorbance = self.x2

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_absorbance_w = np.mean(self.x_absorbance[:, :, wav_lower:wav_upper+1], axis=2)
        else:
            self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength[0]]

        if self.mask is not None:
            # self.x_absorbance_masked = self.__apply_2DMask_on_3DArray(self.mask, self.x_absorbance)
            mask = np.array([self.mask.T] * 100).T
            self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=mask)
            # self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=np.array([self.mask] * 100))
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(min(0, min(self.wavelength)), 0))
                wav_upper = int(round(max(max(self.wavelength), 99), 0))
                self.x_absorbance_masked_w = np.ma.array(np.mean(self.x_absorbance[:, :, wav_lower:wav_upper+1],
                                                                 axis=2), mask=self.mask)
            else:
                self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength[0]], mask=self.mask)
