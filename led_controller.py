"""
LED Controller - Современный интерфейс на CustomTkinter
"""

import asyncio
import customtkinter as ctk
from tkinter import colorchooser, messagebox
from bleak import BleakScanner, BleakClient
import threading
from typing import Optional

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LEDController:
    """Класс для управления LED лентой через Bluetooth"""
    
    def __init__(self):
        self.client: Optional[BleakClient] = None
        self.device_address: Optional[str] = None
        self.write_characteristics = []
        self.device_name: str = ""
        
    async def scan_devices(self):
        """Сканирование доступных Bluetooth устройств"""
        devices = await BleakScanner.discover(timeout=10.0)
        return [(d.name or "Unknown", d.address) for d in devices if d.name]
    
    async def connect(self, address: str, device_name: str = ""):
        """Подключение к устройству"""
        try:
            self.client = BleakClient(address)
            await self.client.connect()
            self.device_address = address
            self.device_name = device_name
            
            self.write_characteristics = []
            print(f"\n=== Информация об устройстве ===")
            print(f"Имя: {device_name}")
            print(f"Адрес: {address}")
            
            for service in self.client.services:
                for char in service.characteristics:
                    if "write" in char.properties or "write-without-response" in char.properties:
                        self.write_characteristics.append(char.uuid)
            
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    async def disconnect(self):
        """Отключение от устройства"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
    
    async def send_command(self, data: bytearray):
        """Отправка команды"""
        if not self.client or not self.client.is_connected:
            return False
        
        for char_uuid in self.write_characteristics:
            try:
                await self.client.write_gatt_char(char_uuid, data, response=False)
                return True
            except:
                pass
        return False
    
    async def send_color(self, r: int, g: int, b: int):
        """Отправка цвета на ленту"""
        data = bytearray([0x7E, 0x07, 0x05, 0x03, r, g, b, 0x10, 0xEF])
        return await self.send_command(data)
    
    async def set_brightness(self, brightness: int):
        """Установка яркости (0-100)"""
        brightness_val = int(brightness * 0.64)
        if brightness_val > 64:
            brightness_val = 64
        data = bytearray([0x7E, 0x04, 0x01, brightness_val, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        return await self.send_command(data)
    
    async def power_on(self):
        """Включение ленты"""
        data = bytearray([0x7E, 0x04, 0x04, 0x01, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        return await self.send_command(data)
    
    async def power_off(self):
        """Выключение ленты"""
        data = bytearray([0x7E, 0x04, 0x04, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        return await self.send_command(data)


class LEDControllerApp:
    """Современный GUI на CustomTkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LED Controller")
        self.root.geometry("700x900")
        
        self.controller = LEDController()
        self.loop = asyncio.new_event_loop()
        self.current_color = (255, 255, 255)
        self.selected_device_idx = None
        
        self.create_ui()
        
        # Запуск asyncio
        self.thread = threading.Thread(target=self.run_asyncio_loop, daemon=True)
        self.thread.start()
    
    def run_asyncio_loop(self):
        """Запуск asyncio event loop"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def create_ui(self):
        """Создание интерфейса"""
        
        # Заголовок
        header = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, 
                    text="💡 LED Controller",
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=25)
        
        # Основной контейнер со скроллом
        container = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Панель подключения
        self.create_connection_panel(container)
        
        # Панель управления цветом
        self.create_color_panel(container)
        
        # Панель управления
        self.create_control_panel(container)
    
    def create_connection_panel(self, parent):
        """Панель подключения к устройству"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 15))
        
        # Заголовок
        ctk.CTkLabel(frame, 
                    text="🔗 Подключение",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Список устройств (контейнер для radiobuttons)
        self.device_list_frame = ctk.CTkScrollableFrame(frame, 
                                                        height=100,
                                                        fg_color="#2b2b2b")
        self.device_list_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Заглушка когда нет устройств
        self.no_devices_label = ctk.CTkLabel(self.device_list_frame,
                                            text="Нажмите 'Сканировать' для поиска устройств...",
                                            font=ctk.CTkFont(size=11),
                                            text_color="gray")
        self.no_devices_label.pack(pady=20)
        
        self.device_radio_var = ctk.IntVar(value=-1)
        
        # Кнопки
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.scan_btn = ctk.CTkButton(btn_frame, 
                                     text="🔍 Сканировать",
                                     command=self.scan_devices,
                                     height=35,
                                     font=ctk.CTkFont(size=13))
        self.scan_btn.pack(side="left", padx=(0, 10))
        
        self.connect_btn = ctk.CTkButton(btn_frame, 
                                        text="⚡ Подключить",
                                        command=self.connect_device,
                                        height=35,
                                        font=ctk.CTkFont(size=13))
        self.connect_btn.pack(side="left", padx=(0, 10))
        
        self.disconnect_btn = ctk.CTkButton(btn_frame, 
                                           text="❌ Отключить",
                                           command=self.disconnect_device,
                                           height=35,
                                           fg_color="#dc3545",
                                           hover_color="#c82333",
                                           font=ctk.CTkFont(size=13),
                                           state="disabled")
        self.disconnect_btn.pack(side="left")
        
        # Статус
        self.status_label = ctk.CTkLabel(frame, 
                                        text="● Не подключено",
                                        font=ctk.CTkFont(size=12),
                                        text_color="#dc3545")
        self.status_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        self.devices = []
    
    def create_color_panel(self, parent):
        """Панель выбора цвета"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Заголовок
        ctk.CTkLabel(frame, 
                    text="🎨 Выбор цвета",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Контейнер для превью и слайдеров
        color_container = ctk.CTkFrame(frame, fg_color="transparent")
        color_container.pack(fill="both", expand=True, padx=15)
        
        # Левая часть - превью
        left_frame = ctk.CTkFrame(color_container, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=(0, 15))
        
        ctk.CTkLabel(left_frame, 
                    text="Превью",
                    font=ctk.CTkFont(size=12)).pack(pady=(0, 10))
        
        self.color_preview = ctk.CTkFrame(left_frame, 
                                         width=180, 
                                         height=180,
                                         fg_color="#FFFFFF",
                                         corner_radius=10)
        self.color_preview.pack()
        self.color_preview.pack_propagate(False)
        
        self.hex_label = ctk.CTkLabel(left_frame, 
                                     text="#FFFFFF",
                                     font=ctk.CTkFont(size=16, weight="bold"))
        self.hex_label.pack(pady=(10, 0))
        
        # Правая часть - слайдеры RGB
        right_frame = ctk.CTkFrame(color_container, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True)
        
        self.rgb_sliders = {}
        colors = [('R', '#ff4444'), ('G', '#44ff44'), ('B', '#4444ff')]
        
        for i, (label, color) in enumerate(colors):
            slider_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            slider_frame.pack(fill="x", pady=10)
            
            # Заголовок слайдера
            header_frame = ctk.CTkFrame(slider_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(header_frame, 
                        text=label,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=color).pack(side="left")
            
            value_label = ctk.CTkLabel(header_frame, 
                                      text="255",
                                      font=ctk.CTkFont(size=13),
                                      width=40)
            value_label.pack(side="right")
            
            # Слайдер
            slider = ctk.CTkSlider(slider_frame,
                                  from_=0,
                                  to=255,
                                  number_of_steps=255,
                                  command=lambda v, lbl=value_label, idx=i: self.on_rgb_change(v, lbl, idx),
                                  state="disabled")
            slider.set(255)
            slider.pack(fill="x")
            
            self.rgb_sliders[label] = (slider, value_label)
        
        # Кнопка выбора цвета
        color_btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        color_btn_frame.pack(fill="x", padx=15, pady=(10, 0))
        
        self.color_picker_btn = ctk.CTkButton(color_btn_frame,
                                             text="🎨 Выбрать из палитры",
                                             command=self.choose_color,
                                             height=35,
                                             state="disabled")
        self.color_picker_btn.pack(side="left", padx=(0, 10))
        
        # Быстрые пресеты
        ctk.CTkLabel(frame, 
                    text="Быстрый выбор",
                    font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=(15, 5))
        
        preset_frame = ctk.CTkFrame(frame, fg_color="transparent")
        preset_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        presets = [
            ("Красный", "#FF0000"),
            ("Зеленый", "#00FF00"),
            ("Синий", "#0000FF"),
            ("Желтый", "#FFFF00"),
            ("Фиолетовый", "#FF00FF"),
            ("Голубой", "#00FFFF"),
            ("Белый", "#FFFFFF"),
            ("Оранжевый", "#FF8800")
        ]
        
        self.preset_buttons = []
        for i, (name, color) in enumerate(presets):
            btn = ctk.CTkButton(preset_frame,
                              text="",
                              width=60,
                              height=30,
                              fg_color=color,
                              hover_color=color,
                              command=lambda c=color: self.set_preset_color(c),
                              state="disabled")
            btn.grid(row=0, column=i, padx=3)
            self.preset_buttons.append(btn)
    
    def create_control_panel(self, parent):
        """Панель управления яркостью и питанием"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x")
        
        # Заголовок
        ctk.CTkLabel(frame, 
                    text="⚙️ Управление",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Яркость
        brightness_frame = ctk.CTkFrame(frame, fg_color="transparent")
        brightness_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        header_frame = ctk.CTkFrame(brightness_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(header_frame, 
                    text="💡 Яркость",
                    font=ctk.CTkFont(size=14)).pack(side="left")
        
        self.brightness_value = ctk.CTkLabel(header_frame, 
                                            text="100%",
                                            font=ctk.CTkFont(size=13))
        self.brightness_value.pack(side="right")
        
        self.brightness_slider = ctk.CTkSlider(brightness_frame,
                                              from_=0,
                                              to=100,
                                              number_of_steps=100,
                                              command=self.on_brightness_change,
                                              state="disabled")
        self.brightness_slider.set(100)
        self.brightness_slider.pack(fill="x")
        
        # Кнопки питания
        power_frame = ctk.CTkFrame(frame, fg_color="transparent")
        power_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.power_on_btn = ctk.CTkButton(power_frame,
                                         text="⚡ Включить",
                                         command=self.power_on,
                                         height=40,
                                         fg_color="#28a745",
                                         hover_color="#218838",
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         state="disabled")
        self.power_on_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.power_off_btn = ctk.CTkButton(power_frame,
                                          text="🔌 Выключить",
                                          command=self.power_off,
                                          height=40,
                                          fg_color="#dc3545",
                                          hover_color="#c82333",
                                          font=ctk.CTkFont(size=14, weight="bold"),
                                          state="disabled")
        self.power_off_btn.pack(side="left", fill="x", expand=True)
    
    def on_rgb_change(self, value, label, index):
        """Изменение RGB слайдера"""
        value = int(value)
        label.configure(text=str(value))
        
        # Обновляем текущий цвет
        colors = list(self.current_color)
        colors[index] = value
        self.current_color = tuple(colors)
        
        # Обновляем превью
        self.update_color_preview()
        
        # Отправляем на ленту
        asyncio.run_coroutine_threadsafe(
            self.controller.send_color(*self.current_color), self.loop
        )
    
    def on_brightness_change(self, value):
        """Изменение яркости"""
        value = int(value)
        self.brightness_value.configure(text=f"{value}%")
        
        asyncio.run_coroutine_threadsafe(
            self.controller.set_brightness(value), self.loop
        )
    
    def update_color_preview(self):
        """Обновление превью цвета"""
        hex_color = '#{:02x}{:02x}{:02x}'.format(*self.current_color)
        self.color_preview.configure(fg_color=hex_color)
        self.hex_label.configure(text=hex_color.upper())
    
    def choose_color(self):
        """Выбор цвета через палитру"""
        color = colorchooser.askcolor(title="Выберите цвет")
        if color[0]:
            r, g, b = map(int, color[0])
            self.set_color(r, g, b)
    
    def set_preset_color(self, hex_color):
        """Установка пресета"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        self.set_color(r, g, b)
    
    def set_color(self, r, g, b):
        """Установка цвета"""
        self.current_color = (r, g, b)
        
        # Обновляем слайдеры
        self.rgb_sliders['R'][0].set(r)
        self.rgb_sliders['G'][0].set(g)
        self.rgb_sliders['B'][0].set(b)
        
        self.rgb_sliders['R'][1].configure(text=str(r))
        self.rgb_sliders['G'][1].configure(text=str(g))
        self.rgb_sliders['B'][1].configure(text=str(b))
        
        # Обновляем превью
        self.update_color_preview()
        
        # Отправляем на ленту
        asyncio.run_coroutine_threadsafe(
            self.controller.send_color(r, g, b), self.loop
        )
    
    def scan_devices(self):
        """Сканирование устройств"""
        # Очищаем список
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()
        
        # Показываем статус сканирования
        scanning_label = ctk.CTkLabel(self.device_list_frame,
                                     text="⏳ Сканирование устройств...",
                                     font=ctk.CTkFont(size=11))
        scanning_label.pack(pady=20)
        
        self.scan_btn.configure(state="disabled")
        self.selected_device_idx = None
        
        def scan():
            devices = asyncio.run_coroutine_threadsafe(
                self.controller.scan_devices(), self.loop
            ).result()
            self.root.after(0, self.update_device_list, devices)
        
        threading.Thread(target=scan, daemon=True).start()
    
    def update_device_list(self, devices):
        """Обновление списка устройств"""
        self.devices = devices
        
        # Очищаем список
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()
        
        if not devices:
            no_dev_label = ctk.CTkLabel(self.device_list_frame,
                                       text="❌ Устройства не найдены",
                                       font=ctk.CTkFont(size=11),
                                       text_color="#dc3545")
            no_dev_label.pack(pady=20)
        else:
            # Создаем список кнопок устройств
            self.device_radio_var.set(-1)
            self.device_buttons = []
            
            for i, (name, address) in enumerate(devices):
                # Создаем кнопку для каждого устройства
                btn = ctk.CTkButton(self.device_list_frame,
                                   text=f"📱 {name}\n    {address}",
                                   font=ctk.CTkFont(size=11),
                                   height=60,
                                   anchor="w",
                                   fg_color="#2b2b2b",
                                   hover_color="#3a3a3a",
                                   border_width=2,
                                   border_color="#3a3a3a",
                                   command=lambda idx=i: self.select_device(idx))
                btn.pack(fill="x", padx=5, pady=3)
                self.device_buttons.append(btn)
        
        self.scan_btn.configure(state="normal")
    
    def select_device(self, idx):
        """Выбор устройства из списка"""
        self.selected_device_idx = idx
        
        # Обновляем визуальное состояние кнопок
        for i, btn in enumerate(self.device_buttons):
            if i == idx:
                # Выбранное устройство - подсвечиваем
                btn.configure(fg_color="#1f6feb", 
                            border_color="#1f6feb",
                            text_color="white")
            else:
                # Остальные - обычный стиль
                btn.configure(fg_color="#2b2b2b", 
                            border_color="#3a3a3a",
                            text_color="white")
    
    def connect_device(self):
        """Подключение к устройству"""
        if not self.devices:
            messagebox.showwarning("Внимание", "Сначала просканируйте устройства")
            return
        
        if self.selected_device_idx is None:
            messagebox.showwarning("Внимание", "Выберите устройство из списка")
            return
        
        device_name, address = self.devices[self.selected_device_idx]
        
        self.status_label.configure(text="● Подключение...", text_color="#ffc107")
        self.connect_btn.configure(state="disabled")
        
        def connect():
            success = asyncio.run_coroutine_threadsafe(
                self.controller.connect(address, device_name), self.loop
            ).result()
            self.root.after(0, self.on_connection_result, success)
        
        threading.Thread(target=connect, daemon=True).start()
    
    def on_connection_result(self, success):
        """Результат подключения"""
        if success:
            self.status_label.configure(text="● Подключено ✓", text_color="#28a745")
            self.disconnect_btn.configure(state="normal")
            
            # Включаем все элементы управления
            for slider, _ in self.rgb_sliders.values():
                slider.configure(state="normal")
            
            self.brightness_slider.configure(state="normal")
            self.color_picker_btn.configure(state="normal")
            self.power_on_btn.configure(state="normal")
            self.power_off_btn.configure(state="normal")
            
            for btn in self.preset_buttons:
                btn.configure(state="normal")
        else:
            self.status_label.configure(text="● Ошибка подключения", text_color="#dc3545")
            self.connect_btn.configure(state="normal")
            messagebox.showerror("Ошибка", "Не удалось подключиться к устройству")
    
    def disconnect_device(self):
        """Отключение от устройства"""
        asyncio.run_coroutine_threadsafe(self.controller.disconnect(), self.loop)
        
        self.status_label.configure(text="● Не подключено", text_color="#dc3545")
        self.connect_btn.configure(state="normal")
        self.disconnect_btn.configure(state="disabled")
        
        # Отключаем все элементы управления
        for slider, _ in self.rgb_sliders.values():
            slider.configure(state="disabled")
        
        self.brightness_slider.configure(state="disabled")
        self.color_picker_btn.configure(state="disabled")
        self.power_on_btn.configure(state="disabled")
        self.power_off_btn.configure(state="disabled")
        
        for btn in self.preset_buttons:
            btn.configure(state="disabled")
    
    def power_on(self):
        """Включение ленты"""
        asyncio.run_coroutine_threadsafe(self.controller.power_on(), self.loop)
    
    def power_off(self):
        """Выключение ленты"""
        asyncio.run_coroutine_threadsafe(self.controller.power_off(), self.loop)


def main():
    root = ctk.CTk()
    app = LEDControllerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
