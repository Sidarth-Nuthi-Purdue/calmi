#!/usr/bin/env python3
"""
Production Test Script for AI Podcast Generator
This script runs the actual podcast generation with real API calls.
"""

import os
import sys
from ai_podcast_generator import AIPodcastGenerator

def run_production_test():
    """Run a production test with the Dennis transcript."""
    
    # API Key (you can also set this as environment variable)
    API_KEY = "sk_9826ff690460e4e48e6a9d0e238e172d209e1c03489353f7"
    
    print("🎙️ AI Podcast Generator - Production Test")
    print("=" * 50)
    
    # Check if transcript file exists
    transcript_file = "dennis_transcript.txt"
    if not os.path.exists(transcript_file):
        print(f"❌ Error: Transcript file '{transcript_file}' not found")
        print("   Please make sure the file exists in the current directory")
        return False
    
    try:
        # Initialize the generator with real API key
        print("🔑 Initializing podcast generator...")
        generator = AIPodcastGenerator(API_KEY)
        
        # Read the transcript
        print(f"📖 Reading transcript from: {transcript_file}")
        with open(transcript_file, 'r') as f:
            transcript = f.read()
        
        if not transcript.strip():
            print("❌ Error: Empty transcript file")
            return False
        
        print(f"✅ Transcript loaded ({len(transcript)} characters)")
        
        # Generate the podcast
        output_filename = "dennis_podcast.mp3"
        print(f"\n🎙️ Generating podcast: {output_filename}")
        print("   This may take a few minutes...")
        
        success = generator.generate_podcast(transcript, output_filename)
        
        if success:
            print(f"\n🎉 Production test completed successfully!")
            print(f"📁 Podcast file: {output_filename}")
            print(f"📝 Script file: {output_filename.replace('.mp3', '_script.txt')}")
            
            # Check file sizes
            if os.path.exists(output_filename):
                size = os.path.getsize(output_filename)
                print(f"📊 Audio file size: {size:,} bytes ({size/1024/1024:.1f} MB)")
            
            return True
        else:
            print("\n❌ Podcast generation failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Production test failed: {str(e)}")
        return False

def run_quick_analysis_test():
    """Run a quick analysis test without API calls."""
    
    print("\n🔍 Quick Analysis Test (No API Calls)")
    print("-" * 30)
    
    try:
        # Create generator with mock key for analysis only
        generator = AIPodcastGenerator("mock_key")
        
        # Read transcript
        with open("dennis_transcript.txt", 'r') as f:
            transcript = f.read()
        
        # Analyze conversation
        analysis = generator.analyze_conversation(transcript)
        
        print("✅ Analysis Results:")
        print(f"   Themes: {', '.join(analysis['themes'])}")
        print(f"   Therapeutic Angles: {', '.join(analysis['therapeutic_angles'])}")
        print(f"   Key Topics: {len(analysis['key_topics'])} identified")
        
        # Generate script preview
        script = generator.generate_podcast_script(transcript, analysis)
        print(f"   Script Length: {len(script)} characters")
        
        # Save preview script
        with open("dennis_script_preview.txt", "w") as f:
            f.write(script)
        print("   📝 Preview script saved to: dennis_script_preview.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis test failed: {str(e)}")
        return False

def main():
    """Main function to run production tests."""
    
    print("🚀 Starting Production Tests...")
    
    # First run quick analysis test
    analysis_success = run_quick_analysis_test()
    
    if not analysis_success:
        print("\n❌ Analysis test failed, stopping here")
        sys.exit(1)
    
    # Ask user if they want to proceed with full generation
    print("\n" + "="*50)
    print("⚠️  Full podcast generation will use your ElevenLabs API credits")
    print("   This will generate actual audio files using the API")
    print("   Estimated cost: ~$0.01-0.05 per podcast")
    
    response = input("\nDo you want to proceed with full podcast generation? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🎙️ Proceeding with full podcast generation...")
        production_success = run_production_test()
        
        if production_success:
            print("\n🎉 All tests completed successfully!")
            print("\n📋 What was generated:")
            print("   ✅ Conversation analysis")
            print("   ✅ Podcast script")
            print("   ✅ Audio podcast file")
            print("\n🎧 You can now listen to the generated podcast!")
        else:
            print("\n❌ Production test failed")
            sys.exit(1)
    else:
        print("\n✅ Analysis test completed successfully!")
        print("   Full podcast generation skipped")
        print("   Check 'dennis_script_preview.txt' for the generated script")

if __name__ == "__main__":
    main() 