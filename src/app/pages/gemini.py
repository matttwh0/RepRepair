import google.generativeai as genai
from dotenv import load_dotenv
import os

# takes in information

async def gemini_analysis(set_data):
    load_dotenv()
    # secret_value = os.getenv("GOOGLE_API_KEY")
    GOOGLE_API_KEY=''
    genai.configure(api_key=GOOGLE_API_KEY)
    # set_data = {"angle of elbow": 180, "poop": "say butt"}
    model = genai.GenerativeModel('gemini-1.5-pro')

    response = model.generate_content(["""
                                    You are a gym assistant giving advice to individuals who are new to the gym. You observe their workouts and can precisely determine their progress. Currently, you will be observing lateral raises.

                                    You will be given a series of text where it'll be labeled as a "Correct Rep" or an "Incorrect Rep", followed by the lowest angle that comes with each elbow. To give feedback to the user, you will use these data points in order to determine what they need to fix. For example, on an incorrect rep, if a user's left elbow angles out heavily more than the other elbow, that means that there is some type of muscle imbalance between their left and right, which is something that you should call out.

                                    For the formatting of your response, I want you to give a brief 3-5 sentence summary of what they did right and what they did wrong, as well as 3 bullet points of what they can improve on in the future. If they had some correct reps, tell them that they reached good depth on some of them. I also want you to point out which rep they did wrong as well. In that rep, you can tell them about not being able to reach enough elbow angle depth. 

                                    Some tips you can give them is going deeper, being more consistent toward the end of their set, etc. 
                                                                        
                                    Set data: {set_data}.
                                     """], stream=True)
  
    response.resolve()
    return response
