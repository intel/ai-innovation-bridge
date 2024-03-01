SHELL = /bin/bash # Use bash syntax
MODEL_NAME="meta-llama/Llama-2-7b-hf"
TEST_PROMPT = "Tell me something about the moon"
MAX_TOKENS = 100
BATCH_SIZE = 2

start-gaudi-docker:
	@docker run -itd --name model-card-gaudi-test --runtime=habana -e HABANA_VISIBLE_DEVICES=all -e OMPI_MCA_btl_vader_single_copy_mechanism=none --cap-add=sys_nice --net=host --ipc=host  vault.habana.ai/gaudi-docker/1.12.0/ubuntu20.04/habanalabs/pytorch-installer-2.0.1:latest
	@docker exec -it model-card-gaudi-test bash

clone-optimum-habana:
	@git clone https://github.com/huggingface/optimum-habana.git
	@cd optimum-habana/examples/text-generation/ && \
	pip3 install -q -r requirements.txt

install-dependencies:
	@pip3 install -q optimum-habana==1.10.0 && \
	pip3 install transformers

run-gaudi-eval:
	@echo "Starting run-gaudi-eval..."
	@start_time=$$(date +%s); \
	{ \
		{ time python run_generation.py --model_name_or_path $(MODEL_NAME) --use_hpu_graphs --use_kv_cache --max_new_tokens $(MAX_TOKENS) --do_sample --batch_size $(BATCH_SIZE) --prompt $(TEST_PROMPT) ; } 2>&1 ; \
		status=$$? ; \
		end_time=$$(date +%s) ; \
		duration=$$((end_time - start_time)) ; \
		echo "run-gaudi-eval completed in $$duration seconds." ; \
		echo "Duration: $$duration seconds" >> run-gaudi-eval.log ; \
		if [ $$status -ne 0 ]; then \
			echo "run-gaudi-eval failed. Check log for details." ; \
			echo "run-gaudi-eval failed" >> run-gaudi-eval.log ; \
		fi ; \
	} | tee run-gaudi-eval.log

run-all:
	@start_time=$$(date +%s)
	@echo "Starting run-all..."
	@make start-gaudi-docker
	@make clone-optimum-habana
	@make install-dependencies
	@make run-gaudi-eval
	@end_time=$$(date +%s)
	@duration=$$((end_time - start_time))
	@echo "run-all completed in $$duration seconds."
