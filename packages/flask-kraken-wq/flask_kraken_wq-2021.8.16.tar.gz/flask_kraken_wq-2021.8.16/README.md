####  flask simple sync work

#### example

```python
from flask_kraken_wq import  Queue,WorkTask

app = Flask(__name__)

from module import funname
from redis import Redis
@app.route('/')
def hello_world():
    Queue(Redis()).add(funname)
    return 'Hello World!'
### thread start work mode
WorkTask(connect=Redis(),flask_app=app).thread() 

### working start mode

WorkTask(connect=Redis(),flask_app=app).start() 

```