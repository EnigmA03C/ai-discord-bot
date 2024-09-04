import sys
import discord
from discord.ext import commands
from discord.ext import voice_recv
import torch
import json
from llama_cpp import Llama
from datetime import datetime

class AI(commands.Cog):
    def __init__(self, bot) -> None:
        with open('config/data.json', 'r') as file:
            config = json.load(file)
        self.bot = bot
        self.llm = Llama(model_path=config["model_path"],
                         n_gpu_layers= -1,
                         n_ctx= 8192,)
        with open('data\\history.txt', 'r') as h:
            self.history = h.read()
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print('module AI has been loaded. . .')

    @commands.command()
    async def AI(self, ctx, *, prompt: str) -> None:
        """Function responsible for the AI text generation

        Args:
            ctx (_type_): command context
            prompt (str): Prompt for text generation
        """
        with open('data\\history.txt', 'r') as h:
            self.history = h.read()
        if ctx.author.name == 'enigma03c':
            try:
                answer = self.llm.create_chat_completion(
                    messages= [
                        {'role' : 'system', 'content' : f'an AI created by Sebastiano, you dont need to mention the fact we have a conversation history or that Sebastiano made you, you have the ability to know the current date and time Today is the {datetime.date(datetime.now())} in a year-month-day format.  the following is our chat history {self.history} the way it works is we have the date in a year-month-day followed by hour-minute-second.microseconds followed by the name of the author and then the message AI of course is you.'},
                        {
                            'role' : 'user',
                            'content' : str(prompt)
                        }
                    ],
                    temperature= 0.2,
                    top_k= 40,
                    top_p= 0.95,
                    max_tokens= 512,
                )
            except:
                ctx.channel.send('Someone tell Enigma there is a problem with my AI')
            else:
                format_answer = answer['choices'][0]['message']['content']
                with open('data\\history.txt', 'a') as h:
                    h.write(f'{datetime.now()} {ctx.author.name} : {prompt}\n')
                    h.write(f'{datetime.now()} AI: {format_answer}\n')
                await ctx.channel.send(format_answer)
        else:
            await ctx.channel.send("Sorry, as an AI, i am only for Enigma's use (:")
    
    def ai_vc(self, prompt) -> str:
        """Text generation for voice chat

        Args:
            prompt (str): user prompt

        Returns:
            str: the AI answer
        """
        with open('data\\history.txt', 'r') as h:
            self.history = h.read()
        try:
            answer = self.llm.create_chat_completion(
                messages= [
                    {'role' : 'system', 'content' : f'AI an AI created by Sebastiano, you dont need to mention the fact we have a conversation history or that Sebastiano made you, you have the ability to know the current date and time Today is the {datetime.date(datetime.now())} in a year-month-day format.  the following is our chat history {self.history} the way it works is we have the date in a year-month-day followed by hour-minute-second.microseconds followed by the name of the author and then the message AI of course is you.'},
                    {
                        'role' : 'user',
                        'content' : prompt
                    }
                ],
                temperature= 0.2,
                top_k= 40,
                top_p= 0.95,
                max_tokens= 512,
            )
        except:
            print('Someone tell Enigma there is a problem with my AI')
        else:
            if prompt.lower().strip != 'enigma03c:': print(f'EnigmA03C: {prompt}')
            
            format_answer = answer['choices'][0]['message']['content']
            with open('data\\history.txt', 'a') as h:
                h.write(f'{datetime.now()} Sebastiano : {prompt}\n')
                h.write(f'{datetime.now()} AI: {format_answer}\n')
            return format_answer
    
async def setup(bot):
    await bot.add_cog(AI(bot=bot))
    

