import hashlib
import re
import shutil
import zipfile
from pathlib import Path
import os, subprocess, sys, tempfile, time
import requests


class BuildError(Exception):
    pass


# ---- Android WebView shell (written to disk at build time) ----
TEMPLATE = {
    "settings.gradle": """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositories { google(); mavenCentral() }
}
rootProject.name = 'ApkShell'
include ':app'
""",
    "build.gradle": "plugins { id 'com.android.application' version '8.3.2' apply false }\n",
    "gradle.properties": "org.gradle.jvmargs=-Xmx1024m -Dfile.encoding=UTF-8\norg.gradle.daemon=false\n",
    "app/build.gradle": """plugins { id 'com.android.application' }
android {
    namespace 'com.apkbot.shell'
    compileSdk 34
    defaultConfig {
        applicationId "__APPID__"
        minSdk 24
        targetSdk 34
        versionCode 1
