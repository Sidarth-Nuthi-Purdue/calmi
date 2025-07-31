#!/usr/bin/env python3
"""
Check what audio processing tools are available on the system.
"""

import subprocess
import sys

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ ffmpeg available: {version_line}")
            return True
        else:
            print("❌ ffmpeg not working")
            return False
    except FileNotFoundError:
        print("❌ ffmpeg not found")
        return False

def check_pydub():
    """Check if pydub is available."""
    try:
        import pydub
        try:
            version = pydub.__version__
        except AttributeError:
            version = "unknown"
        print(f"✅ pydub available: version {version}")
        return True
    except ImportError:
        print("❌ pydub not installed")
        return False

def install_pydub():
    """Install pydub if not available."""
    try:
        print("📦 Installing pydub...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])
        print("✅ pydub installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install pydub: {str(e)}")
        return False

def main():
    """Check audio tools and provide recommendations."""
    print("🔍 Checking Audio Processing Tools")
    print("=" * 40)
    
    ffmpeg_available = check_ffmpeg()
    pydub_available = check_pydub()
    
    print("\n📋 Summary:")
    if ffmpeg_available:
        print("   ✅ ffmpeg - Best option for audio concatenation")
    else:
        print("   ❌ ffmpeg - Not available")
    
    if pydub_available:
        print("   ✅ pydub - Good fallback option")
    else:
        print("   ❌ pydub - Not installed")
    
    print("\n💡 Recommendations:")
    
    if ffmpeg_available:
        print("   🎯 ffmpeg will be used for audio concatenation (most reliable)")
    elif pydub_available:
        print("   🎯 pydub will be used for audio concatenation")
    else:
        print("   ⚠️  No audio tools available!")
        print("   📦 Installing pydub...")
        if install_pydub():
            print("   ✅ pydub installed - audio concatenation should work now")
        else:
            print("   ❌ Failed to install pydub - audio concatenation may fail")
    
    print("\n🚀 Ready to test audio concatenation!")

if __name__ == "__main__":
    main() 