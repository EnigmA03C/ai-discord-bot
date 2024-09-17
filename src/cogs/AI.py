from discord.ext import commands
import json
import datetime
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)


class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        with open("src/config/data.json", "r") as file:
            self.config = json.load(file)

        self.bot = bot

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config["model_path"],
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config["model_path"],
            quantization_config=self.bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
        )

        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
        )

        self.terminators = [
            self.pipe.tokenizer.eos_token_id,
            self.pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        with open("src/data/history.txt", "r") as h:
            self.history = h.read()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"module AI has been loaded. . . with state {self.device}")

    @commands.Cog.listener("on_message")
    async def on_message(self, ctx: commands.Context) -> None:
        if ctx.author.id != self.bot.user.id:
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI created by Sebastiano to be entertaining",
                },
                {"role": "user", "content": ctx.content},
            ]

            outputs = self.pipe(
                messages,
                eos_token_id=self.terminators,
                do_sample=True,
                max_length=256,
                temperature=0.2,
                top_k=40,
                top_p=0.95,
            )

            answer = outputs[0]["generated_text"][-1]

            await ctx.channel.send(answer["content"])
        else:
            return

    def ai_vc(self, prompt) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an AI created by Sebastiano to be entertaining",
            },
            {"role": "user", "content": prompt},
        ]

        outputs = self.pipe(
            messages,
            eos_token_id=self.terminators,
            do_sample=True,
            max_length=256,
            temperature=0.2,
            top_k=40,
            top_p=0.95,
        )
        answer = outputs[0]["generated_text"][-1]

        return answer["content"]


async def setup(bot):
    await bot.add_cog(AI(bot=bot))
