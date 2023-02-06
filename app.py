from pathlib import Path
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import torch
import discord

output = Path("./output") #fine-tuning된 모델 경로
channel =  #봇이 작동할 Discord Channel ID (int)
token = "" #Discord Developer Portal에서 발급받은 봇의 Token
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #CUDA설치 시 GPU, 미설치 시 CPU로 작동
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", #한국어는 "skt/kogpt2-base-v2", 일본어는 "rinna/japanese-gpt2-medium"
  bos_token='</s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token='<mask>')
model = GPT2LMHeadModel.from_pretrained(output)
model.to(device)
model.eval()

def generate_reply(inp, num_gen=1):
    input_text = "<s>" + str(inp) + "[SEP]"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    out = model.generate(input_ids, do_sample=True, max_length=128, num_return_sequences=num_gen,
                        top_p=0.95, top_k=50, no_repeat_ngram_size=2)
 #input = inp
    for sent in tokenizer.batch_decode(out):
        try:
            sent = sent.split('[SEP]')[1]
            sent = sent.replace('<s>', '')
            sent = sent.replace('</s>', '\n')
            return(sent)
        except:
            return(sent)

class GPTBot(discord.Client):
    async def on_ready(self):
        print(self.user + " | Started") #Terminal로 시작됨을 알림

    async def on_message(self, message):
        if message.author == self.user: #봇이 보낸 메세지일 경우 무시
            return
        if message.channel == self.get_channel(channel):
            await message.channel.send(generate_reply(message.content))

intents = discord.Intents.default()
intents.message_content = True
client = GPTBot(intents=intents)
client.run(token)
