from PIL import Image
import io
import base64
import torch
import torchvision.transforms as transforms
from flask import Flask, jsonify, render_template, Response, request

app = Flask(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = torch.load('model/all-types-model.pth', map_location=device)
model.to(device)
model.eval()

model0 = torch.load('model/non-recharge-model.pth', map_location=device)
model.to(device)
model.eval()

model1 = torch.load('model/recharge-model.pth', map_location=device)
model.to(device)
model.eval()

model31 = torch.load('model/model-1.pth', map_location=device)
model.to(device)
model.eval()

model32 = torch.load('model/model-2.pth', map_location=device)
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# layer 1
class_labels = ['non_rechargeable_battery', 'rechargeable_battery']

# layer 2
non_recharge_class_labels = ['GP-aa', 'duracell-aa', 'energizer-aaa', 'gp-super-aa', 'gp-super-aaa', 
                             'gp-supercell-aaa', 'matsusho-aa', 'matsusho-aaa', 'matsusho-super-aa']
recharge_class_labels = ['Energizer', 'GP-recyko-aaa', 'black-eneloop', 'toshiba', 'white-eneloop']

# layer 3
model_1_class_labels = ['Energizer', 'GP-recyko-aaa', 'energizer-aaa', 'gp-super-aa']
model_2_class_labels = ['black-eneloop', 'duracell-aa', 'matsusho-super-aa']

# final result
final_1_labels = ['Energizer', 'GP-recyko-aaa', 'energizer-aaa', 'gp-super-aa']
final_2_labels = ['black-eneloop', 'duracell-aa', 'matsusho-super-aa']

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predictions', methods=['POST'])        
def get_predictions():

    data = request.get_json()
    image = data['image']
    image = image.split(',')[1].encode('utf-8')
    image = base64.b64decode(image)
    image = Image.open(io.BytesIO(image))
    # image = Image.open(io.BytesIO(base64.b64decode(image)))
    input = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input)

    class_index1 = torch.argmax(output).item()
    class1 = class_labels[class_index1]
    probabilities = torch.nn.functional.softmax(output, dim=1)
    probability1 = probabilities[0][class_index1].item()

    # layer 2
    if class_index1 == 0:
        with torch.no_grad():
            output = model0(input)

        class_index2 = torch.argmax(output).item()
        class2 = non_recharge_class_labels[class_index2]
        probabilities = torch.nn.functional.softmax(output, dim=1)
        probability2 = probabilities[0][class_index2].item()

        # layer 3
        if class2 in model_1_class_labels:
            with torch.no_grad():
                output = model31(input)

            class_index3 = torch.argmax(output).item()
            class3 = final_1_labels[class_index3]
            probabilities = torch.nn.functional.softmax(output, dim=1)
            probability3 = probabilities[0][class_index3].item()

        elif class2 in model_2_class_labels:
            with torch.no_grad():
                output = model32(input)

            class_index3 = torch.argmax(output).item()
            class3 = final_2_labels[class_index3]
            probabilities = torch.nn.functional.softmax(output, dim=1)
            probability3 = probabilities[0][class_index3].item()

        else:
           class3 = "None"
           probability3 = "None"

    # layer 2
    else:
        with torch.no_grad():
            output = model1(input)

        class_index2 = torch.argmax(output).item()
        class2 = recharge_class_labels[class_index2]
        probabilities = torch.nn.functional.softmax(output, dim=1)
        probability2 = probabilities[0][class_index2].item()

        # layer 3
        if class2 in model_2_class_labels:
            with torch.no_grad():
                output = model32(input)

            class_index3 = torch.argmax(output).item()
            class3 = final_2_labels[class_index3]
            probabilities = torch.nn.functional.softmax(output, dim=1)
            probability3 = probabilities[0][class_index3].item()

        elif class2 in model_1_class_labels:
            with torch.no_grad():
                output = model31(input)

            class_index3 = torch.argmax(output).item()
            class3 = final_1_labels[class_index3]
            probabilities = torch.nn.functional.softmax(output, dim=1)
            probability3 = probabilities[0][class_index3].item()

        else:
            class3 = "None"
            probability3 = "None"

    if class3 in non_recharge_class_labels:
        finalclass = 'non rechargeable battery'

    elif class3 in recharge_class_labels:
        finalclass = 'rechargeable battery'

    else:
        finalclass = 'None'

    return jsonify({'class1': class1, 
                    'probability1': probability1, 
                    'class2': class2, 
                    'probability2': probability2,
                    'finalclass': finalclass, 
                    'finalbrand': class3,
                    'probability3': probability3})

if __name__ == '__main__':
    app.run(debug=True)