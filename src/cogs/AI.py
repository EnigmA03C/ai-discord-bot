from discord.ext import commands
import json
import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

class AI(commands.Cog):
    def __init__(self, bot) -> None:
        with open('src/config/data.json', 'r') as file:
            config = json.load(file)
        
        self.bot = bot
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit= True,
            bnb_4bit_quant_type= 'fp4',
            bnb_4bit_use_double_quant= False,
            bnb_4bit_compute_dtype= torch.float16
        )

        self.tokenizer = AutoTokenizer.from_pretrained(config["model_path"])
        self.model = AutoModelForCausalLM.from_pretrained(config["model_path"], quantization_config = self.bnb_config)

        with open('src/data/history.txt', 'r') as h:
            self.history = h.read()
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'module AI has been loaded. . . with state {self.device}')

    @commands.command()
    async def AI(self, ctx, *, prompt: str) -> None:
        system_message = f"an AI created by Sebastiano to chat and be entertaining"
        user_message = prompt
        input_text = f"System: {system_message}\nUser: {user_message}\nAI:\n"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        outputs = self.model.generate(
            inputs["input_ids"],
            max_new_tokens= 512,
            temperature=0.2,
            top_k=40,
            top_p=0.95,
            do_sample=True,
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        format_answer = answer[len(input_text):].strip()
        
        await ctx.channel.send(format_answer)
    
    def ai_vc(self, prompt) -> str:
        system_message = f"an AI created by Sebastiano to chat and be entertaining"
        user_message = prompt
        input_text = f"System: {system_message}\nUser: {user_message}\nAI:\n"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        outputs = self.model.generate(
            inputs["input_ids"],
            max_new_tokens= 130,
            temperature=0.2,
            top_k=40,
            top_p=0.95,
            do_sample=True,
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        format_answer = answer[len(input_text):].strip()
        
        return format_answer
    
async def setup(bot):
    await bot.add_cog(AI(bot=bot))
    

