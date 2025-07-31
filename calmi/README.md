# AI Podcast Generator for Sid :)

A Python script that transforms conversation transcripts into AI-generated podcast episodes with therapeutic insights, philosophical reflections, and warm conversational tone.

## Features

- **Conversation Analysis**: Automatically detects themes and emotional patterns in transcripts
- **Therapeutic Insights**: Generates psychotherapy-informed perspectives and reframing
- **Philosophical Reflections**: Incorporates big-picture thinking and meaning-making
- **Dual Host Format**: Uses two AI voices for natural conversation flow
- **ElevenLabs Integration**: High-quality text-to-speech with podcast-optimized voices
- **Sample Conversations**: Built-in examples for testing and demonstration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

You'll need an ElevenLabs API key. You can either:

- Set it as an environment variable:
  ```bash
  export ELEVENLABS_API_KEY="your_api_key_here"
  ```
- Or pass it directly with the `--api-key` flag

### 3. Generate Your First Podcast

Try one of the sample conversations:

```bash
python ai_podcast_generator.py --sample heavy_emotional_disclosure --api-key "your_api_key_here"
```

Or use your own transcript:

```bash
python ai_podcast_generator.py --transcript my_conversation.txt --output my_podcast.mp3 --api-key "your_api_key_here"
```

## Usage Examples

### Sample Conversations

The script includes 5 sample conversations for testing:

1. **heavy_emotional_disclosure** - Deep vulnerability and relationship fears
2. **goal_setting_accountability** - Entrepreneurship and overcoming resistance
3. **light_reflective_checkin** - Mindful appreciation and gratitude
4. **crisis_management** - Job loss and uncertainty
5. **long_term_patterns** - Therapy insights and relationship patterns

### Command Line Options

```bash
python ai_podcast_generator.py [OPTIONS]

Options:
  --transcript, -t    Path to transcript file
  --output, -o        Output filename (default: ai_podcast.mp3)
  --sample, -s        Use a sample conversation
  --api-key          ElevenLabs API key
```

### Examples

```bash
# Generate podcast from sample conversation
python ai_podcast_generator.py --sample crisis_management

# Generate podcast from custom transcript
python ai_podcast_generator.py --transcript my_talk.txt --output my_episode.mp3

# Use environment variable for API key
export ELEVENLABS_API_KEY="sk_9826ff690460e4e48e6a9d0e238e172d209e1c03489353f7"
python ai_podcast_generator.py --sample goal_setting_accountability

python ai_podcast_generator.py --transcript dennis_breakup_transcript.txt --output dennis_breakup_podcast.mp3

```

## Output

The script generates:

1. **MP3 Audio File**: The final podcast episode
2. **Text Script**: A transcript of the generated podcast for reference

## How It Works

### 1. Conversation Analysis
The script analyzes the transcript to identify:
- Key themes (anxiety, relationships, goals, etc.)
- Emotional tone
- Therapeutic angles for intervention

### 2. Script Generation
Creates a podcast script that includes:
- Warm introduction setting the tone
- Main discussion with therapeutic insights
- Philosophical reflections on meaning and purpose
- Encouraging conclusion

### 3. Voice Generation
Uses ElevenLabs API to convert text to speech with:
- Two distinct voices for natural conversation
- Podcast-optimized voice settings
- Proper pacing and tone

### 4. Audio Assembly
Combines all audio segments into a final MP3 file.

## API Keys

### ElevenLabs
- **API Key**: `sk_9826ff690460e4e48e6a9d0e238e172d209e1c03489353f7`
- **Purpose**: Text-to-speech conversion
- **Features**: High-quality voices, podcast optimization

### Play.ht (Future Use)
- **API Key**: `ak-030965aa9519486c97708d3c41c8fa39`
- **User ID**: `lo7OKbDgCQgdU4BdkR4jOnWjXc73`
- **Purpose**: Alternative TTS option for future development

## Voice Configuration

The script uses two ElevenLabs voices:
- **Host 1**: Rachel (warm, conversational)
- **Host 2**: Domi (thoughtful, supportive)

You can change these by modifying the `voice_id` values in the `AIPodcastGenerator` class.

## Customization

### Modifying the Script Template
Edit the `generate_podcast_script()` method to change the podcast structure and tone.

### Adding New Themes
Extend the `analyze_conversation()` method to detect additional themes and patterns.

### Voice Settings
Adjust voice parameters in the `text_to_speech()` method for different styles.

## Future Enhancements

### Pipeline 2 Features
- Research paper integration
- External resource retrieval
- Evidence-based insights

### Audio Improvements
- Background music integration
- Sound effects and transitions
- Professional audio mixing

### Analysis Enhancements
- Sentiment analysis
- Emotion detection
- Pattern recognition

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your ElevenLabs API key is valid and has sufficient credits
2. **Audio Generation Fails**: Check your internet connection and API quota
3. **Empty Transcript**: Ensure your transcript file contains text

### Debug Mode
Add print statements in the script to see detailed progress information.

## License

This project is created for Sid's AI podcast feature development.

## Support

For questions or issues, check the ElevenLabs API documentation or review the script's error messages for guidance. 
