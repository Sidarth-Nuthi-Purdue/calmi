#!/usr/bin/env python3
"""
Test script for the AI Podcast Generator
This script demonstrates the functionality without making API calls.
"""

import os
import sys
from ai_podcast_generator import AIPodcastGenerator, load_sample_conversations

def test_conversation_analysis():
    """Test the conversation analysis functionality."""
    print("🧪 Testing Conversation Analysis...")
    
    # Create a mock generator (no API key needed for analysis)
    generator = AIPodcastGenerator("mock_key")
    
    # Test with a sample conversation
    conversations = load_sample_conversations()
    test_transcript = conversations["heavy_emotional_disclosure"]
    
    # Analyze the conversation
    analysis = generator.analyze_conversation(test_transcript)
    
    print("✅ Analysis Results:")
    print(f"   Themes: {', '.join(analysis['themes'])}")
    print(f"   Therapeutic Angles: {', '.join(analysis['therapeutic_angles'])}")
    print(f"   Key Topics: {len(analysis['key_topics'])} topics identified")
    
    return analysis

def test_script_generation():
    """Test the podcast script generation."""
    print("\n🧪 Testing Script Generation...")
    
    # Create a mock generator
    generator = AIPodcastGenerator("mock_key")
    
    # Use sample conversation
    conversations = load_sample_conversations()
    test_transcript = conversations["goal_setting_accountability"]
    
    # Analyze and generate script
    analysis = generator.analyze_conversation(test_transcript)
    script = generator.generate_podcast_script(test_transcript, analysis)
    
    print("✅ Script Generated Successfully!")
    print(f"   Script length: {len(script)} characters")
    print(f"   Contains Host 1: {'[Host 1]' in script}")
    print(f"   Contains Host 2: {'[Host 2]' in script}")
    print(f"   Contains therapeutic content: {'therapeutic' in script.lower()}")
    
    # Save sample script
    with open("sample_script.txt", "w") as f:
        f.write(script)
    print("   📝 Sample script saved to: sample_script.txt")
    
    return script

def test_voice_segmentation():
    """Test the script segmentation for different voices."""
    print("\n🧪 Testing Voice Segmentation...")
    
    # Create a mock generator
    generator = AIPodcastGenerator("mock_key")
    
    # Generate a script
    conversations = load_sample_conversations()
    test_transcript = conversations["crisis_management"]
    analysis = generator.analyze_conversation(test_transcript)
    script = generator.generate_podcast_script(test_transcript, analysis)
    
    # Split into voice segments
    segments = generator.split_script_for_voices(script)
    
    print("✅ Voice Segmentation Results:")
    print(f"   Total segments: {len(segments)}")
    
    host1_segments = [s for s in segments if s[1] == generator.host_1_voice_id]
    host2_segments = [s for s in segments if s[1] == generator.host_2_voice_id]
    
    print(f"   Host 1 segments: {len(host1_segments)}")
    print(f"   Host 2 segments: {len(host2_segments)}")
    
    # Show first few segments
    print("\n   Sample segments:")
    for i, (text, voice_id) in enumerate(segments[:3]):
        voice_name = "Host 1" if voice_id == generator.host_1_voice_id else "Host 2"
        print(f"     {i+1}. {voice_name}: {text[:50]}...")
    
    return segments

def test_sample_conversations():
    """Test all sample conversations."""
    print("\n🧪 Testing Sample Conversations...")
    
    conversations = load_sample_conversations()
    generator = AIPodcastGenerator("mock_key")
    
    print(f"✅ Loaded {len(conversations)} sample conversations:")
    
    for name, transcript in conversations.items():
        analysis = generator.analyze_conversation(transcript)
        print(f"   {name}: {', '.join(analysis['themes'])}")
    
    return conversations

def main():
    """Run all tests."""
    print("🎙️ AI Podcast Generator - Test Suite")
    print("=" * 50)
    
    try:
        # Test conversation analysis
        analysis = test_conversation_analysis()
        
        # Test script generation
        script = test_script_generation()
        
        # Test voice segmentation
        segments = test_voice_segmentation()
        
        # Test sample conversations
        conversations = test_sample_conversations()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Summary:")
        print("   ✅ Conversation analysis working")
        print("   ✅ Script generation working")
        print("   ✅ Voice segmentation working")
        print("   ✅ Sample conversations loaded")
        print("\n🚀 Ready to generate podcasts with real API calls!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 