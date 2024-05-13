from llama_cpp import Llama
import argparse
import os 

def main(FLAGS):
  
  if os.path.isfile(FLAGS.target_file):
    print("Model file already exists")
  else:
    os.system(f"wget -O {FLAGS.target_file} {FLAGS.download_link}")
  
  # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
  llm = Llama(
    model_path=FLAGS.model_name,  # Download the model file first
    n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=FLAGS.n_threads,            # The number of CPU threads to use, tailor to your system and the resulting performance
  )

  # Simple inference example
  output = llm(
    f"### System:\n{FLAGS.sys_prompt}\n### User:\n{FLAGS.prompt}\n### Assistant:", # Prompt
    max_tokens=FLAGS.max_token,  # Generate up to 512 tokens
    stop=[f"{FLAGS.stop_token}"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
    echo=True        # Whether to echo the prompt
  )
  
  print(output['choices'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-m',
                        '--model_name',
                        type=str,
                        default="./neural-chat-7b-v3-3.Q4_K_M.gguf",
                        help="models")
    parser.add_argument('-r',
                        '--download_link',
                        type=str,
                        default="https://huggingface.co/TheBloke/neural-chat-7B-v3-3-GGUF/resolve/main/neural-chat-7b-v3-3.Q4_K_M.gguf?download=true",
                        help="file download link")
    parser.add_argument('-f',
                        '--target_file',
                        type=str,
                        default="neural-chat-7b-v3-3.Q4_K_M.gguf",
                        help="file name in repo")
    parser.add_argument('-p',
                        '--prompt',
                        type=str,
                        default="Can you help me?",
                        help="prompt for the model")
    parser.add_argument('-s',
                        '--sys_prompt',
                        type=str,
                        default="You are a useful and professional chatbot",
                        help="system prompt")
    parser.add_argument('-ts',
                        '--stop_token',
                        type=str,
                        default="</s>",
                        help="select stop token")
    parser.add_argument('-n',
                        '--n_threads',
                        type=int,
                        default="16",
                        help="CPU threads")
    parser.add_argument('-ptk',
                        '--max_token',
                        type=int,
                        default="512",
                        help="Max tokens")
    FLAGS = parser.parse_args()
    main(FLAGS)