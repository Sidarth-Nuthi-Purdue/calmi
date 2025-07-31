#!/usr/bin/env python3
"""
AI Podcast Generator for Sid :)

This script takes a conversation transcript and generates an AI podcast episode
with therapeutic insights, philosophical reflections, and warm conversational tone.
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import sys

class AIPodcastGenerator:
    def __init__(self, elevenlabs_api_key: str, playht_api_key: str = None, playht_user_id: str = None):
        """
        Initialize the AI Podcast Generator with API keys.
        
        Args:
            elevenlabs_api_key: ElevenLabs API key for text-to-speech
            playht_api_key: Play.ht API key (optional, for future use)
            playht_user_id: Play.ht user ID (optional, for future use)
        """
        self.elevenlabs_api_key = elevenlabs_api_key
        self.playht_api_key = playht_api_key
        self.playht_user_id = playht_user_id
        
        # ElevenLabs API endpoints
        self.elevenlabs_base_url = "https://api.elevenlabs.io/v1"
        
        # Voice IDs for podcast hosts (you can change these)
        self.host_1_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - warm, conversational
        self.host_2_voice_id = "AZnzlk1XvdvUeBnXmlld"  # Domi - thoughtful, supportive
        
        # Podcast configuration
        self.podcast_config = {
            "intro_duration": 30,  # seconds
            "main_duration": 480,  # 8 minutes
            "outro_duration": 30,  # seconds
            "total_target_duration": 540  # 9 minutes total
        }
    
    def analyze_conversation(self, transcript: str) -> Dict:
        """
        Analyze the conversation transcript using AI to extract deep insights.
        
        Args:
            transcript: The conversation transcript text
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Use AI analysis for deeper insights
            analysis_prompt = f"""
            Analyze this personal conversation transcript and provide therapeutic insights.
            
            Transcript:
            {transcript}
            
            Please provide a JSON response with these fields:
            - "core_themes": List of 2-3 main psychological/emotional themes
            - "emotional_patterns": Key emotional patterns you notice
            - "therapeutic_insights": 3-4 specific therapeutic observations
            - "philosophical_angles": 2-3 deeper life questions or philosophical themes
            - "reframing_opportunities": Specific ways to reframe challenges positively
            - "growth_indicators": Signs of resilience, self-awareness, or growth
            - "support_suggestions": Practical support or coping strategies
            
            Focus on being compassionate, insightful, and therapeutically informed.
            """
            
            # For now, use a sophisticated keyword-based approach with deeper analysis
            # In a full implementation, you'd call an AI API here
            analysis = self._deep_keyword_analysis(transcript)
            
        except Exception as e:
            print(f"⚠️ AI analysis failed, using fallback: {str(e)}")
            analysis = self._fallback_analysis(transcript)
            
        return analysis
    
    def _deep_keyword_analysis(self, transcript: str) -> Dict:
        """Enhanced keyword-based analysis with therapeutic depth."""
        transcript_lower = transcript.lower()
        
        analysis = {
            "core_themes": [],
            "emotional_patterns": [],
            "therapeutic_insights": [],
            "philosophical_angles": [],
            "reframing_opportunities": [],
            "growth_indicators": [],
            "support_suggestions": []
        }
        
        # Core themes detection
        if any(word in transcript_lower for word in ["stuck", "paralyzed", "fear", "doubt", "afraid"]):
            analysis["core_themes"].append("fear and avoidance patterns")
            analysis["therapeutic_insights"].append("Fear often masks deeper concerns about self-worth and capability")
            analysis["reframing_opportunities"].append("Fear as information rather than instruction")
            
        if any(word in transcript_lower for word in ["expectations", "pressure", "perfect", "should"]):
            analysis["core_themes"].append("perfectionism and expectations")
            analysis["therapeutic_insights"].append("Perfectionism can be a form of self-protection against judgment")
        
        if any(word in transcript_lower for word in ["trust", "believe", "confidence", "capable"]):
            analysis["core_themes"].append("self-trust and inner confidence")
            analysis["growth_indicators"].append("Awareness of trust issues is the first step toward healing")
            
        # Emotional patterns
        if "voice in my head" in transcript_lower or "telling me" in transcript_lower:
            analysis["emotional_patterns"].append("inner critic and negative self-talk")
            analysis["support_suggestions"].append("Practice mindful awareness of inner dialogue")
            
        # Philosophical angles
        if any(word in transcript_lower for word in ["meaning", "purpose", "why", "worth"]):
            analysis["philosophical_angles"].append("search for meaning and life purpose")
            
        if any(word in transcript_lower for word in ["journey", "process", "growing", "learning"]):
            analysis["philosophical_angles"].append("life as continuous growth and evolution")
            
        # Growth indicators
        if any(word in transcript_lower for word in ["aware", "realize", "notice", "understand"]):
            analysis["growth_indicators"].append("Strong self-awareness and insight")
            
        if any(word in transcript_lower for word in ["trying", "working on", "practice"]):
            analysis["growth_indicators"].append("Active engagement in personal development")
            
        # Default insights if none detected
        if not analysis["therapeutic_insights"]:
            analysis["therapeutic_insights"] = [
                "The willingness to examine one's patterns shows courage and self-compassion",
                "Growth often happens in the space between comfort and challenge"
            ]
            
        if not analysis["philosophical_angles"]:
            analysis["philosophical_angles"] = [
                "the balance between acceptance and change",
                "finding meaning in uncertainty and growth"
            ]
            
        return analysis
    
    def _fallback_analysis(self, transcript: str) -> Dict:
        """Simple fallback analysis."""
        return {
            "core_themes": ["personal growth", "self-reflection"],
            "emotional_patterns": ["mixed emotions about change"],
            "therapeutic_insights": ["Self-awareness is a powerful tool for growth"],
            "philosophical_angles": ["the journey of becoming"],
            "reframing_opportunities": ["Challenges as opportunities for development"],
            "growth_indicators": ["Willingness to examine patterns"],
            "support_suggestions": ["Practice self-compassion"]
        }
    
    def generate_podcast_script(self, transcript: str, analysis: Dict) -> str:
        """
        Generate a dynamic, conversational podcast script with overlapping dialogue.
        
        Args:
            transcript: The conversation transcript
            analysis: Analysis results from analyze_conversation
            
        Returns:
            Generated podcast script with natural conversation flow
        """
        # Extract analysis components
        themes = analysis.get("core_themes", ["personal growth"])
        insights = analysis.get("therapeutic_insights", [])
        philosophical = analysis.get("philosophical_angles", [])
        reframes = analysis.get("reframing_opportunities", [])
        growth = analysis.get("growth_indicators", [])
        
        # Create a more dynamic, conversational script
        script = open("sample_script2.txt", 'r').read()

        return script.strip()
        
    def text_to_speech(self, text: str, voice_id: str, filename: str) -> bool:
        """
        Convert text to speech using ElevenLabs API with enhanced inflections.
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.elevenlabs_base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            # Enhanced voice settings for more natural inflections
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.3,  # Lower stability for more variation
                    "similarity_boost": 0.7,  # Higher similarity for consistent voice
                    "style": 0.8,  # Add style for more expressive speech
                    "use_speaker_boost": True  # Enhance speaker clarity
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"✅ Generated audio: {filename}")
                return True
            else:
                print(f"❌ Error generating audio: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error in text_to_speech: {str(e)}")
            return False
    
    def generate_podcast(self, transcript: str, output_filename: str = "ai_podcast.mp3") -> bool:
        """
        Generate a complete AI podcast episode from a transcript.
        
        Args:
            transcript: The conversation transcript
            output_filename: Name of the output MP3 file
            
        Returns:
            True if successful, False otherwise
        """
        print("🎙️ Starting AI Podcast Generation...")
        
        # Step 1: Analyze the conversation
        print("📊 Analyzing conversation...")
        analysis = self.analyze_conversation(transcript)
        themes = analysis.get('core_themes', analysis.get('themes', ['personal growth']))
        print(f"   Detected themes: {', '.join(themes)}")
        
        # Step 2: Generate the podcast script
        print("✍️ Generating podcast script...")
        script = self.generate_podcast_script(transcript, analysis)
        
        # Save the script for reference
        script_filename = output_filename.replace('.mp3', '_script.txt')
        with open(script_filename, 'w') as f:
            f.write(script)
        print(f"📝 Script saved to: {script_filename}")
        
        # Step 3: Split script into segments for different voices
        segments = self.split_script_for_voices(script)
        print(f"   Created {len(segments)} voice segments")
        
        # Step 4: Generate audio for each segment
        print("🎵 Generating audio segments...")
        audio_files = []
        
        for i, segment in enumerate(segments):
            if len(segment) == 3:
                segment_text, voice_id, timing_info = segment
            else:
                segment_text, voice_id = segment
                timing_info = "normal"
                
            segment_filename = f"segments/segment_{i:02d}.mp3"
            print(f"   Generating segment {i+1}/{len(segments)}: {len(segment_text)} chars ({timing_info})")
            
            if self.text_to_speech(segment_text, voice_id, segment_filename):
                audio_files.append((segment_filename, timing_info))
            else:
                print(f"❌ Failed to generate segment {i}")
                return False
        
        print(f"   Successfully generated {len(audio_files)} audio segments")
        
        # Step 5: Combine audio files
        print("🔗 Combining audio segments...")
        if self.combine_audio_files_smart(audio_files, output_filename):
            print(f"🎉 Podcast generated successfully: {output_filename}")
            
            # Clean up segment files
            for segment_info in audio_files:
                try:
                    if isinstance(segment_info, tuple):
                        segment_file, _ = segment_info
                    else:
                        segment_file = segment_info
                    os.remove(segment_file)
                except:
                    pass
            
            return True
        else:
            print("❌ Failed to combine audio files")
            return False
    
    def generate_podcast_from_script(self, script_file: str, output_filename: str = "ai_podcast.mp3") -> bool:
        """
        Generate a podcast from a pre-written script file (bypassing transcript analysis).
        Args:
            script_file: Path to the script text file
            output_filename: Name of the output MP3 file
        Returns:
            True if successful, False otherwise
        """
        print(f"🎙️ Generating podcast from script: {script_file}")
        try:
            with open(script_file, 'r') as f:
                script = f.read()
        except Exception as e:
            print(f"❌ Error reading script file: {str(e)}")
            return False
        
        # Save a copy of the script for reference
        script_filename = output_filename.replace('.mp3', '_script.txt')
        with open(script_filename, 'w') as f:
            f.write(script)
        print(f"📝 Script saved to: {script_filename}")
        
        # Split script into segments for different voices
        segments = self.split_script_for_voices(script)
        print(f"   Created {len(segments)} voice segments")
        
        # Generate audio for each segment
        print("🎵 Generating audio segments...")
        audio_files = []
        for i, segment in enumerate(segments):
            if len(segment) == 3:
                segment_text, voice_id, timing_info = segment
            else:
                segment_text, voice_id = segment
                timing_info = "normal"
            segment_filename = f"segments/segment_{i:02d}.mp3"
            print(f"   Generating segment {i+1}/{len(segments)}: {len(segment_text)} chars ({timing_info})")
            if self.text_to_speech(segment_text, voice_id, segment_filename):
                audio_files.append((segment_filename, timing_info))
            else:
                print(f"❌ Failed to generate segment {i}")
                return False
        print(f"   Successfully generated {len(audio_files)} audio segments")
        
        # Combine audio files
        print("🔗 Combining audio segments...")
        if self.combine_audio_files_smart(audio_files, output_filename):
            print(f"🎉 Podcast generated successfully: {output_filename}")
            # Clean up segment files
            for segment_info in audio_files:
                try:
                    if isinstance(segment_info, tuple):
                        segment_file, _ = segment_info
                    else:
                        segment_file = segment_info
                    # os.remove(segment_file)
                except:
                    pass
            return True
        else:
            print("❌ Failed to combine audio files")
            return False
    
    def split_script_for_voices(self, script: str) -> List[tuple]:
        """
        Split the script into segments for different voices.
        
        Args:
            script: The complete podcast script
            
        Returns:
            List of (text, voice_id) tuples
        """
        segments = []
        lines = script.split('\n')
        current_segment = ""
        current_voice = self.host_1_voice_id
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle overlap speech markers
            if "[OVERLAP - Host" in line:
                if current_segment:
                    segments.append((current_segment, current_voice, "normal"))
                
                if "Host 1" in line:
                    current_voice = self.host_1_voice_id
                else:
                    current_voice = self.host_2_voice_id
                    
                # Extract the text after the marker
                text = line.split("]", 1)[1].strip() if "]" in line else ""
                if text:
                    segments.append((text, current_voice, "overlap"))
                current_segment = ""
                
            # Skip any remaining simultaneous markers (legacy)
            elif "[SIMULTANEOUS" in line or "[Both -" in line:
                # Skip these lines entirely
                pass
                
            # Check for regular voice indicators
            elif "[Host 1]" in line or "[INTRO - Host 1]" in line or "[MAIN DISCUSSION - Host 1]" in line or "[OUTRO - Host 1]" in line:
                if current_segment:
                    segments.append((current_segment, current_voice, "normal"))
                current_segment = line.replace("[Host 1]", "").replace("[INTRO - Host 1]", "").replace("[MAIN DISCUSSION - Host 1]", "").replace("[OUTRO - Host 1]", "").strip()
                current_voice = self.host_1_voice_id
            elif "[Host 2]" in line or "[INTRO - Host 2]" in line or "[MAIN DISCUSSION - Host 2]" in line or "[OUTRO - Host 2]" in line:
                if current_segment:
                    segments.append((current_segment, current_voice, "normal"))
                current_segment = line.replace("[Host 2]", "").replace("[INTRO - Host 2]", "").replace("[MAIN DISCUSSION - Host 2]", "").replace("[OUTRO - Host 2]", "").strip()
                current_voice = self.host_2_voice_id
            # Skip stage directions like [laughing], [also laughing], etc.
            elif line.startswith("[") and line.endswith("]"):
                pass  # Skip stage directions
            else:
                current_segment += " " + line
        
        # Add the last segment
        if current_segment:
            segments.append((current_segment, current_voice, "normal"))
        
        # Ensure all segments have timing info
        final_segments = []
        for segment in segments:
            if len(segment) == 2:
                text, voice = segment
                timing = "normal"
            else:
                text, voice, timing = segment
            
            if text.strip():
                final_segments.append((text.strip(), voice, timing))
        
        return final_segments
    
    def combine_audio_files(self, audio_files: List[str], output_filename: str, overlap_probability: float = 0.3) -> bool:
        """
        Combine multiple audio files into one, sometimes overlapping segments for a conversational feel.
        Uses pydub for audio processing. Falls back to ffmpeg or simple concat if needed.
        
        Args:
            audio_files: List of audio file paths
            output_filename: Output filename
            overlap_probability: Probability (0-1) that a segment will overlap with the previous one
        Returns:
            True if successful, False otherwise
        """
        import random
        try:
            if not audio_files:
                print("❌ No audio files to combine")
                return False
            try:
                from pydub import AudioSegment
            except ImportError:
                print("⚠️  pydub not available, installing...")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])
                from pydub import AudioSegment

            print(f"🔗 Combining {len(audio_files)} audio segments with overlap_probability={overlap_probability}")
            combined = AudioSegment.from_mp3(audio_files[0])
            silence = AudioSegment.silent(duration=500)  # 0.5 seconds

            for i, audio_file in enumerate(audio_files[1:], 1):
                segment = AudioSegment.from_mp3(audio_file)
                # Decide whether to overlap
                do_overlap = (random.random() < overlap_probability)
                if do_overlap and len(combined) > 2000 and len(segment) > 1000:
                    # Overlap by 1.5 seconds (or less if segment is short)
                    overlap_ms = min(1500, len(segment) // 2, len(combined) // 2)
                    print(f"   Overlapping segment {i+1} by {overlap_ms} ms")
                    # Overlay segment onto the end of combined
                    pre = combined[:-overlap_ms]
                    overlay = combined[-overlap_ms:].overlay(segment[:overlap_ms])
                    post = segment[overlap_ms:]
                    combined = pre + overlay + post
                else:
                    print(f"   Appending segment {i+1} (no overlap)")
                    combined = combined + silence + segment

            combined.export(output_filename, format="mp3")
            print(f"✅ Combined audio saved to: {output_filename}")
            return True
        except Exception as e:
            print(f"❌ Error combining audio files with overlap: {str(e)}")
            # Fallback to ffmpeg concat
            try:
                import subprocess
                file_list = "file_list.txt"
                with open(file_list, "w") as f:
                    for audio_file in audio_files:
                        f.write(f"file '{audio_file}'\n")
                cmd = [
                    "ffmpeg", "-f", "concat", "-safe", "0", 
                    "-i", file_list, "-c", "copy", output_filename, "-y"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if os.path.exists(file_list):
                    os.remove(file_list)
                if result.returncode == 0:
                    print(f"✅ Combined audio saved to: {output_filename}")
                    return True
                else:
                    print(f"⚠️  ffmpeg failed: {result.stderr}")
            except Exception as ffmpeg_error:
                print(f"❌ ffmpeg fallback failed: {str(ffmpeg_error)}")
            # Final fallback: just copy the first file
            try:
                if audio_files:
                    import shutil
                    shutil.copy(audio_files[0], output_filename)
                    print(f"⚠️  Fallback: copied first segment only to {output_filename}")
                    return True
            except:
                pass
            return False
    
    def combine_segments_only(self, output_filename: str = "combined_podcast.mp3") -> bool:
        """
        Just combine existing segment files with smart timing.
        """
        import glob
        import os
        
        # Find all segment files
        segment_files = sorted(glob.glob("segments/segment_*.mp3"))
        if not segment_files:
            print("❌ No segment files found in segments/ directory")
            return False
            
        # Create audio_files list with timing info based on filenames
        audio_files = []
        for i, segment_file in enumerate(segment_files):
            # Default to normal timing - you'd need to store timing info separately
            # for a real implementation
            audio_files.append((segment_file, "normal"))
            
        return self.combine_audio_files_smart(audio_files, output_filename)
    
    def _trim_silence(self, audio_segment: 'AudioSegment', silence_thresh: int = -40) -> 'AudioSegment':
        """
        Trim silence from the beginning and end of an audio segment.
        
        Args:
            audio_segment: The audio segment to trim
            silence_thresh: Silence threshold in dB (lower = more sensitive)
        
        Returns:
            Trimmed audio segment
        """
        try:
            from pydub.silence import detect_nonsilent
            
            # Detect non-silent chunks
            nonsilent_chunks = detect_nonsilent(
                audio_segment, 
                min_silence_len=100,  # 100ms minimum silence
                silence_thresh=silence_thresh
            )
            
            if not nonsilent_chunks:
                return audio_segment  # Return original if no non-silent parts found
            
            # Get the first and last non-silent chunk
            start_trim = nonsilent_chunks[0][0]
            end_trim = nonsilent_chunks[-1][1]
            
            # Trim with small padding to avoid cutting off speech
            padding = 50  # 50ms padding
            start_trim = max(0, start_trim - padding)
            end_trim = min(len(audio_segment), end_trim + padding)
            
            return audio_segment[start_trim:end_trim]
            
        except ImportError:
            # If pydub.silence not available, return original
            return audio_segment
        except Exception:
            # If trimming fails for any reason, return original
            return audio_segment
    
    def combine_audio_files_smart(self, audio_files: List[tuple], output_filename: str) -> bool:
        """
        Combine audio files with smart timing based on dialogue markers.
        
        Args:
            audio_files: List of (filename, timing_info) tuples
            output_filename: Output filename
        Returns:
            True if successful, False otherwise
        """
        try:
            if not audio_files:
                print("❌ No audio files to combine")
                return False
                
            try:
                from pydub import AudioSegment
            except ImportError:
                print("⚠️ pydub not available, falling back to simple combination")
                simple_files = [f[0] if isinstance(f, tuple) else f for f in audio_files]
                return self.combine_audio_files(simple_files, output_filename, overlap_probability=0.2)

            print(f"🔗 Combining {len(audio_files)} audio segments with smart timing")
            
            # Load first segment
            if isinstance(audio_files[0], tuple):
                first_file, _ = audio_files[0]
            else:
                first_file = audio_files[0]
            
            # Trim silence from first segment and load
            combined = AudioSegment.from_mp3(first_file)
            combined = self._trim_silence(combined)
            
            # Natural conversation timing
            tiny_pause = AudioSegment.silent(duration=100)     # 0.1 seconds - quick but natural
            short_pause = AudioSegment.silent(duration=150)    # 0.15 seconds - comfortable
            normal_pause = AudioSegment.silent(duration=200)   # 0.2 seconds - natural breath
            
            for i, audio_info in enumerate(audio_files[1:], 1):
                if isinstance(audio_info, tuple):
                    audio_file, timing_info = audio_info
                else:
                    audio_file = audio_info
                    timing_info = "normal"
                
                # Load and trim silence from this segment
                segment = AudioSegment.from_mp3(audio_file)
                segment = self._trim_silence(segment)
                
                if timing_info == "overlap":
                    # MUCH more aggressive overlap - cut into previous segment
                    # Trim end of combined first, then overlap heavily
                    combined = self._trim_silence(combined)
                    overlap_ms = min(2000, len(segment) // 1.5, len(combined) // 2)  # Very aggressive
                    print(f"   🔄 TIGHT overlap segment {i+1} by {overlap_ms} ms")
                    
                    if overlap_ms > 100:  # Only overlap if meaningful
                        pre = combined[:-overlap_ms]
                        overlay = combined[-overlap_ms:].overlay(segment[:overlap_ms])
                        post = segment[overlap_ms:]
                        combined = pre + overlay + post
                    else:
                        # Direct connection - no pause at all
                        combined = combined + segment
                    
                elif timing_info == "simultaneous":
                    # True simultaneous - back up significantly and overlay
                    print(f"   🎭 SIMULTANEOUS overlay for segment {i+1}")
                    combined = self._trim_silence(combined)
                    backup_ms = min(1000, len(combined) // 3, len(segment))
                    if backup_ms > 0:
                        before = combined[:-backup_ms]
                        overlay_section = combined[-backup_ms:].overlay(segment)
                        combined = before + overlay_section
                    else:
                        combined = combined.overlay(segment)
                    
                else:  # normal - natural conversation flow
                    # Trim both segments and use comfortable pause
                    combined = self._trim_silence(combined)
                    combined = combined + short_pause + segment
                    print(f"   ➡️  Added segment {i+1} with natural pause")

            combined.export(output_filename, format="mp3")
            print(f"✅ Combined audio saved to: {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error in smart audio combination: {str(e)}")
            # Fallback to original method
            simple_files = [f[0] if isinstance(f, tuple) else f for f in audio_files]
            return self.combine_audio_files(simple_files, output_filename, overlap_probability=0.2)

def load_sample_conversations() -> Dict[str, str]:
    """
    Load sample conversations for testing.
    
    Returns:
        Dictionary of conversation names and their transcripts
    """
    conversations = {
        "heavy_emotional_disclosure": """
        I've been feeling really overwhelmed lately. Like, everything just feels like too much. 
        I had this conversation with my partner last night and it just... it brought up so much stuff. 
        I realized I've been carrying around this fear of abandonment for years, and I don't know how to let it go. 
        Every time someone gets close to me, I start to panic that they're going to leave. 
        It's exhausting, you know? I want to be able to trust and be vulnerable, but it's so hard. 
        I keep thinking about my childhood and how my parents would fight and threaten to leave each other. 
        I know that's probably where this comes from, but knowing that doesn't make it easier to deal with.
        """,
        
        "goal_setting_accountability": """
        I've been trying to work on my goals for months now, but I keep getting stuck. 
        I want to start my own business, but every time I sit down to work on it, I get paralyzed by fear. 
        What if I fail? What if people think my idea is stupid? What if I invest all this time and money and it goes nowhere? 
        I know I need to just start small and take it one step at a time, but it's so hard to overcome that initial resistance. 
        I've been reading all these books about entrepreneurship and productivity, but I feel like I'm just collecting information instead of actually doing anything. 
        I need to find a way to hold myself accountable and actually make progress.
        """,
        
        "light_reflective_checkin": """
        Today was actually a pretty good day. I went for a walk in the morning and the weather was beautiful. 
        I've been trying to be more mindful about the small moments of joy in my life. 
        Like, I noticed how the sunlight was filtering through the trees, and it just made me feel grateful to be alive. 
        I've been thinking a lot about what brings me happiness and how I can create more of those moments. 
        It's funny how when you start paying attention, you realize there are so many little things to appreciate. 
        I'm still working through some stuff, but I feel like I'm making progress, you know?
        """,
        
        "crisis_management": """
        I'm really struggling right now. I lost my job last week and I don't know how I'm going to pay my rent. 
        I've been applying everywhere but no one is getting back to me. I feel like such a failure. 
        My family keeps asking me what I'm going to do, and I don't have any answers. 
        I'm trying to stay positive, but it's so hard when everything feels like it's falling apart. 
        I don't want to ask for help because I feel like I should be able to handle this on my own. 
        But I'm scared. I don't know what to do next.
        """,
        
        "long_term_patterns": """
        I've been in therapy for about a year now, and we've been talking about these patterns I keep repeating in my relationships. 
        I always seem to end up with people who are emotionally unavailable, and then I try to fix them or change them. 
        My therapist says I'm recreating the dynamic I had with my parents, where I was always trying to manage their emotions. 
        It makes sense intellectually, but it's so hard to break these patterns when they're so deeply ingrained. 
        I want to have healthy relationships, but I don't even know what that looks like. 
        I'm afraid that if I stop trying to fix people, they won't want to be with me anymore.
        """
    }
    
    return conversations

def main():
    """Main function to run the AI Podcast Generator."""
    parser = argparse.ArgumentParser(description="Generate AI podcast episodes from conversation transcripts")
    parser.add_argument("--transcript", "-t", help="Path to transcript file")
    parser.add_argument("--output", "-o", default="ai_podcast.mp3", help="Output filename")
    parser.add_argument("--sample", "-s", help="Use a sample conversation (heavy_emotional_disclosure, goal_setting_accountability, light_reflective_checkin, crisis_management, long_term_patterns)")
    parser.add_argument("--script-file", help="Path to a pre-written script file (instead of transcript/sample)")
    parser.add_argument("--combine-only", action="store_true", help="Just combine existing segments/ files")
    parser.add_argument("--api-key", help="ElevenLabs API key")
    
    args = parser.parse_args()
    
    # Handle combine-only mode
    if args.combine_only:
        print("🔗 Combine-only mode: combining existing segments...")
        # Create generator without API key for combining only
        generator = AIPodcastGenerator("dummy_key")  # Won't be used for combining
        success = generator.combine_segments_only(args.output)
        if success:
            print(f"\n🎉 Audio combination complete!")
            print(f"📁 Output file: {args.output}")
        else:
            print("\n❌ Audio combination failed")
        sys.exit(0 if success else 1)
    
    # Get API key
    api_key = args.api_key or os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ Error: ElevenLabs API key is required.")
        print("   Set it with --api-key or ELEVENLABS_API_KEY environment variable")
        sys.exit(1)
    
    # Initialize the generator
    generator = AIPodcastGenerator(api_key)
    
    # Get transcript or script file
    transcript = ""
    if args.sample:
        conversations = load_sample_conversations()
        if args.sample in conversations:
            transcript = conversations[args.sample]
            print(f"📖 Using sample conversation: {args.sample}")
        else:
            print(f"❌ Unknown sample conversation: {args.sample}")
            print(f"   Available: {', '.join(conversations.keys())}")
            sys.exit(1)
    elif args.transcript:
        try:
            with open(args.transcript, 'r') as f:
                transcript = f.read()
            print(f"📖 Loaded transcript from: {args.transcript}")
        except Exception as e:
            print(f"❌ Error reading transcript file: {str(e)}")
            sys.exit(1)
    elif args.script_file:
        try:
            with open(args.script_file, 'r') as f:
                script = f.read()
            transcript = script # Treat script as transcript for processing
            print(f"📖 Loaded script from: {args.script_file}")
        except Exception as e:
            print(f"❌ Error reading script file: {str(e)}")
            sys.exit(1)
    else:
        print("❌ Error: Please provide either --transcript, --sample, or --script-file")
        sys.exit(1)
    
    if not transcript.strip():
        print("❌ Error: Empty transcript or script")
        sys.exit(1)
    
    # Generate the podcast
    if args.script_file:
        success = generator.generate_podcast_from_script(args.script_file, args.output)
    else:
        success = generator.generate_podcast(transcript, args.output)
    
    if success:
        print(f"\n🎉 Podcast generation complete!")
        print(f"📁 Output file: {args.output}")
        print(f"📝 Script file: {args.output.replace('.mp3', '_script.txt')}")
    else:
        print("\n❌ Podcast generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 