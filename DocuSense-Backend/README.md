# DocuSense-Backend
This folder contains the Python backend for serving DocuSense. 

## Making .venv (recommended)
```shell
python -m venv ./.venv

# Linux / macOS: 
. ./.venv/bin/activate

# Windows
./.venv/Scripts/activate.bat
```

## Installing requirements
```shell
pip install -r requirements.txt
```

## Installing PyTorch
This wasn't included in requirements.txt because it depends on your system architecture. 

1. Visit [pytorch.org](https://pytorch.org/) and go under the "Install PyTorch" section.
2. Follow the directions and install. 

## HuggingFace
This is a hub for downloading open source machine learning models. 

To download Google Gemma / other models, you will need a HuggingFace account. 

1. Create a HuggingFace account
2. Accept the machine learning model's terms of use.
    - For example, to use [Gemma 2-billion params](https://huggingface.co/google/gemma-2-2b-it), you need to accept the 
      terms and conditions for the model. 
3. Make sure you run the requirements installation first above. 
4. Next, run `huggingface-cli login`. 
5. You can now run the code. 

## Running the backend
```shell
python app.py
```