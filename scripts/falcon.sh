# some config
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/config.json -O ../model_artifacts/chatbot/falcon/config.json
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/configuration_RW.py -O ../model_artifacts/chatbot/falcon/configuration_RW.py

# tokenizer and tokenizer config 
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/tokenizer_config.json -O ../model_artifacts/chatbot/falcon/tokenizer_config.json
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/tokenizer.json -O ../model_artifacts/chatbot/falcon/tokenizer.json
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/special_tokens_map.json -O ../model_artifacts/chatbot/falcon/special_tokens_map.json


# model weights and index
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/pytorch_model-00001-of-00002.bin -O ../model_artifacts/chatbot/falcon/pytorch_model-00001-of-00002.bin
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/pytorch_model-00002-of-00002.bin -O ../model_artifacts/chatbot/falcon/pytorch_model-00002-of-00002.bin
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/pytorch_model.bin.index.json -O ../model_artifacts/chatbot/falcon/pytorch_model.bin.index.json
