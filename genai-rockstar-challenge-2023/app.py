from sd_amx import run_stable_diffusion
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder = 'output_images')

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image_url = None

    if request.method == 'POST':
        prompt = request.form['prompt']
        # Call your stable diffusion function here with the provided prompt
        # Replace the following line with your actual function call and image URL
        generated_image_url = run_stable_diffusion(prompt)

    return render_template('index.html', generated_image_url=generated_image_url)


if __name__ == '__main__':
    app.run(debug=True)
