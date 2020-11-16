# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os
from datetime import date


class ImageMaker:
    BASE_IMAGE_PATH = {
        "Clear": "./resources/clear_base.jpg",
        "Rain": "./resources/rain_base.jpg",
        "Snow": "./resources/snow_base.jpg",
        "Cloud": "./resources/cloud_base.jpg"
    }

    def __init__(self, date_, weather_type, temperature):
        self.image_path = self.BASE_IMAGE_PATH.get(weather_type)
        self.text = f'{date.isoformat(date_)} {weather_type} {temperature}'

    def write_text(self):
        image = cv.imread(self.image_path)
        font = cv.FONT_HERSHEY_SCRIPT_COMPLEX
        start_pos = (20, 20)
        font_size = 0.55
        color = (219, 112, 147)

        image = cv.putText(image, self.text, start_pos, font, font_size, color, 1)

        self.save_image(image)

    def save_image(self, image):
        filename = self.text.replace(" ", "") + '.jpg'
        dir_path = os.path.join(os.getcwd(), 'results')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        result_path = os.path.join(dir_path, filename)

        cv.imwrite(result_path, image)

    def gradient_settings(self, i):
        SETTINGS = {
            "Clear": (i, 255, 255),
            "Rain": (128 + i // 2, i, i),
            "Snow": (255, i, i),
            "Cloud": (60 + i, 60 + i, 60 + i)
        }
        return SETTINGS

    def gradient(self, weather, base_path, gradient_name):
        image = cv.imread(base_path)
        height, width, channels_no = image.shape

        for i in range(height):
            cv.line(image, (0, i), (width, i), self.gradient_settings(i)[weather], 1)
        cv.imwrite(gradient_name, image)

    # CREATE BLENDING OF GRADIENT AND IMAGE
    def blend_images(self, background, foreground, blend_name):
        background_image = cv.imread(background, -1)
        foreground_image = cv.imread(foreground, -1)

        f_height, f_width, f_channels_no = foreground_image.shape

        # Normalise alpha channel
        alpha = foreground_image[:, :, 2] / 255.0

        background_image = cv.resize(background_image, (f_width, f_height), interpolation=cv.INTER_CUBIC)
        result = np.zeros((f_height, f_width, 3), np.uint8)

        result[:, :, 0] = (1. - alpha) * background_image[:, :, 0] + alpha * foreground_image[:, :, 0]
        result[:, :, 1] = (1. - alpha) * background_image[:, :, 1] + alpha * foreground_image[:, :, 1]
        result[:, :, 2] = (1. - alpha) * background_image[:, :, 2] + alpha * foreground_image[:, :, 2]

        cv.imwrite(blend_name, result)
