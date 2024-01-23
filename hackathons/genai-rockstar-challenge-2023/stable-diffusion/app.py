from sd_amx import run_stable_diffusion
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder = 'output_images')

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image_url = 'https://www.intel.com/content/dam/www/central-libraries/us/en/images/xeon-scalable-processors-family-framed-badge.jpg.rendition.intel.web.480.270.jpg'
    inference_time = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        # Call your stable diffusion function here with the provided prompt
        # Replace the following line with your actual function call and image URL
        
        # Acquire the generated image URL and inference time
        generated_image_url, inference_time = run_stable_diffusion(prompt)
        # Print the inference time
        
        # Reduce inference_time to two decimal places
        inference_time = round(inference_time, 2)
        print(f'inference_time = {inference_time}')
        
        
    return render_template('index.html', generated_image_url=generated_image_url, inference_time=inference_time)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
