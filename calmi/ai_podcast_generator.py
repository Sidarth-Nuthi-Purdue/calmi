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

# Add OpenAI client
try:
    from openai import OpenAI
except ImportError:
    print("⚠️ OpenAI library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

class AIPodcastGenerator:
    def __init__(self, elevenlabs_api_key: str, playht_api_key: str = None, playht_user_id: str = None, openai_api_key: str = None):
        """
        Initialize the AI Podcast Generator with API keys.
        
        Args:
            elevenlabs_api_key: ElevenLabs API key for text-to-speech
            playht_api_key: Play.ht API key (optional, for future use)
            playht_user_id: Play.ht user ID (optional, for future use)
            openai_api_key: OpenAI API key for script generation
        """
        self.elevenlabs_api_key = elevenlabs_api_key
        self.playht_api_key = playht_api_key
        self.playht_user_id = playht_user_id
        
        # Initialize OpenAI client
        self.openai_client = None
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
            print("✅ OpenAI client initialized")
        
        # ElevenLabs API endpoints
        self.elevenlabs_base_url = "https://api.elevenlabs.io/v1"
        
        # Voice IDs for podcast hosts (you can change these)
        # ElevenLabs voices
        self.elevenlabs_host_1 = "21m00Tcm4TlvDq8ikWAM"  # Rachel - warm, conversational
        self.elevenlabs_host_2 = "MF3mGyEYCl7XYWbV9V6O"  # Elli - natural, friendly female voice
        
        # Play.ht voices (better for podcasts - using simpler voice names)
        self.playht_host_1 = "jennifer"  # Natural female voice
        self.playht_host_2 = "michael"   # Natural male voice
        
        # Default to ElevenLabs (more reliable)
        self.host_1_voice_id = self.elevenlabs_host_1
        self.host_2_voice_id = self.elevenlabs_host_2
        
        # TTS provider preference - default to ElevenLabs
        self.tts_provider = "elevenlabs"
        
        # Only use Play.ht if explicitly requested and credentials available
        if playht_api_key and playht_user_id:
            self.playht_host_1_backup = self.playht_host_1
            self.playht_host_2_backup = self.playht_host_2
        
        # Podcast configuration
        self.podcast_config = {
            "intro_duration": 30,  # seconds
            "main_duration": 480,  # 8 minutes
            "outro_duration": 30,  # seconds
            "total_target_duration": 540  # 9 minutes total
        }
    
    def analyze_conversation(self, transcript: str) -> Dict:
        """
        Analyze the conversation transcript using OpenAI to extract deep insights.
        
        Args:
            transcript: The conversation transcript text
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = self._openai_analysis(transcript)    
        return analysis
    
    def _openai_analysis(self, transcript: str) -> Dict:
        """
        Use OpenAI to analyze the conversation transcript.
        
        Args:
            transcript: The conversation transcript text
            
        Returns:
            Dictionary containing analysis results
        """
        analysis_prompt = f"""
Analyze this personal conversation transcript and provide therapeutic insights. Be deeply empathetic and therapeutically informed.

Transcript:
{transcript}

Please provide a JSON response with these exact fields:
- "core_themes": List of 2-3 main psychological/emotional themes
- "emotional_patterns": Key emotional patterns you notice
- "therapeutic_insights": 3-4 specific therapeutic observations
- "philosophical_angles": 2-3 deeper life questions or philosophical themes
- "reframing_opportunities": Specific ways to reframe challenges positively
- "growth_indicators": Signs of resilience, self-awareness, or growth
- "support_suggestions": Practical support or coping strategies

Focus on being compassionate, insightful, and therapeutically informed. Return ONLY valid JSON.
"""
            
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate therapist and philosopher analyzing conversations to provide deep insights. Always respond with valid JSON only."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        analysis = json.loads(analysis_text)
        
        # Validate required fields
        required_fields = ["core_themes", "emotional_patterns", "therapeutic_insights", 
                            "philosophical_angles", "reframing_opportunities", "growth_indicators", "support_suggestions"]
        
        for field in required_fields:
            if field not in analysis:
                analysis[field] = []
        
        print("✅ OpenAI conversation analysis complete")
        return analysis

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
        
        # Generate AI-powered empathetic script
        script = self._generate_ai_script(transcript, analysis)
        
        return script.strip()
    
    def _generate_ai_script(self, transcript: str, analysis: Dict) -> str:
        """
        Generate an AI-powered podcast script that's deeply empathetic and therapeutic.
        
        Args:
            transcript: The original conversation transcript
            analysis: Analysis results containing themes, insights, etc.
            
        Returns:
            Generated podcast script
        """
        return self._create_ai_prompted_script(transcript, analysis)
            
    def _create_ai_prompted_script(self, transcript: str, analysis: Dict) -> str:
        """
        Create a script using OpenAI for natural, therapeutic podcast generation.
        """
        return self._openai_script_generation(transcript, analysis)
    
    def _load_example_scripts(self) -> str:
        """Load example scripts from the scripts/ directory to provide context."""
        example_scripts = []
        script_files = ["fear_of_success_script.txt", "relationship_patterns_script.txt", "crisis_support_script.txt"]
        
        for script_file in script_files:
            try:
                with open(f"scripts/{script_file}", 'r') as f:
                    content = f.read()
                    example_scripts.append(f"=== {script_file.replace('_', ' ').replace('.txt', '').title()} ===\n{content}")
            except FileNotFoundError:
                continue
        
        return "\n\n".join(example_scripts)

    def _openai_script_generation(self, transcript: str, analysis: Dict) -> str:
        """
        Generate podcast script using OpenAI API with example scripts as context.
        
        Args:
            transcript: The original conversation transcript
            analysis: Analysis results from analyze_conversation
            
        Returns:
            Generated podcast script
        """
        # Load example scripts for context
        example_scripts = self._load_example_scripts()
        
        # Prepare context from analysis
        themes = analysis.get('core_themes', [])
        insights = analysis.get('therapeutic_insights', [])
        philosophical = analysis.get('philosophical_angles', [])
        reframes = analysis.get('reframing_opportunities', [])
        growth = analysis.get('growth_indicators', [])
        
        script_prompt = f"""
Create a warm, empathetic podcast script for "Deep Reflections" hosted by Sarah and Rachel, following the style and format of the examples below.

EXAMPLE SCRIPTS (for style reference):
{example_scripts}

ORIGINAL CONVERSATION TO ANALYZE:
{transcript}

ANALYSIS INSIGHTS:
- Core themes: {', '.join(themes) if themes else 'personal growth'}
- Therapeutic insights: {'; '.join(insights[:2]) if insights else 'self-awareness and courage'}
- Philosophical angles: {'; '.join(philosophical) if philosophical else 'the journey of becoming'}
- Growth signs: {'; '.join(growth) if growth else 'vulnerability and self-reflection'}

REQUIREMENTS:
1. Use the EXACT same format markers as the examples: [INTRO - Host 1], [Host 2], [OVERLAP - Host 1], [OUTRO - Host 2], etc.
2. Make it deeply personal and specific to THIS conversation - reference actual quotes and moments
3. Include therapeutic reframes and philosophical insights like the examples
4. Feel warm, conversational, and sometimes overlapping like real friends talking
5. Sarah (Host 1) tends to be more philosophical, Rachel (Host 2) more therapeutic
6. Address the specific struggles and growth signs from this person's sharing
7. End with genuine encouragement and wisdom
8. Match the natural flow and conversational style of the examples

Create a script that feels like it was written by the same caring hosts who wrote the examples.
"""
            
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a script writer for the therapeutic podcast 'Deep Reflections.' Study the example scripts carefully and create a new script that matches their warmth, insight, and conversational flow exactly. Always use the same format markers and maintain the caring, therapeutic tone."},
                {"role": "user", "content": script_prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        script = response.choices[0].message.content.strip()
        print("✅ OpenAI script generation complete (with example context)")
        return script
    
    
    
    def text_to_speech_playht(self, text: str, voice_id: str, filename: str) -> bool:
        """
        Convert text to speech using Play.ht API.
        
        Args:
            text: Text to convert to speech
            voice_id: Play.ht voice ID
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import time
            
            # Step 1: Create the TTS job
            create_url = "https://api.play.ht/api/v2/tts"
            
            headers = {
                "Authorization": f"Bearer {self.playht_api_key}",
                "X-User-ID": self.playht_user_id,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "voice": voice_id,
                "quality": "premium",
                "output_format": "mp3",
                "speed": 1.0,
                "sample_rate": 24000
            }
            
            response = requests.post(create_url, json=data, headers=headers)
            
            if response.status_code != 201:
                print(f"❌ Error creating Play.ht job: {response.status_code} - {response.text}")
                return False
            
            job_data = response.json()
            job_id = job_data.get("id")
            
            if not job_id:
                print("❌ No job ID returned from Play.ht")
                return False
            
            # Step 2: Poll for completion
            status_url = f"https://api.play.ht/api/v2/tts/{job_id}"
            max_attempts = 30  # 30 seconds max wait
            
            for attempt in range(max_attempts):
                status_response = requests.get(status_url, headers=headers)
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    
                    if status_data.get("output") and status_data["output"].get("url"):
                        # Step 3: Download the audio
                        audio_url = status_data["output"]["url"]
                        audio_response = requests.get(audio_url)
                        
                        if audio_response.status_code == 200:
                            with open(filename, "wb") as f:
                                f.write(audio_response.content)
                            print(f"✅ Generated Play.ht audio: {filename}")
                            return True
                        else:
                            print(f"❌ Error downloading audio: {audio_response.status_code}")
                            return False
                    
                    elif status_data.get("status") == "error":
                        print(f"❌ Play.ht job failed: {status_data.get('error', 'Unknown error')}")
                        return False
                
                time.sleep(1)  # Wait 1 second before polling again
            
            print("❌ Play.ht job timed out")
            return False
                
        except Exception as e:
            print(f"❌ Error in Play.ht text_to_speech: {str(e)}")
            return False
        
    def text_to_speech(self, text: str, voice_id: str, filename: str) -> bool:
        """
        Convert text to speech using the configured TTS provider with fallback.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID for the configured provider
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if self.tts_provider == "playht":
            success = self.text_to_speech_playht(text, voice_id, filename)
            if not success:
                print("⚠️  Play.ht failed, falling back to ElevenLabs...")
                # Switch to ElevenLabs voice IDs and try again
                fallback_voice = self.elevenlabs_host_1 if voice_id == self.playht_host_1 else self.elevenlabs_host_2
                return self.text_to_speech_elevenlabs(text, fallback_voice, filename)
            return success
        else:
            return self.text_to_speech_elevenlabs(text, voice_id, filename)
    
    def text_to_speech_elevenlabs(self, text: str, voice_id: str, filename: str) -> bool:
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
            elif any(marker in line for marker in ["[Host 1]", "[INTRO - Host 1]", "[MAIN DISCUSSION - Host 1]", "[OUTRO - Host 1]"]):
                if current_segment:
                    segments.append((current_segment, current_voice, "normal"))
                # Remove ALL possible markers from the line
                text = line
                for marker in ["[Host 1]", "[INTRO - Host 1]", "[MAIN DISCUSSION - Host 1]", "[OUTRO - Host 1]"]:
                    text = text.replace(marker, "")
                current_segment = text.strip()
                current_voice = self.host_1_voice_id
            elif any(marker in line for marker in ["[Host 2]", "[INTRO - Host 2]", "[MAIN DISCUSSION - Host 2]", "[OUTRO - Host 2]"]):
                if current_segment:
                    segments.append((current_segment, current_voice, "normal"))
                # Remove ALL possible markers from the line
                text = line
                for marker in ["[Host 2]", "[INTRO - Host 2]", "[MAIN DISCUSSION - Host 2]", "[OUTRO - Host 2]"]:
                    text = text.replace(marker, "")
                current_segment = text.strip()
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
            
            # Detect non-silent chunks with gentler settings
            nonsilent_chunks = detect_nonsilent(
                audio_segment, 
                min_silence_len=200,  # 200ms minimum silence (more conservative)
                silence_thresh=silence_thresh
            )
            
            if not nonsilent_chunks:
                return audio_segment  # Return original if no non-silent parts found
            
            # Get the first and last non-silent chunk
            start_trim = nonsilent_chunks[0][0]
            end_trim = nonsilent_chunks[-1][1]
            
            # Trim with more generous padding to preserve natural speech endings
            start_padding = 100  # 100ms padding at start
            end_padding = 200    # 200ms padding at end (more generous for natural endings)
            start_trim = max(0, start_trim - start_padding)
            end_trim = min(len(audio_segment), end_trim + end_padding)
            
            return audio_segment[start_trim:end_trim]
            
        except ImportError:
            # If pydub.silence not available, return original
            return audio_segment
        except Exception:
            # If trimming fails for any reason, return original
            return audio_segment
    
    def _trim_silence_gentle(self, audio_segment: 'AudioSegment', silence_thresh: int = -50) -> 'AudioSegment':
        """
        Very gentle silence trimming that preserves natural speech patterns.
        
        Args:
            audio_segment: The audio segment to trim
            silence_thresh: Silence threshold in dB (higher = less sensitive)
        
        Returns:
            Gently trimmed audio segment
        """
        try:
            from pydub.silence import detect_nonsilent
            
            # Use very conservative settings
            nonsilent_chunks = detect_nonsilent(
                audio_segment, 
                min_silence_len=300,  # 300ms minimum silence (very conservative)
                silence_thresh=silence_thresh  # Less sensitive threshold
            )
            
            if not nonsilent_chunks:
                return audio_segment
            
            # Get the first and last non-silent chunk
            start_trim = nonsilent_chunks[0][0]
            end_trim = nonsilent_chunks[-1][1]
            
            # Use very generous padding to preserve natural speech
            start_padding = 150  # 150ms padding at start
            end_padding = 300    # 300ms padding at end (very generous)
            start_trim = max(0, start_trim - start_padding)
            end_trim = min(len(audio_segment), end_trim + end_padding)
            
            return audio_segment[start_trim:end_trim]
            
        except ImportError:
            return audio_segment
        except Exception:
            return audio_segment
    
    def _normalize_volume(self, audio_segment: 'AudioSegment', target_dBFS: float = -20.0) -> 'AudioSegment':
        """
        Normalize audio volume to a target level.
        
        Args:
            audio_segment: The audio segment to normalize
            target_dBFS: Target volume level in dBFS
        
        Returns:
            Volume-normalized audio segment
        """
        try:
            # Calculate the difference between current and target volume
            change_in_dBFS = target_dBFS - audio_segment.dBFS
            
            # Apply the volume change
            normalized_audio = audio_segment.apply_gain(change_in_dBFS)
            
            return normalized_audio
            
        except Exception:
            # If normalization fails, return original
            return audio_segment
    
    def _add_with_crossfade(self, combined: 'AudioSegment', new_segment: 'AudioSegment', 
                           pause: 'AudioSegment', crossfade_ms: int = 100) -> 'AudioSegment':
        """
        Add a new segment with a smooth crossfade to reduce choppy transitions.
        
        Args:
            combined: The existing combined audio
            new_segment: The new segment to add
            pause: Silence to add between segments
            crossfade_ms: Crossfade duration in milliseconds
        
        Returns:
            Combined audio with smooth transition
        """
        try:
            from pydub import AudioSegment as AS
            
            # Add the pause first
            combined_with_pause = combined + pause
            
            # Check if we have enough audio for crossfade
            if len(combined_with_pause) < crossfade_ms or len(new_segment) < crossfade_ms:
                # Not enough audio for crossfade, just concatenate
                return combined_with_pause + new_segment
            
            # Create crossfade
            # Take the last part of combined and first part of new segment
            combined_end = combined_with_pause[-crossfade_ms:]
            new_start = new_segment[:crossfade_ms]
            
            # Fade out the end of combined, fade in the start of new
            combined_end_faded = combined_end.fade_out(crossfade_ms)
            new_start_faded = new_start.fade_in(crossfade_ms)
            
            # Overlay them
            crossfaded_section = combined_end_faded.overlay(new_start_faded)
            
            # Combine: everything before crossfade + crossfaded section + rest of new segment
            result = (combined_with_pause[:-crossfade_ms] + 
                     crossfaded_section + 
                     new_segment[crossfade_ms:])
            
            return result
            
        except Exception as e:
            # If crossfade fails, fall back to simple concatenation
            print(f"   ⚠️ Crossfade failed, using simple join: {str(e)}")
            return combined + pause + new_segment
    
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
            
            # Load first segment with gentle trimming
            combined = AudioSegment.from_mp3(first_file)
            combined = self._trim_silence_gentle(combined)  # Use gentler trimming for first segment
            combined = self._normalize_volume(combined)
            
            # Natural conversation timing with more breathing room
            tiny_pause = AudioSegment.silent(duration=200)     # 0.2 seconds - quick but natural
            short_pause = AudioSegment.silent(duration=400)    # 0.4 seconds - comfortable pause
            normal_pause = AudioSegment.silent(duration=600)   # 0.6 seconds - natural breath
            
            for i, audio_info in enumerate(audio_files[1:], 1):
                if isinstance(audio_info, tuple):
                    audio_file, timing_info = audio_info
                else:
                    audio_file = audio_info
                    timing_info = "normal"
                
                # Load and trim silence from this segment
                segment = AudioSegment.from_mp3(audio_file)
                # Use gentler trimming for first few segments (intro is important)
                if i <= 3:  # First 3 segments get gentle treatment
                    segment = self._trim_silence_gentle(segment)
                else:
                    segment = self._trim_silence(segment)
                # Normalize volume levels
                segment = self._normalize_volume(segment)
                
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
                    # Trim both segments and add with crossfade
                    combined = self._trim_silence(combined)
                    combined = self._add_with_crossfade(combined, segment, short_pause)
                    print(f"   ➡️  Added segment {i+1} with smooth crossfade")

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
    parser.add_argument("--sample", "-s", default="heavy_emotional_disclosure", help="Use a sample conversation (heavy_emotional_disclosure, goal_setting_accountability, light_reflective_checkin, crisis_management, long_term_patterns)")
    parser.add_argument("--script-file", help="Path to a pre-written script file (instead of transcript/sample)")
    parser.add_argument("--combine-only", action="store_true", help="Just combine existing segments/ files")
    parser.add_argument("--api-key", default="", help="ElevenLabs API key")
    parser.add_argument("--playht-key", default="", help="Play.ht API key")
    parser.add_argument("--playht-user", default="", help="Play.ht User ID")
    parser.add_argument("--openai-key", default="", help="OpenAI API key for script generation")
    parser.add_argument("--use-playht", default=False, action="store_true", help="Force use Play.ht instead of ElevenLabs")
    
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
    
    # Get Play.ht credentials
    playht_key = args.playht_key or os.getenv("PLAYHT_API_KEY")
    playht_user = args.playht_user or os.getenv("PLAYHT_USER_ID")
    
    # Get OpenAI API key
    openai_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️ OpenAI API key not provided - using fallback script generation")
        print("   Provide with --openai-key or OPENAI_API_KEY environment variable for AI generation")
    
    # Initialize the generator
    generator = AIPodcastGenerator(api_key, playht_key, playht_user, openai_key)
    
    # Override to use Play.ht if requested
    if args.use_playht and playht_key and playht_user:
        generator.tts_provider = "playht"
        generator.host_1_voice_id = generator.playht_host_1
        generator.host_2_voice_id = generator.playht_host_2
        print(f"🎙️ Using TTS provider: PLAY.HT (forced)")
        print(f"   Play.ht voices: Jennifer & Michael")
    else:
        print(f"🎙️ Using TTS provider: ELEVENLABS (default)")
        print(f"   ElevenLabs voices: Rachel & Elli")
    
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