#!/usr/bin/env python3
"""
Simple script to generate a podcast from the Dennis transcript.
Run this to create the actual podcast without any prompts.
"""

import os
import sys
from ai_podcast_generator import AIPodcastGenerator

def main():
    """Generate podcast from Dennis transcript."""
    
    # API Key
    API_KEY = "sk_9826ff690460e4e48e6a9d0e238e172d209e1c03489353f7"
    
    print("🎙️ Generating Dennis Podcast...")
    
    # Check if transcript exists
    if not os.path.exists("dennis_transcript.txt"):
        print("❌ Error: dennis_transcript.txt not found")
        sys.exit(1)
    
    try:
        # Initialize generator
        generator = AIPodcastGenerator(API_KEY)
        
        # Read transcript
        with open("dennis_transcript.txt", 'r') as f:
            transcript = f.read()
        
        # Generate podcast
        output_file = "dennis_podcast.mp3"
        success = generator.generate_podcast(transcript, output_file)
        
        if success:
            print(f"\n🎉 Podcast generated successfully!")
            print(f"📁 File: {output_file}")
            print(f"📝 Script: {output_file.replace('.mp3', '_script.txt')}")
        else:
            print("\n❌ Podcast generation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 