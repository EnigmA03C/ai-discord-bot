import discord
from discord.ext import commands
from discord.ext.voice_recv import VoiceRecvClient, AudioSink, VoiceData
from discord.ext.voice_recv.extras import SpeechRecognitionSink 
import speech_recognition as sr
import numpy as np
import whisper
import torch
from TTS.api import TTS

class Voice(commands.Cog):
    whisper_model = whisper.load_model("base", device=torch.device(0))
    
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('module Voice has been loaded. . .')
    
    @commands.command()
    async def join(self, ctx) -> None:
        """command for the bot to join the vc

        Args:
            ctx (context): command context

        Returns:
            None
        """
        channel = ctx.author.voice.channel
        ai_voice = self.bot.get_cog('AI')
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device=0)
        
        if ctx.author.name in ('enigma03c', 'dragonrage9911956'):
            if channel: 
                try:
                    def process_whisper(recognizer: sr.Recognizer.adjust_for_ambient_noise, audio: sr.AudioData, user):
                        self.default_recognizer = 'whisper'
                        try:
                            func = getattr(recognizer, 'recognize_' + self.default_recognizer, recognizer.recognize_whisper)
                            text = str(func(audio, language= 'english', translate= False)).lower().strip()
                            
                            if text and text != 'you':
                                if(not voice_client.is_playing()):
                                    answer = ai_voice.ai_vc(text)
                                
                                    tts.tts_to_file(text=answer,
                                    file_path="src/data/voice/AI_Output.wav",
                                    speaker_wav=["src/data/voice/AI_Voice.wav"],
                                    language="en")
                                
                                    ctx.voice_client.play(discord.FFmpegPCMAudio("data/voice/AI_Output.wav"))
                                else:
                                    return
                            else:
                                pass
                        except sr.UnknownValueError:
                            print('Bad speech chunk')
                        
                        return text
                    
                    voice_client = await channel.connect(cls= VoiceRecvClient)
                    voice_client.listen(SpeechRecognitionSink(process_cb=process_whisper, default_recognizer= self.whisper_model, ignore_silence_packets= False, phrase_time_limit=30))
                    await ctx.channel.send(f'Got it, moving to voice channel {ctx.author.voice.channel.name} and directing output to {ctx.author.voice.channel}.')
                except Exception as e:
                    await ctx.channel.send(f"Failed to connect to the voice channel: {str(e)}")
            else:
                await ctx.send("Couldn't join the channel, someone tell enigma to enter first")
                return
        else:
            await ctx.send("Im sorry i only obey Enigma C:")
    
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Voice(bot))
