Homeschool bundle with learner hub vehicles update

Contents:
- homeschool-web-starter/   web app starter
- skill.zip                 ChatGPT skill bundle
- baseline_api_check.py     API checker script
- run_app.sh                app launcher

This version adds:
- preferred learning vehicles as the first card on the learner hub
- blank preferred vehicles for new learners
- editable learner vehicles with dropdown plus custom entries
- language page showing the learner's current vehicles

Suggested use in WSL:
1. Rename your current Homeschool folder if needed.
2. Unzip this archive so it creates a new Homeschool folder.
3. Create a venv in the Homeschool folder if you do not already have one:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r homeschool-web-starter/backend/requirements.txt
4. Run the app:
   ./run_app.sh
5. Open:
   http://127.0.0.1:8000
   http://127.0.0.1:8000/docs
