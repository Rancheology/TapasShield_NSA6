import os
import subprocess

MODELS_DIR = os.path.abspath("hardware/3d_models").replace("\\", "/")
os.makedirs(MODELS_DIR, exist_ok=True)

def write_vrml(filename, content):
    path = os.path.join(MODELS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[OK] Wrote {filename}")

# 1. terminal_2p_508.wrl (Phoenix Contact MKDS 2-pin 5.08mm)
# Size: X=8.5 (depth), Y=10.16 (width for 2 pins at -2.54 and +2.54), Z=10.0 (height)
write_vrml("terminal_2p_508.wrl", """#VRML V2.0 utf8
# Phoenix MKDS 1,5/ 2-5,08 Terminal Block (Industrial Green)
Transform {
  children [
    # Main Housing (Green)
    Transform {
      translation 0 0 5.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.0 0.55 0.25
              specularColor 0.2 0.3 0.2
              shininess 0.25
            }
          }
          geometry Box { size 8.5 10.16 10.0 }
        }
      ]
    }
    # Wire Entry Cavity 1 (Left / Front)
    Transform {
      translation -4.0 -2.54 3.5
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.08 0.08 0.08 }
          }
          geometry Box { size 1.0 3.2 3.2 }
        }
      ]
    }
    # Wire Entry Cavity 2
    Transform {
      translation -4.0 2.54 3.5
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.08 0.08 0.08 }
          }
          geometry Box { size 1.0 3.2 3.2 }
        }
      ]
    }
    # Top Screw 1 (Silver)
    Transform {
      translation 0.5 -2.54 10.05
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.85 0.88
              specularColor 0.95 0.95 0.95
              shininess 0.9
            }
          }
          geometry Cylinder { radius 1.6 height 0.2 }
        }
      ]
    }
    # Top Screw 2 (Silver)
    Transform {
      translation 0.5 2.54 10.05
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.85 0.88
              specularColor 0.95 0.95 0.95
              shininess 0.9
            }
          }
          geometry Cylinder { radius 1.6 height 0.2 }
        }
      ]
    }
    # Screw 1 Slot (Dark)
    Transform {
      translation 0.5 -2.54 10.16
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.1 0.1 0.1 } }
          geometry Box { size 0.5 2.6 0.1 }
        }
      ]
    }
    # Screw 2 Slot (Dark)
    Transform {
      translation 0.5 2.54 10.16
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.1 0.1 0.1 } }
          geometry Box { size 0.5 2.6 0.1 }
        }
      ]
    }
    # Solder Pin 1 (THT)
    Transform {
      translation 0 -2.54 -1.8
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.8 0.8 0.85 shininess 0.8 } }
          geometry Cylinder { radius 0.5 height 3.6 }
        }
      ]
    }
    # Solder Pin 2 (THT)
    Transform {
      translation 0 2.54 -1.8
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.8 0.8 0.85 shininess 0.8 } }
          geometry Cylinder { radius 0.5 height 3.6 }
        }
      ]
    }
  ]
}
""")

# 2. esp32_s3_wroom.wrl (ESP32-S3-WROOM-1 Module)
# Size: X=18.0, Y=25.5, Z=3.2
write_vrml("esp32_s3_wroom.wrl", """#VRML V2.0 utf8
# ESP32-S3-WROOM-1 3D Model with Metallic Shield Can & PCB Antenna
Transform {
  children [
    # FR4 Substrate (Dark Industrial Green)
    Transform {
      translation 0 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.05 0.28 0.12
              specularColor 0.15 0.2 0.15
              shininess 0.2
            }
          }
          geometry Box { size 18.0 25.5 0.8 }
        }
      ]
    }
    # Brushed Silver Metallic RF Shield Can
    Transform {
      translation 0 2.8 2.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.82 0.84 0.86
              specularColor 0.95 0.95 0.98
              shininess 0.85
            }
          }
          geometry Box { size 16.0 17.5 2.4 }
        }
      ]
    }
    # ESP32-S3 Chip Core Mark
    Transform {
      translation 0 2.8 3.22
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.3 0.3 0.32 }
          }
          geometry Box { size 5.0 5.0 0.05 }
        }
      ]
    }
    # PCB Inverted-F Antenna Traces (Copper Gold on Top End Y = -9.5)
    Transform {
      translation 0 -9.5 0.83
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.65 0.15
              specularColor 0.9 0.8 0.3
              shininess 0.75
            }
          }
          geometry Box { size 14.0 4.0 0.06 }
        }
      ]
    }
    # Antenna Meander Slot 1
    Transform {
      translation -3.5 -9.5 0.84
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.05 0.28 0.12 } }
          geometry Box { size 1.0 3.0 0.08 }
        }
      ]
    }
    # Antenna Meander Slot 2
    Transform {
      translation 1.5 -9.5 0.84
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.05 0.28 0.12 } }
          geometry Box { size 1.0 3.0 0.08 }
        }
      ]
    }
  ]
}
""")

# 3. soic8.wrl (ATECC608B SOIC-8)
write_vrml("soic8.wrl", """#VRML V2.0 utf8
# SOIC-8 Molded Epoxy IC Package
Transform {
  children [
    # IC Body
    Transform {
      translation 0 0 0.95
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.12 0.12 0.14
              specularColor 0.2 0.2 0.2
              shininess 0.15
            }
          }
          geometry Box { size 3.9 4.9 1.5 }
        }
      ]
    }
    # Pin 1 Polarity Dot
    Transform {
      translation -1.2 -1.8 1.72
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.8 0.8 0.8 } }
          geometry Cylinder { radius 0.25 height 0.06 }
        }
      ]
    }
    # Left Lead Frame
    Transform {
      translation -2.25 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.9 4.2 0.3 }
        }
      ]
    }
    # Right Lead Frame
    Transform {
      translation 2.25 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.9 4.2 0.3 }
        }
      ]
    }
  ]
}
""")

# 4. msop10.wrl (ADS1115 MSOP-10)
write_vrml("msop10.wrl", """#VRML V2.0 utf8
# MSOP-10 Molded Epoxy IC Package
Transform {
  children [
    # IC Body
    Transform {
      translation 0 0 0.6
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.12 0.12 0.14
              specularColor 0.2 0.2 0.2
              shininess 0.15
            }
          }
          geometry Box { size 3.0 3.0 1.0 }
        }
      ]
    }
    # Pin 1 Dot
    Transform {
      translation -0.9 -0.9 1.12
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.8 0.8 0.8 } }
          geometry Cylinder { radius 0.2 height 0.05 }
        }
      ]
    }
    # Left Leads
    Transform {
      translation -1.85 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.8 2.6 0.2 }
        }
      ]
    }
    # Right Leads
    Transform {
      translation 1.85 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.8 2.6 0.2 }
        }
      ]
    }
  ]
}
""")

# 5. sot23_6.wrl (TPS54302 SOT-23-6)
write_vrml("sot23_6.wrl", """#VRML V2.0 utf8
# SOT-23-6 IC Package
Transform {
  children [
    Transform {
      translation 0 0 0.65
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.12 0.12 0.14 specularColor 0.2 0.2 0.2 shininess 0.15 }
          }
          geometry Box { size 1.6 2.9 1.1 }
        }
      ]
    }
    Transform {
      translation -1.0 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 2.4 0.2 }
        }
      ]
    }
    Transform {
      translation 1.0 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 2.4 0.2 }
        }
      ]
    }
  ]
}
""")

# 6. sot23_5.wrl (AP2112K SOT-23-5)
write_vrml("sot23_5.wrl", """#VRML V2.0 utf8
# SOT-23-5 LDO Package
Transform {
  children [
    Transform {
      translation 0 0 0.65
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.12 0.12 0.14 specularColor 0.2 0.2 0.2 shininess 0.15 }
          }
          geometry Box { size 1.6 2.9 1.1 }
        }
      ]
    }
    Transform {
      translation -1.0 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 2.4 0.2 }
        }
      ]
    }
    Transform {
      translation 1.0 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 2.0 0.2 }
        }
      ]
    }
  ]
}
""")

# 7. sma_diode.wrl (SMAJ28CA TVS Diode, DO-214AC)
write_vrml("sma_diode.wrl", """#VRML V2.0 utf8
# DO-214AC (SMA) Molded Diode Package
Transform {
  children [
    # Molded Body
    Transform {
      translation 0 0 1.15
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.14 0.14 0.16 specularColor 0.2 0.2 0.2 shininess 0.2 }
          }
          geometry Box { size 2.6 4.3 2.1 }
        }
      ]
    }
    # Cathode Band (Silver)
    Transform {
      translation 0 -1.2 2.22
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 2.6 0.5 0.05 }
        }
      ]
    }
    # End Leads
    Transform {
      translation 0 -2.2 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 1.6 0.8 0.4 }
        }
      ]
    }
    Transform {
      translation 0 2.2 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 1.6 0.8 0.4 }
        }
      ]
    }
  ]
}
""")

# 8. smc_diode.wrl (B540C Schottky, DO-214AB)
write_vrml("smc_diode.wrl", """#VRML V2.0 utf8
# DO-214AB (SMC) Power Diode Package
Transform {
  children [
    Transform {
      translation 0 0 1.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.14 0.14 0.16 specularColor 0.2 0.2 0.2 shininess 0.2 }
          }
          geometry Box { size 3.6 6.8 2.3 }
        }
      ]
    }
    Transform {
      translation 0 -2.0 2.42
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 3.6 0.7 0.05 }
        }
      ]
    }
    Transform {
      translation 0 -3.4 0.45
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 2.2 1.0 0.5 }
        }
      ]
    }
    Transform {
      translation 0 3.4 0.45
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 2.2 1.0 0.5 }
        }
      ]
    }
  ]
}
""")

# 9. inductor_7x7.wrl (10µH Power Inductor)
write_vrml("inductor_7x7.wrl", """#VRML V2.0 utf8
# 7.3x7.3mm Shielded Power Inductor
Transform {
  children [
    # Ferrite Body (Dark Charcoal)
    Transform {
      translation 0 0 2.1
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.22 0.22 0.25 specularColor 0.35 0.35 0.4 shininess 0.3 }
          }
          geometry Box { size 7.3 7.3 4.2 }
        }
      ]
    }
    # Terminal Electrode 1
    Transform {
      translation -3.5 0 1.0
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 5.0 2.0 }
        }
      ]
    }
    # Terminal Electrode 2
    Transform {
      translation 3.5 0 1.0
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.6 5.0 2.0 }
        }
      ]
    }
  ]
}
""")

# 10. smd_0805_r.wrl (0805 Resistor)
write_vrml("smd_0805_r.wrl", """#VRML V2.0 utf8
# SMD 0805 Resistor
Transform {
  children [
    # Black Resistive Body
    Transform {
      translation 0 0 0.3
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.1 0.1 0.1 specularColor 0.2 0.2 0.2 shininess 0.2 }
          }
          geometry Box { size 1.3 1.25 0.55 }
        }
      ]
    }
    # Endcap 1 (Silver)
    Transform {
      translation -0.85 0 0.3
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.4 1.25 0.55 }
        }
      ]
    }
    # Endcap 2 (Silver)
    Transform {
      translation 0.85 0 0.3
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.4 1.25 0.55 }
        }
      ]
    }
  ]
}
""")

# 11. smd_0603_r.wrl (0603 Resistor)
write_vrml("smd_0603_r.wrl", """#VRML V2.0 utf8
# SMD 0603 Resistor
Transform {
  children [
    Transform {
      translation 0 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.1 0.1 0.1 specularColor 0.2 0.2 0.2 shininess 0.2 }
          }
          geometry Box { size 1.0 0.8 0.45 }
        }
      ]
    }
    Transform {
      translation -0.65 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.3 0.8 0.45 }
        }
      ]
    }
    Transform {
      translation 0.65 0 0.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.3 0.8 0.45 }
        }
      ]
    }
  ]
}
""")

# 12. smd_0603_c.wrl (0603 MLCC Capacitor, Ceramic Tan)
write_vrml("smd_0603_c.wrl", """#VRML V2.0 utf8
# SMD 0603 MLCC Ceramic Capacitor
Transform {
  children [
    # Ceramic Body (Tan/Beige)
    Transform {
      translation 0 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.76 0.60 0.42
              specularColor 0.3 0.25 0.2
              shininess 0.2
            }
          }
          geometry Box { size 1.0 0.8 0.8 }
        }
      ]
    }
    Transform {
      translation -0.65 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.3 0.8 0.8 }
        }
      ]
    }
    Transform {
      translation 0.65 0 0.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.85 0.85 0.88 specularColor 0.9 0.9 0.9 shininess 0.9 }
          }
          geometry Box { size 0.3 0.8 0.8 }
        }
      ]
    }
  ]
}
""")

# 13. led_0805_green.wrl (Emerald LED)
write_vrml("led_0805_green.wrl", """#VRML V2.0 utf8
# SMD 0805 Emerald Green LED
Transform {
  children [
    # White Base Carrier
    Transform {
      translation 0 0 0.15
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.92 0.92 0.92 specularColor 0.3 0.3 0.3 shininess 0.2 }
          }
          geometry Box { size 2.0 1.25 0.3 }
        }
      ]
    }
    # Translucent Emerald Green Lens
    Transform {
      translation 0 0 0.58
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.05 0.85 0.25
              emissiveColor 0.02 0.4 0.1
              specularColor 0.3 0.9 0.4
              transparency 0.35
              shininess 0.9
            }
          }
          geometry Box { size 1.3 0.9 0.55 }
        }
      ]
    }
    # Silver Endpads
    Transform {
      translation -0.85 0 0.15
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.3 1.25 0.3 }
        }
      ]
    }
    Transform {
      translation 0.85 0 0.15
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.3 1.25 0.3 }
        }
      ]
    }
  ]
}
""")

# 14. led_0805_red.wrl (Crimson LED)
write_vrml("led_0805_red.wrl", """#VRML V2.0 utf8
# SMD 0805 Crimson Red LED
Transform {
  children [
    Transform {
      translation 0 0 0.15
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.92 0.92 0.92 specularColor 0.3 0.3 0.3 shininess 0.2 }
          }
          geometry Box { size 2.0 1.25 0.3 }
        }
      ]
    }
    # Translucent Crimson Red Lens
    Transform {
      translation 0 0 0.58
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.92 0.1 0.1
              emissiveColor 0.4 0.05 0.05
              specularColor 0.9 0.3 0.3
              transparency 0.35
              shininess 0.9
            }
          }
          geometry Box { size 1.3 0.9 0.55 }
        }
      ]
    }
    Transform {
      translation -0.85 0 0.15
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.3 1.25 0.3 }
        }
      ]
    }
    Transform {
      translation 0.85 0 0.15
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.3 1.25 0.3 }
        }
      ]
    }
  ]
}
""")

# 15. sw_tactile_6x6.wrl (Tactile Pushbutton SW1)
write_vrml("sw_tactile_6x6.wrl", """#VRML V2.0 utf8
# 6.0x6.0mm Tactile Pushbutton Switch
Transform {
  children [
    # Phenolic Base Housing
    Transform {
      translation 0 0 1.25
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.15 0.12 0.1 specularColor 0.2 0.2 0.2 shininess 0.2 }
          }
          geometry Box { size 6.0 6.0 2.5 }
        }
      ]
    }
    # Stainless Steel Metal Top Plate
    Transform {
      translation 0 0 2.65
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.85 0.88
              specularColor 0.95 0.95 0.98
              shininess 0.9
            }
          }
          geometry Box { size 6.0 6.0 0.3 }
        }
      ]
    }
    # Cylindrical Actuator Button (Black)
    Transform {
      translation 0 0 3.4
      children [
        Shape {
          appearance Appearance {
            material Material { diffuseColor 0.08 0.08 0.08 specularColor 0.3 0.3 0.3 shininess 0.3 }
          }
          geometry Cylinder { radius 1.5 height 1.2 }
        }
      ]
    }
    # Solder Terminals
    Transform {
      translation -3.3 0 0.5
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.8 5.0 0.4 }
        }
      ]
    }
    Transform {
      translation 3.3 0 0.5
      children [
        Shape {
          appearance Appearance { material Material { diffuseColor 0.85 0.85 0.88 shininess 0.9 } }
          geometry Box { size 0.8 5.0 0.4 }
        }
      ]
    }
  ]
}
""")

# 16. m3_mounting_hole.wrl (M3 Hole Plating Ring)
write_vrml("m3_mounting_hole.wrl", """#VRML V2.0 utf8
# M3 Annular Plating Ring
Transform {
  children [
    Transform {
      translation 0 0 0.03
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.75 0.25
              specularColor 0.9 0.85 0.4
              shininess 0.8
            }
          }
          geometry Cylinder { radius 3.0 height 0.06 }
        }
      ]
    }
  ]
}
""")

print("All 16 VRML models successfully generated.")

