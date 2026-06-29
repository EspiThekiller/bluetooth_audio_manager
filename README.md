# Bluetooth Audio Manager para Home Assistant

Un componente personalizado (Custom Component) para Home Assistant que te permite gestionar, emparejar y conectar dispositivos de audio Bluetooth fácilmente desde la interfaz de Home Assistant. Esta integración soluciona los problemas comunes de audio al conectar altavoces Bluetooth en instalaciones de Home Assistant OS/Supervised, recargando automáticamente el subsistema de audio cuando se conecta un dispositivo.

![Icon](icon.svg)

### 1. Instalar vía HACS
*(Nota: Asegúrate de que tu repositorio en GitHub sea **Público**. Si es privado, HACS no lo encontrará).*

Haz clic en el siguiente botón para abrir HACS y añadir este repositorio a tu Home Assistant. Si el botón te da error, puedes añadir manualmente la URL `https://github.com/EspiThekiller/bluetooth_audio_manager` en HACS (Integraciones > 3 puntitos > Repositorios Personalizados).

[![Añadir repositorio a HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=EspiThekiller&repository=bluetooth_audio_manager&category=integration)

***

### 2. Añadir y Configurar la Integración
Una vez que hayas instalado el componente desde HACS y hayas **reiniciado Home Assistant**, haz clic en el siguiente botón para abrir la configuración y empezar a emparejar tus dispositivos de audio Bluetooth.

[![Configurar Integración](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=bluetooth_audio_manager)

## Características

- **Configuración desde la Interfaz (Config Flow):** Escanea y selecciona fácilmente los dispositivos Bluetooth cercanos desde la pestaña de Integraciones. ¡Sin tocar código YAML!
- **Emparejamiento Automático:** Empareja y da permisos de confianza (trust) de forma automática al dispositivo Bluetooth seleccionado a través de `bluetoothctl`.
- **Interruptor de Conexión:** Crea una entidad de tipo interruptor (switch) para conectar o desconectar manualmente tu dispositivo Bluetooth en cualquier momento.
- **Sensor de Estado:** Crea un sensor binario que monitorea en tiempo real el estado de conectividad del dispositivo.
- **Recarga de Audio Integrada:** Utiliza la API del Supervisor de Home Assistant para recargar el audio automáticamente (`http://supervisor/audio/reload`) al conectarse, asegurando que la salida de sonido pase correctamente al dispositivo Bluetooth.
- **Servicio Personalizado:** Expone el servicio `bluetooth_audio_manager.connect_and_reload`, ideal para ser llamado desde tus automatizaciones y scripts.

## Requisitos Previos

- Home Assistant OS o Home Assistant Supervised (se requiere el `SUPERVISOR_TOKEN` para la recarga del audio).
- El equipo host (donde corre Home Assistant) debe tener capacidades Bluetooth y la herramienta `bluetoothctl` instalada y accesible.

## Instalación Manual

1. Descarga o clona este repositorio.
2. Copia la carpeta `bluetooth_audio_manager` en el directorio `custom_components` de tu instalación de Home Assistant (`/config/custom_components/`).
3. Reinicia Home Assistant.
4. Ve a **Ajustes** > **Dispositivos y servicios** > **Añadir Integración**.
5. Busca "Bluetooth Audio Manager" y sigue las instrucciones en pantalla para escanear y seleccionar tu dispositivo Bluetooth.

## Servicios

### `bluetooth_audio_manager.connect_and_reload`

Se conecta al dispositivo Bluetooth especificado y fuerza una recarga del audio en el Supervisor.

| Atributo | Opcional | Descripción |
| -------- | -------- | ----------- |
| `mac_address` | Sí | La dirección MAC del dispositivo Bluetooth (ej., `00:11:22:33:44:55`). Si se omite, se usará la dirección MAC configurada por defecto en la integración. |

## Entidades Creadas

Por cada dispositivo configurado, se crean las siguientes entidades:
- `switch.<nombre_dispositivo>_connect`: Interruptor para encender o apagar la conexión del dispositivo.
- `binary_sensor.<nombre_dispositivo>_connection`: Indica si el dispositivo está actualmente conectado o no.

*(Nota: Ambas entidades vienen con un icono por defecto de una nota musical `mdi:music-note`).*

## Solución de Problemas

- **No se encuentran dispositivos durante la configuración:** Asegúrate de que el host de Home Assistant tiene el Bluetooth encendido y que el altavoz o auricular que quieres añadir está en modo emparejamiento (pairing).
- **El audio no se recarga tras conectar:** Esta característica requiere Home Assistant OS o Supervised. Si ejecutas Home Assistant en versión Container o Core puro, la API del Supervisor no estará disponible.
