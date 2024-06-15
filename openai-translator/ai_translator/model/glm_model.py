from zhipuai import ZhipuAI

from model import Model

class GLMModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = ZhipuAI(api_key=api_key)

    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                translation = response.choices[0].message.content.strip()

                return translation, True
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "", False
