# fine-tuning 하기
```
python tr.py --model_name_or_path=skt/kogpt2-base-v2 --train_file=data.txt --validation_file=data.txt --do_train --do_eval --num_train_epochs=10 --save_steps=10000 --save_total_limit=3 --per_device_train_batch_size=1 --per_device_eval_batch_size=1 --output_dir=output --use_fast_tokenizer=False
```
