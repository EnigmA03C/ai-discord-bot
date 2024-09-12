from discord.ext import commands
import json
import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        with open("src/config/data.json", "r") as file:
            config = json.load(file)

        self.bot = bot

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="fp4",
            bnb_4bit_use_double_quant=False,
            bnb_4bit_compute_dtype=torch.float16,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(config["model_path"])
        self.model = AutoModelForCausalLM.from_pretrained(
            config["model_path"], quantization_config=self.bnb_config
        )

        self.tokenizer.pad_token = self.tokenizer.eos_token

        with open("src/data/history.txt", "r") as h:
            self.history = h.read()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"module AI has been loaded. . . with state {self.device}")

    @commands.Cog.listener("on_message")
    async def on_message(self, ctx: commands.Context) -> None:
        if ctx.author.id != self.bot.user.id:
            system_message = "an AI created by Sebastiano to chat and be entertaining. "
            user_message = str(ctx.content)
            input_text = f"{system_message}\n{user_message}<|end_of_text|>"

            inputs = self.tokenizer(text=input_text, padding=True, return_tensors="pt")
            inputs = {key: value.to(self.device) for key, value in inputs.items()}

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    temperature=0.2,
                    top_k=40,
                    top_p=0.95,
                    eos_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                )

            answer = self.tokenizer.batch_decode(
                outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]

            format_answer = answer[len(input_text) :].strip()

            await ctx.channel.send(format_answer)
        else:
            return

    def ai_vc(self, prompt) -> str:
        system_message = "an AI created by Sebastiano to chat and be entertaining"
        user_message = prompt
        input_text = f"System: {system_message}\nUser: {user_message}\nAI:\n"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=160,
                temperature=0.2,
                top_k=40,
                top_p=0.95,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        answer = self.tokenizer.decode(
            outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        format_answer = answer  # [len(input_text) :].strip()

        return format_answer


async def setup(bot):
    await bot.add_cog(AI(bot=bot))
