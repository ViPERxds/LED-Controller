"""
Модуль с протоколами для различных типов LED лент
Добавляйте свои протоколы или модифицируйте существующие
"""

from typing import Dict, Callable
import struct


class LEDProtocol:
    """Базовый класс для протоколов LED лент"""
    
    def __init__(self, name: str):
        self.name = name
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Генерация команды для установки цвета"""
        raise NotImplementedError
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Генерация команды для установки яркости"""
        raise NotImplementedError
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        raise NotImplementedError
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        raise NotImplementedError


class GenericProtocol(LEDProtocol):
    """
    Универсальный протокол для большинства китайских LED лент
    Совместим с: ELK-BLEDOM, Magic Home, Happy Lighting, и др.
    """
    
    def __init__(self):
        super().__init__("Generic/Universal")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Формат: [0x56, R, G, B, 0x00, 0xF0, 0xAA]"""
        return bytearray([0x56, r, g, b, 0x00, 0xF0, 0xAA])
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Формат: [0x56, brightness, 0x00, 0x00, 0x00, 0xF0, 0xAA]"""
        return bytearray([0x56, brightness, 0x00, 0x00, 0x00, 0xF0, 0xAA])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0xCC, 0x23, 0x33])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0xCC, 0x24, 0x33])


class MagicHomeProtocol(LEDProtocol):
    """
    Протокол для Magic Home LED контроллеров
    Совместим с: Magic Home, Magic Hue, Flux LED
    """
    
    def __init__(self):
        super().__init__("Magic Home")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Формат: [0x31, R, G, B, 0x00, 0xF0, 0x0F, checksum]"""
        data = [0x31, r, g, b, 0x00, 0xF0, 0x0F]
        checksum = sum(data) & 0xFF
        return bytearray(data + [checksum])
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Установка яркости через изменение белого канала"""
        return bytearray([0x31, 0x00, 0x00, 0x00, brightness, 0x0F, 0x0F])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0x71, 0x23, 0x0F])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0x71, 0x24, 0x0F])


class GoveeProtocol(LEDProtocol):
    """
    Протокол для Govee LED лент
    Совместим с: Govee H6127, H6159, и другие BLE модели
    """
    
    def __init__(self):
        super().__init__("Govee")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Формат Govee: [0x33, 0x05, 0x02, R, G, B, 0x00, ...checksum]"""
        data = [0x33, 0x05, 0x02, r, g, b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        checksum = sum(data) & 0xFF
        return bytearray(data + [checksum])
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Установка яркости"""
        data = [0x33, 0x04, brightness, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        checksum = sum(data) & 0xFF
        return bytearray(data + [checksum])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0x33, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x35])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0x33, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x34])


class YeelightProtocol(LEDProtocol):
    """
    Протокол для Yeelight LED устройств
    Совместим с: Yeelight LED Strip, Yeelight Bulb (BLE версии)
    """
    
    def __init__(self):
        super().__init__("Yeelight")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Yeelight использует 32-bit RGB значение"""
        rgb_value = (r << 16) + (g << 8) + b
        return bytearray([0x43, 0x01, 0x02] + list(struct.pack('>I', rgb_value)))
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Яркость в процентах"""
        return bytearray([0x43, 0x02, brightness])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0x43, 0x40, 0x01])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0x43, 0x40, 0x02])


class TrLifeProtocol(LEDProtocol):
    """
    Протокол для Triones/Tr-Life LED контроллеров
    Совместим с: Triones, Happy Lighting, iDual
    """
    
    def __init__(self):
        super().__init__("Triones/TrLife")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Формат: [0x56, R, G, B, 0x00, 0xF0, 0xAA]"""
        return bytearray([0x56, r, g, b, 0x00, 0xF0, 0xAA])
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Яркость через модификацию цвета"""
        return bytearray([0x56, brightness, brightness, brightness, 0x00, 0xF0, 0xAA])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0xCC, 0x23, 0x33])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0xCC, 0x24, 0x33])


class ZenggeProtocol(LEDProtocol):
    """
    Протокол для Zengge LED устройств
    Совместим с: Zengge, LEDnet WF
    """
    
    def __init__(self):
        super().__init__("Zengge")
    
    def color_command(self, r: int, g: int, b: int) -> bytearray:
        """Формат с контрольной суммой"""
        return bytearray([0x7E, 0x00, 0x05, 0x03, r, g, b, 0x00, 0xEF])
    
    def brightness_command(self, brightness: int) -> bytearray:
        """Установка яркости"""
        return bytearray([0x7E, 0x00, 0x01, brightness, 0x00, 0x00, 0x00, 0x00, 0xEF])
    
    def power_on_command(self) -> bytearray:
        """Команда включения"""
        return bytearray([0x7E, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF])
    
    def power_off_command(self) -> bytearray:
        """Команда выключения"""
        return bytearray([0x7E, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF])


# Реестр протоколов
PROTOCOLS: Dict[str, LEDProtocol] = {
    "Generic": GenericProtocol(),
    "Magic Home": MagicHomeProtocol(),
    "Govee": GoveeProtocol(),
    "Yeelight": YeelightProtocol(),
    "Triones": TrLifeProtocol(),
    "Zengge": ZenggeProtocol(),
}


def get_protocol(name: str) -> LEDProtocol:
    """Получить протокол по имени"""
    return PROTOCOLS.get(name, GenericProtocol())


def list_protocols() -> list:
    """Список доступных протоколов"""
    return list(PROTOCOLS.keys())


# Функции для определения протокола по имени устройства
def detect_protocol_by_name(device_name: str) -> LEDProtocol:
    """
    Автоматическое определение протокола по имени устройства
    
    Args:
        device_name: Имя Bluetooth устройства
    
    Returns:
        Подходящий протокол или Generic по умолчанию
    """
    device_name = device_name.lower()
    
    # Govee
    if any(keyword in device_name for keyword in ['govee', 'h6', 'igovi']):
        return PROTOCOLS["Govee"]
    
    # Magic Home
    if any(keyword in device_name for keyword in ['magic', 'flux', 'hue']):
        return PROTOCOLS["Magic Home"]
    
    # Yeelight
    if any(keyword in device_name for keyword in ['yeelight', 'yee']):
        return PROTOCOLS["Yeelight"]
    
    # Triones
    if any(keyword in device_name for keyword in ['triones', 'happy', 'idual']):
        return PROTOCOLS["Triones"]
    
    # Zengge
    if any(keyword in device_name for keyword in ['zengge', 'lednet']):
        return PROTOCOLS["Zengge"]
    
    # ELK-BLEDOM и другие популярные китайские ленты
    if any(keyword in device_name for keyword in ['elk', 'bledom', 'ble', 'led']):
        return PROTOCOLS["Generic"]
    
    # По умолчанию
    return GenericProtocol()


# Примеры использования:
"""
# Использование конкретного протокола
protocol = get_protocol("Magic Home")
color_data = protocol.color_command(255, 0, 0)  # Красный цвет

# Автоматическое определение
protocol = detect_protocol_by_name("ELK-BLEDOM")
color_data = protocol.color_command(0, 255, 0)  # Зеленый цвет

# Список всех протоколов
available = list_protocols()
print(available)
"""

