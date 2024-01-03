# huggingface auth token for read access to the llama2 7B param chat model
HF_TOKEN="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"

# general config.json
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/config.json -O ../model_artifacts/config.json
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/configuration_RW.py -O ../model_artifacts/chatbot/falcon/configuration_RW.py
wget https://huggingface.co/tiiuae/falcon-7b-instruct/resolve/main/modelling_RW.py -O ../model_artifacts/chatbot/falcon/modelling_RW.py

# tokenizer and tokenizer config
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/tokenizer_config.json -O ../model_artifacts/tokenizer_config.json
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/tokenizer.json -O ../model_artifacts/tokenizer.json
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/special_tokens_map.json -O ../model_artifacts/special_tokens_map.json

# model in .safetensors format
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/model-00001-of-00002.safetensors -O ../model_artifacts/model-00001-of-00002.safetensors
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/model-00002-of-00002.safetensors -O ../model_artifacts/model-00002-of-00002.safetensors
wget --header="Authorization: Bearer $HF_TOKEN" https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/resolve/main/model.safetensors.index.json -O ../model_artifacts/model.safetensors.index.json
