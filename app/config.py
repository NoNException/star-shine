import os
import customtkinter as ctk


DATABASE_PATH = os.path.join("data", "user_data.db")


def setup_theme():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
