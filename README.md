# HomeAssistant

This archive contains various blueprints for Home Assistant

|Bluperint|Description|Import|Preview|
|-----------|-----------|-------|----|
|Awtrix Battery Monitor|Monitors the battery status of a mobile device|[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_battery_monitor.yaml)|
|Awtrix Door Status|Icon based monitor for Binary/Sensor (open/close) status monitoring. Generally used for doors and windows|[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_door_status.yaml)  |
|Awtrix HVAC| See the current heating/cooling mode |[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_hvac.yaml)|
| Awtrix Weather | Super weather blueprint - Conditions + Forecast + Sunrise/Set + MoonPhase| [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_weatherflow.yaml) |
| Awtrix Humdiity UV | See Humidity & Current UV Index | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_uv_hum.yaml)|
| Awtrix AQI IQAir | Give current AQI + Forecast | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_aqi.yaml)|
| Awtrix Pollen 🥀️| Parses IQAir's pollen data into a nice picture | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fawtrix_pollen.yaml)|![](./resources/pollen/pollenPreview.gif)|
| Fireplace Sounds | Play a fireplace sound when fireplace is on| [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Ffireplace_sound.yml)|
| Hue Remote | Simulate the state change feature of a hue remote in software | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fhue-dimmer.yaml) |
| Climate Alert | Get an actionable notification if somebody sets the heat too high | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fjeeftor%2FHomeAssistant%2Fmaster%2Fblueprints%2Fautomation%2Fclimate_alert.yaml) |

# Getting the ICONS

```bash
# If you runt his script it will help upload icons to your Awtrix device
bash -c "$(curl -fsSL https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/upload_icon.sh)"

# Or you can run 
bash -c "$(curl -fsSL https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/upload_icon.sh)" -- IP_ADDRESS_OF_CLOCK
```

### Innoveli

It was built out with the following devices:

* Inovelli Red Dimmer
* August SmartLock Pro (zwave)
* MyQ Garage Door opener
* ZwaveJS

In order to set the LEDs i forked scripts from @brianhanifin's [Home-Assistant-Config](https://github.com/brianhanifin/Home-Assistant-Config) repo

<https://my.home-assistant.io/create-link/?redirect=blueprint_import>
