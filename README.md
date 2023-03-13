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
- Mellow NF-Crazy Standard Flow Hotend (Mosquitto clone)
- Bondtech LGX Lite

Mods/Deviations (versus a stock build):
- ACM Panels
- 5mm Foam/Foil insulation directly under hotbed to redirect radiated heat back to hotbed.
- 40x40x10 Heatsinks added to A/B Motors (cutouts made in panels to allow natural convection cooling).
- MasturMynd's [Pandora Gantry Mod](https://github.com/MasturMynd/Pandora)
- Custom belted Z (also provides a center rear pi camera)
  - based heavily on Mathematical Potato's [V0.1 Belted Z Drive](https://github.com/VoronDesign/VoronUsers/tree/master/printer_mods/MathematicalPotato/v0.1_belted_z_drive)
- Christoph Muller's [kirigami bed V3](https://github.com/christophmuellerorg/voron_0_kirigami_bed)
  - Upgraded for V0.2 usage using some (unreleased) VOC-only mods
- Thiagolocatelli's [V0 Utility Belt](https://github.com/thiagolocatelli/VoronUsers/tree/master/printer_mods/DoubleT/v0_utility_belt)
- Skuep's [V0 Umbilical Plus](https://github.com/skuep/V0-Umbilical-Plus) update to Timmit99's [V0 Ubilical](https://github.com/timmit99/Voron-Hardware/tree/V0-Umbilical/V0-Umbilical)
- 0ndsk4's [Nevermore Micro V4](https://github.com/0ndsk4/VoronUsers/tree/0ndsk4/printer_mods/0ndsk4/Nevermore_Air_Filter)
- bartlammers' [Disco/Daylight on a Matchstick](https://github.com/VoronDesign/Voron-Hardware/tree/master/Daylight)
- Zruncho's [ZeroClick Bed Probe](https://github.com/zruncho3d/ZeroClick)

Updates:
- Added rear chamber webcam
- Serialized!
- Motion testing complete. Serial requested.
- Inital config. Build in progress.

- - - 
This repo based on f0or1s' [cr10_klipper repo](http://github.com/fl0r1s/cr10_klipper), rpanfili's [voron-ht repo](http://github.com/rpanfili/voron-ht), and Zellneralex's [klipper_config repo](http://github.com/zellneralex/klipper_config) among many others.
It is a work in progress as I keept finding new and better ways to organize/tune my setup.
