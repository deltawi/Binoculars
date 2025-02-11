__all__ = ["app"]

import gradio as gr
from binoculars import Binoculars

BINO = Binoculars()
TOKENIZER = BINO.tokenizer
MINIMUM_TOKENS = 64


def count_tokens(text):
    return len(TOKENIZER(text).input_ids)


def run_detector(input_str):
    if count_tokens(input_str) < MINIMUM_TOKENS:
        gr.Warning(f"Too short length. Need minimum {MINIMUM_TOKENS} tokens to run Binoculars.")
        return ""
    return f"{BINO.predict(input_str)}"


# def load_set(progress=gr.Progress()):
#     tokens = [None] * 24
#     for count in progress.tqdm(tokens, desc="Counting Tokens..."):
#         time.sleep(0.01)
#     return ["Loaded"] * 2


css = """
.green { color: black!important;line-height:1.9em; padding: 0.2em 0.2em; background: #ccffcc; border-radius:0.5rem;}
.red { color: black!important;line-height:1.9em; padding: 0.2em 0.2em; background: #ffad99; border-radius:0.5rem;}
.hyperlinks {
  display: flex;
  align-items: center;
  align-content: center;
  padding-top: 12px;
  justify-content: flex-end;
  margin: 0 10px; /* Adjust the margin as needed */
  text-decoration: none;
  color: #000; /* Set the desired text color */
}
"""

capybara_problem = '''Dr. Capy Cosmos, a capybara unlike any other, astounded the scientific community with his groundbreaking research in astrophysics. With his keen sense of observation and unparalleled ability to interpret cosmic data, he uncovered new insights into the mysteries of black holes and the origins of the universe. As he peered through telescopes with his large, round eyes, fellow researchers often remarked that it seemed as if the stars themselves whispered their secrets directly to him. Dr. Cosmos not only became a beacon of inspiration to aspiring scientists but also proved that intellect and innovation can be found in the most unexpected of creatures.'''

with gr.Blocks(css=css,
               theme=gr.themes.Default(font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"])) as app:
    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("<p><h1> binoculars: zero-shot llm-text detector</h1>")
        with gr.Column(scale=1):
            gr.HTML("""
            <p>
            <a href="https://arxiv.org/abs/2401.12070" target="_blank">paper</a>
                
            <a href="https://github.com/AHans30/Binoculars" target="_blank">code</a>
                
            <a href="mailto:ahans1@umd.edu" target="_blank">contact</a>
            """, elem_classes="hyperlinks")
    with gr.Row():
        input_box = gr.Textbox(value=capybara_problem, placeholder="Enter text here", lines=8, label="Input Text", )
    with gr.Row():
        clear_button = gr.ClearButton()
        submit_button = gr.Button("Run Binoculars", variant="primary")
    with gr.Row():
        output_text = gr.Textbox(label="Prediction", value="AI-Generated")

    with gr.Row():
        gr.HTML("<p><p><p>")
    with gr.Row():
        gr.HTML("<p><p><p>")
    with gr.Row():
        gr.HTML("<p><p><p>")

    with gr.Accordion("Disclaimer", open=False):
        gr.Markdown(
            """
            - `Accuracy` :
                - AI-generated text detectors aim for accuracy, but achieving 100% is challenging.
                - The provided prediction is for demo purposes only and should not be considered a consumer product.
                - Users are advised to exercise discretion, and we assume no liability for any use.
            - `Detection Use Cases` : 
                - In this work, our focus is to achieve an ultra-low false positive rate, crucial for sensitive downstream use case (e.g., avoiding false accusations in academic honesty cases). 
                - We find optimal application in content moderation, for example in detecting AI-generated reviews on platforms like Amazon, Google, Yelp, etc. This represents one of the most compelling and noteworthy use cases for Binoculars.
            - `Human Supervision Advisory` :
                - Strongly caution against using Binoculars (or any detector) without human supervision.
            - `Performance by Language` :
                - As noted in our paper, Binoculars exhibit superior detection performance in the English language compared to other languages.
            """
        )

    with gr.Accordion("Cite our work", open=False):
        gr.Markdown(
            """
            ```bibtex
                @misc{hans2024spotting,
                      title={Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text}, 
                      author={Abhimanyu Hans and Avi Schwarzschild and Valeriia Cherepanova and Hamid Kazemi and Aniruddha Saha and Micah Goldblum and Jonas Geiping and Tom Goldstein},
                      year={2024},
                      eprint={2401.12070},
                      archivePrefix={arXiv},
                      primaryClass={cs.CL}
                }
            """
        )

    # confidence_bar = gr.Label(value={"Confidence": 0})

    # clear_button.click(lambda x: input_box., )
    submit_button.click(run_detector, inputs=input_box, outputs=output_text)
    clear_button.click(lambda: ("", ""), outputs=[input_box, output_text])
