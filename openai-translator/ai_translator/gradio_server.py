import os
import sys
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator


def translation(input_file):

    output_file_path = Translator.translate_pdf(input_file.name)
    LOG.info(f"output_file_path: {output_file_path}")

    return output_file_path

def launch_gradio():

    iface = gr.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gr.File(label="上传PDF文件")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")

def initialize_translator():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_type = args.model_type
    if model_type == "OpenAIModel":
        model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
        api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
        model = OpenAIModel(model=model_name, api_key=api_key)
    else:
        model_name = args.model_name if args.model_name else config['model_name']
        api_key = args.api_key if args.api_key else config['api_key']
        model = GLMModel(model=model_name, api_key=api_key)

    global Translator
    Translator = PDFTranslator(model)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
