# thumbor_dash
A thumbor server extension for DASH


## Setup

#### Requirements

- Python >= 3.9
- Pip >= 21.1
- Thumbor == 7.0.0a5

See the requirements for setting up `thumbor` in the [documentation](https://thumbor.readthedocs.io/en/latest/installing.html)

#### 1. Install thumbor_dash

`pip install thumbor_dash`

Note: thumbor_dash, thumbor, and other required dependencies will be installed

#### 2. Create a thumbor configuration file
  
`thumbor-config > thumbor.conf`

#### 3. Add these lines to `thumbor.conf` file

```python
# Set allowed dimensions
MIN_WIDTH = 1
MIN_HEIGHT = 1
MAX_WIDTH = 1200
MAX_HEIGHT = 800

# Set security key
SECURITY_KEY = "0"

# Url signing method
URL_SIGNER = 'thumbor_dash.url_signers.base64_hmac_sha256'

# Use only signed URL
ALLOW_UNSAFE_URL = False

# Set user moderation rules
REQUEST_TIME_LIMIT = 1 # time between requests in minutes
USAGE_VIOLATION_LIMIT = 5 # total number of times a requester can violate the time limit before ban
BAN_DURATION = 10 # requester ban duration in minutes
```

## Usage

#### 1. Start thumbor_dash server

   `thumbor_dash --conf=thumbor.conf`

#### 2. Sign image URL

   ```python

   thumbor_dash-url --key="<SECURITY_KEY>" --width=<width> --height=<height> --dashauth="requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<avatarUrl>):owner(<ownerId>):updatedAt(<updatedAt>)" --filters="<filters>" <imageURL>

   ```

`output:`

   ```python

   /<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<field>):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>

   ```

#### 3. Thumbor_dash image retrieval URL

   ```python
   http://<thumbor_dash-server>/<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<field>):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>
   
   ```

   Note: If running the server locally, `<thumbor_dash-server>` should be `localhost:8888`


## Example

 This is a signed `thumbor_dash url`. Simply run `thumbor_dash` and paste this link in your browser.

   ```python

   http://localhost:8888/MXd8uDwHf1xqp6YG0RzlkrmtdBaq1ZyzznPLJft1rl4=/1200x800/dashauth:requester(26AxVi5bvYYaC94GmeTmqX21vzsSxar2a4imxSE8ULUQ):contract(D6tjxCZzZobDQztc4S1PK7EDwm4CegLARpiKZn6jQc1R):document(thumbnailField):field(avatarUrl):owner(26AxVi5bvYYaC94GmeTmqX21vzsSxar2a4imxSE8ULUQ):updatedAt(1627948894242)/filters:format(jpeg)/https%3A//github.com/thumbor/thumbor/raw/master/example.jpg


   
   ```




