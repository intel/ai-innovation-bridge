import argparse
from optimum.intel import IPEXModelForCausalLM
from transformers import AutoTokenizer, pipeline


def main(FLAGS):
  
    model = IPEXModelForCausalLM.from_pretrained(FLAGS.model)
    tokenizer = AutoTokenizer.from_pretrained(FLAGS.model)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    results = pipe(FLAGS.prompt)
    
    print(results)

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