from flask import Flask, request, render_template

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__, template_folder='template')
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html', results=None, prediction_text=None)

    try:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        score = round(float(results[0]), 2)
        prediction_text = f"Predicted maths score: {score}"
        return render_template('home.html', results=score, prediction_text=prediction_text)

    except Exception as e:
        return render_template('home.html', results=None, prediction_text=f"Prediction failed: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


