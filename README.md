```markdown
# Battery Classification Web Application

A web-based application that uses computer vision and machine learning to classify battery types and brands via webcam capture. The application leverages WebRTC for real-time camera access and PyTorch for image classification.


## Features
- Real-time webcam access and video stream display
- Capture images for battery classification
- Multi-layer classification:
  - Layer 1: Distinguishes between rechargeable and non-rechargeable batteries
  - Layer 2: Identifies specific battery brands
  - Layer 3: Refines classification for final results
- Save captured images locally
- Responsive web interface


## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript, WebRTC
- **Backend**: Python, Flask
- **Machine Learning**: PyTorch, torchvision
- **Image Processing**: Pillow (PIL)


## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd battery-classification-app
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your pre-trained model files in the `model/` directory. Required model files:
   - `all-types-model.pth`
   - `non-recharge-model.pth`
   - `recharge-model.pth`
   - `model-1.pth`
   - `model-2.pth`


## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Select a video source from the dropdown menu (if multiple cameras are available)

4. Click "Capture and prediction" to capture an image and get classification results

5. View results in the three classification layers displayed on the page

6. Click "Save Image" to download the captured image locally


## Project Structure
- `app.py`: Backend Flask application with classification logic
- `templates/index1.html`: Main web interface
- `static/script.js`: Frontend JavaScript for camera handling and API calls
- `static/main.css`: Styling for the web interface
- `static/ga.js`: Google Analytics integration
- `model/`: Directory for storing pre-trained model files (not included in repository)


## Model Classification Details

### Layer 1 Classifications
- `non_rechargeable_battery`
- `rechargeable_battery`

### Layer 2 Classifications
- Non-rechargeable: `GP-aa`, `duracell-aa`, `energizer-aaa`, `gp-super-aa`, `gp-super-aaa`, `gp-supercell-aaa`, `matsusho-aa`, `matsusho-aaa`, `matsusho-super-aa`
- Rechargeable: `Energizer`, `GP-recyko-aaa`, `black-eneloop`, `toshiba`, `white-eneloop`

### Final Classifications
- Group 1: `Energizer`, `GP-recyko-aaa`, `energizer-aaa`, `gp-super-aa`
- Group 2: `black-eneloop`, `duracell-aa`, `matsusho-super-aa`

