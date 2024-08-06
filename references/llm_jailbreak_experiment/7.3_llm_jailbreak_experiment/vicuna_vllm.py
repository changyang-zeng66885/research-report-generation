import common
from vllm import LLM, SamplingParams

VICUNA_PATH = "你的huggingface模型路径"

class VicunaVLLM():

    def __init__(self, model_name="vicuna", loaded_model=None, loaded_tokenizer=None):
        self.model_name = model_name
        if loaded_model:
            self.model = loaded_model
        else:
            self.model = LLM(model=VICUNA_PATH, tensor_parallel_size=2)
        self.tokenizer = None

    def batched_generate(self,
                         full_prompts_list,
                         max_n_tokens: int,
                         temperature: float,
                         top_p: float):
        sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=max_n_tokens)
        outputs = self.model.generate(full_prompts_list, sampling_params)
        return [output.outputs[0].text for output in outputs]

    def generate(self,
                 full_prompt,
                 max_n_tokens: int,
                 temperature: float,
                 top_p: float):
        outputs_list = self.batched_generate([full_prompt], max_n_tokens, temperature, top_p)
        return outputs_list[0]


    def preprocess_input(self, prompt_list, system_prompt=None):
        input_list = []
        for prompt in prompt_list:
            conv = common.conv_template("vicuna_v1.1")
            if system_prompt:
                conv.set_system_message(system_prompt)
            conv.append_message(conv.roles[0], prompt)
            conv.append_message(conv.roles[1], None)
            input_list.append(conv.get_prompt())
        return input_list


if __name__ == '__main__':
    llm = VicunaVLLM()
    input_list = VicunaVLLM.preprocess_input(["Write a story about making a cake."], "")
    print(input_list)
    print(llm.batched_generate(input_list, 512, 0, 0.95))

