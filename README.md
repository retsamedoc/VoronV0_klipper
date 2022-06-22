# Voron V0.696 Klipper Profile

Software:
- [Raspberry Pi OS Lite "Buster"](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
- [Klipper](https://github.com/KevinOConnor/klipper)
- [Moonraker](https://github.com/Arksine/moonraker)
- [Mainsail](https://github.com/meteyou/mainsail)
- [Crowsnest](https://github.com/mainsail-crew/crowsnest)
- [PrettyGCode](https://github.com/Kragrathea/pgcode)

Hardware:
- Raspberry Pi 4B
- BigTreeTech SKR mini E3 V2.0 Controller

Mods/Deviations (W.R.T. Stock V0.1):
- Changed controller chamber fans to be controlled by each SKR (fans only operate when the drivers are active).
- Cork insulation directly under hotbed to protect electronic chamber from direct/radiated heat.
- Mathematical Potato's [V0.1 Belted Z Drive](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/MathematicalPotato/v0.1_belted_z_drive)
- Ch4relsB's [Slim V0 Handles](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/Ch4rlesB/V0_Handles_Slim)
- Andre's [Neopixel Front Bed Mount](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/Andre/V0_Neopixel_Front_Bed_Mount)
- Andre's [Mini AB ADXL345 Mount](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/Andre/Mini_Afterburner_ADXL345_Mount)
- Thiagolocatelli's [V0 Utility Belt](https://github.com/thiagolocatelli/VoronUsers/tree/master/printer_mods/DoubleT/v0_utility_belt)
- Skuep's [V0 Umbilical Plus](https://github.com/skuep/V0-Umbilical-Plus) update to Timmit99's [V0 Ubilical](https://github.com/timmit99/Voron-Hardware/tree/V0-Umbilical/V0-Umbilical)
- 0ndsk4's [Nevermore Micro V4](https://github.com/0ndsk4/VoronUsers/tree/0ndsk4/printer_mods/0ndsk4/Nevermore_Air_Filter)
- Johannchung's [Raspberry Pi Camera Mount](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/johanncc/Raspberry_Pi_Camera_Mount)

Updates:
- Added rear chamber webcam
- Serialized!
- Motion testing complete. Serial requested.
- Inital config. Build in progress.

- - - 
This repo based on f0or1s' [cr10_klipper repo](http://github.com/fl0r1s/cr10_klipper), rpanfili's [voron-ht repo](http://github.com/rpanfili/voron-ht), and Zellneralex's [klipper_config repo](http://github.com/zellneralex/klipper_config) among many others.
It is a work in progress as I keept finding new and better ways to organize/tune my setup.
