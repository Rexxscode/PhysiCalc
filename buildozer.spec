[app]

# Nama aplikasi
title = Rumus Fisika SMP

# Nama paket
package.name = rumusfisikasmp

# Domain paket
package.domain = com.fisikasmp

# Source code
source.dir = .

# File utama
source.include_exts = py,png,jpg,kv,atlas,ttf

# Versi aplikasi
version = 1.0

# Requirements
requirements = python3,kivy==2.1.0,hostpython3

# Versi Android SDK
android.api = 31
android.minapi = 21
android.sdk = 23
android.ndk = 23b
android.ndk_api = 21

# Permission Android
android.permissions = INTERNET

# Ikon aplikasi
icon.filename = %(source.dir)s/assets/icon.png

# Orientasi layar
orientation = portrait

# Fullscreen
fullscreen = 0

# Versi Python
python.version = 3.9

# Buildozer
log_level = 2

# Atur ukuran window untuk Android
osx.python_version = 3
osx.kivy_version = 2.1.0

# Atur build
[buildozer]
log_level = 2
warn_on_root = 1