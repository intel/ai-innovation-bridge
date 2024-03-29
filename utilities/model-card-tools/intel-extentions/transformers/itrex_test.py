import argparse
from transformers import AutoTokenizer
from intel_extension_for_transformers.transformers import AutoModelForCausalLM


def main(FLAGS):
  
    tokenizer = AutoTokenizer.from_pretrained(FLAGS.model, trust_remote_code=True)
    inputs = tokenizer(FLAGS.prompt, return_tensors="pt").input_ids  
    model = AutoModelForCausalLM.from_pretrained(FLAGS.model, load_in_4bit=True)
    raw_tokens = model.generate(inputs, max_new_tokens=10)
    prediction = tokenizer.decode(raw_tokens[0], skip_special_tokens=True)

    print(prediction)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-m',
                        '--model',
                        type=str,
                        default="Intel/neural-chat-7b-v1-1",
                        help="models")
    parser.add_argument('-p',
                        '--prompt',
                        type=str,
                        default="Can you help me?",
                        help="prompt for the model")
    
    FLAGS = parser.parse_args()
    main(FLAGS)