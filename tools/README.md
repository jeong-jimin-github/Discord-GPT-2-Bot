# Data 생성하기
* [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)를 사용해 다음 형식과 같은 CSV파일을 준비한다. (example.csv 참조)
```
AuthorID, Author, Date, Content, Attachments, Reactions
```
* 다음 명령어를 입력해 data.txt를 생성한다.
```
python .py
```

생성된 data.txt의 형식은 다음과 같아야 한다.
```
</s>입력[SEP]출력</s>
```

# fine-tuning 하기
* 다음 명령어를 입력해 fine-tuning 작업을 시작한다. (이 작업은 GPU로 하기를 <b>강력히</b> 추천한다.)
```
python tr.py --model_name_or_path=skt/kogpt2-base-v2 --train_file=data.txt --validation_file=data.txt --do_train --do_eval --num_train_epochs=10 --save_steps=10000 --save_total_limit=3 --per_device_train_batch_size=1 --per_device_eval_batch_size=1 --output_dir=output --use_fast_tokenizer=False
```
