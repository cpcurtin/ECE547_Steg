from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World This is Water Marking Backend"}


# PSNR is an integrated function in tensorflow. https://www.tensorflow.org/api_docs/python/tf/image/psnr
# MSE is integrated in both numpy and scikit-learn. https://www.geeksforgeeks.org/python-mean-squared-error/#
# Assuming there are no issues importing these modules with our website, we should just use them because they are already defined. Tensorflow specifically 
#   demos using PSNR on image files in the documentation linked above. 
# There are also functions for jpeg rescaling and other image manipulation. https://www.tensorflow.org/api_docs/python/tf/image