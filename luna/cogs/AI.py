import sys
import discord
from discord.ext import commands
from discord.ext import voice_recv
import torch
import json
from datetime import datetime
import transformers

class AI(commands.Cog):
    def __init__(self, bot) -> None:
        with open('C:\\Users\\sdang\\source\\repos\\ai-discord-bot\\config\\data.json', 'r') as file:
            config = json.load(file)
        self.bot = bot
        
        self.bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type = 'fp4',
            bnb_4bit_use_double_quant=False,
            bnb_4bit_compute_dtype=torch.float16,
        )
        
        self.model_name = config["model_path"]
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.model_name)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(self.model_name, quantization_config = self.bnb_config)
        
        self.llm = transformers.pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                
        with open('data\\history.txt', 'r') as h:
            self.history = h.read()
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print('module AI has been loaded. . .')

    @commands.command()
    async def AI(self, ctx, *, prompt: str) -> None:
        try:
            messages = [
                {"role": "system", "content": "You are my AI assistant"},
                {"role": "user", "content": prompt},
            ]
            
            outputs = self.llm(messages,
                               max_new_tokens = 256,
                               temperature = 0.2,
                               top_k = 40,
                               top_p = 0.95,
                               )
            
            await ctx.channel.send(outputs[0]["generated_text"][-1])
        except Exception as e:
            await ctx.channel.send(e)
    
    def ai_vc(self, prompt) -> str:
        """Text generation for voice chat

        Args:
            prompt (str): user prompt

        Returns:
            str: the AI answer
        """
        with open('C:\\Users\\sdang\\source\\repos\\ai-discord-bot\\data\\history.txt', 'r') as h:
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
    

