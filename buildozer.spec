[app]
title = Lumina OS
package.name = luminaos
package.domain = org.lumina
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_pattern = lumina_data.json
version = 1.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,urllib3,certifi,idna,charset-normalizer
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.min_api = 21
android.ndk = 25b
android.accept_sdk_license = True
p4a.branch = master
