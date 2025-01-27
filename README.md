# AI-Wife
This code is designed to listen to a microphone and then use OpenAI's GPT language model to generate responses. The output from GPT is then read out loud using a TTS (Text-to-Speech) engine provided by ElevenLabs.



# Setup
Install dependencies
```
git clone 
cd ai-wife
pip install -r requirements.txt
```

# Usage

Edit the variables `openai_api_key` and `elevenlabs_api_key` in `config.json`

`elevenlabs_api_key` is the API key for [ElevenLabs](https://beta.elevenlabs.io/). Found in Profile Settings

`openai_api_key` is the API key for OpenAI. Found [here](https://platform.openai.com/account/api-keys)

Then run `run.py`

### Default TTS
```
python run.py --pyttsx3
```
### Elevenlabs TTS
```
python run.py --elevenlabs
```
then you're set

# Video
[My ai wife](https://youtu.be/2NLH_cp3XQQ)

<a href="https://youtu.be/2NLH_cp3XQQ" target="_blank">
    <img src="https://img.youtube.com/vi/2NLH_cp3XQQ/0.jpg" 
         alt="My ai wife" width="240" height="180" border="10" />
</a>


# Note

Please note that this project was created solely for fun and as part of a YouTube video, so the quality and reliability of the code may be questionable. Also, after the completion of the project checklist, there won't be much activity in updating or improving this repository. Nonetheless, we hope that this project can serve as a source of inspiration for anyone interested in building their own AI stuff u know

# License
This program is under the [MIT license](/LICENSE) 

