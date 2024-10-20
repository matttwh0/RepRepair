from flask import Flask, request, jsonify
import os
from analyz import analyze_video
from gemini import gemini_analysis

app = Flask(__name__)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'video' not in request.files:
        return "No video file provided", 400

    video_file = request.files['video']
    file_path = os.path.join('uploads', video_file.filename)
    video_file.save(file_path)

    try:
        # Analyze the uploaded video using analyze_video from analyz.py
        #angles = analyze_video(file_path)
        angles = {"angle of left elbow": 45, "angle of right elbow": 180}
        # Execute the Gemini analysis with the resulting angles
        analysis_result = gemini_analysis(angles)

        # Respond with the analysis
        return jsonify({"analysis": analysis_result})
    except Exception as error:
        print(f'Error processing video: {error}')
        return "Error processing video and generating analysis.", 500
    finally:
        # Delete uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
