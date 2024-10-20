from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
# from analyz import analyze_video
from gemini import gemini_analysis
from analyz import process_video

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200
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
        #TODO: when all said and done switch the 2  commands below comment first and release second
        #angles = process_video(file_path)
        angles = {"angle of left elbow": 45, "angle of right elbow": 180}

        #TODO: test code
        rep_data, processed_video_path = process_video(angles)
        print(f"Video processed successfully: {processed_video_path}")

        
        # Execute the Gemini analysis with the resulting angles
        analysis_result = gemini_analysis(rep_data)

        # Respond with the analysis

        return jsonify({"analysis": analysis_result})
        #test code below
        # return jsonify({
        #     "analysis": analysis_result,
        #     "set_data": rep_data,
        #     "processed_video_path": os.path.basename(processed_video_path)  # Only send the filename
        # })
    
    except Exception as error:
        print(f'Error processing video: {error}')
        return "Error processing video and generating analysis.", 500
    finally:
        # Delete uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
