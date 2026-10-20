[app]

# (str) Title of your application
title = Lumina OS

# (str) Package name
package.name = luminaos

# (str) Package domain (needed for android/ios packaging)
package.domain = org.lumina

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (process only files with these extensions)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
source.include_pattern = lumina_data.json

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,urllib3,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions required
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.min_api = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Path to a custom buildozer directory
p4a.branch = master
