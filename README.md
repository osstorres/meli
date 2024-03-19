
<br />
<div align="center">
  <a href="images/mercado-libre-log.jpg">
    <img src="images/mercado-libre-log.jpg" alt="Logo" width="320" height="250">
  </a>

  <h3 align="center">Mercado Libre Challenge - Osiel Torres</h3>

</div>



# 🚧 About The Project

Mercadolibre hoy en día correr sus aplicaciones en más de 20000 servidores, estos suelen comunicarse entre sí a través de apis, algunas accesibles desde el exterior (api.mercadolibre.com).
Uno de los problemas que tenemos actualmente es como controlar y medir estas interconexiones. Para esto necesitamos crear e implementar un "proxy de apis" (codear).
Este proxy debe poder cumplir al menos con los siguientes requisitos (en orden de importancia):

● Permitir ejecutar la función de proxy, sobre el dominio api.mercadolibre.com, es decir que al ejecutar un llamado al proxy este debera retornar el llamado a api.mercadolibre.com
Ejemplo "curl 127.0.0.1:8080/categories/MLA97994" debera retornar el contenido de https://api.mercadolibre.com/categories/MLA97994

● Se deberá poder controlar la cantidad máxima de llamados por

    ○ ip de origen
    ○ path de destino
    ○ Combinaciones de ambos
    ○ Otros criterios u alternativas de control son bien vistas ;)
● Estadísticas de uso: se deben almacenar (y en lo posible visualizar) estadísticas de uso del proxy

● El proxy debe correr sobre Linux

● El código debe estar en un repo git para poder pegarle un vistazo y discutir

● La carga media del proxy (como solución) debe poder superar los 50000 request/segundo. Por lo cual como escala la solución es muy importante

Algunos deseables:
- La interfaz para estadísticas y control podría soportar rest
- Tener todos los puntos completos (y funcionando), aunque cualquier nivel de completitud es aceptable
- Tener algún dibujo, diagrama u otros sobre como es el diseño, funcionamiento y escalabilidad del sistema suma mucho
- Funcionar contra el api de mercadolibre real, estaría buenísimo, de todas formas son conocidos algunos errores con HTTP’s, por lo que cualquier otra alternativa (mocks, otra api, etc) que pruebe el funcionamiento también es válido

---
## ⚠️ Suggestion: Read first "Motivation to create" Section
### Built With

<p>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="100" height="100" />&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="100" height="100" />&nbsp;
</p>

---


<!-- GETTING STARTED -->
# ⚡️ Development environment explain

Containers in order docker-compose.yaml file:

### Services Overview:

#### 1. **dynamodb-local**:
   - **Description**: This service provides a local instance of DynamoDB for testing purposes.
   - **Usage**: Utilize this service to interact with a local instance of DynamoDB during development and testing.
   - **Ports**: Exposes port 8000 for accessing the local DynamoDB instance.

#### 2. **redis**:
   - **Description**: Redis service used as a message broker and cache.
   - **Usage**: Provides caching and message broker functionalities for various services.
   - **Ports**: Exposes port 6380 for connecting to Redis.

#### 3. **django**:
   - **Description**: Django container serving as the main application for proxy sync service.
   - **Usage**: Runs the Django application handling proxy synchronization tasks.
   - **Dependencies**: Depends on `dynamodb-local`, `localstack`, and `redis`.
   - **Ports**: Exposes port 8123 for accessing the Django application.

#### 4. **celery**:
   - **Description**: Celery container responsible for executing asynchronous tasks.
   - **Usage**: Executes background tasks asynchronously using Celery.
   - **Dependencies**: Depends on `redis`.
   
#### 5. **flower**:
   - **Description**: Container providing a web-based tool for monitoring and debugging Celery tasks.
   - **Usage**: Monitor and debug Celery tasks visually through Flower's web interface.
   - **Dependencies**: Depends on `redis` and `celery`.
   - **Ports**: Exposes port 5555 for accessing the Flower web interface.

#### 6. **localstack**:
   - **Description**: LocalStack service simulating various AWS resources.
   - **Usage**: Mimics AWS services locally for development and testing purposes.
   - **Supported Services**: SQS, IAM, S3, Lambda, and lambda subs
   - **Ports**: Exposes port 4566 for accessing LocalStack services.

#### 7. **init-service**:
   - **Description**: Service for initializing resources in LocalStack.
   - **Usage**: Initializes resources such as Lambda functions, SQS queues, and DynamoDB tables in LocalStack.
   - **Dependencies**: Depends on `localstack`.

#### 8. **fastapi**:
   - **Description**: FastAPI container providing a RESTful API to retrieve metadata stats.
   - **Usage**: Access metadata statistics through the FastAPI RESTful API.
   - **Dependencies**: Depends on `dynamodb-local`.
   - **Ports**: Exposes port 9000 for accessing the FastAPI endpoints.

#### 9. **dynamodb-admin**:
   - **Description**: Container for visualizing DynamoDB tables through a web-based UI.
   - **Usage**: View and interact with DynamoDB tables through the admin UI.
   - **Dependencies**: Depends on `dynamodb-local`.
   - **Ports**: Exposes port 8001 for accessing the DynamoDB Admin UI.

#### 10. **master**:
   - **Description**: Master service for Locust used for load testing.
   - **Usage**: Orchestrates and controls Locust load testing scenarios.
   - **Ports**: Exposes port 8089 for accessing the Locust master.

#### 11. **worker**:
   - **Description**: Worker service for Locust used for load testing.
   - **Usage**: Executes load testing scenarios defined by the master Locust service.
   - **Dependencies**: Depends on the master Locust service.


----

#  🔨 Getting Started

Start the project


  ```sh
  docker-compose up --build
  ```

It's important to wait for the init-service to complete in order to have the following:

- SQS Queue created
- Lambda consumer created
- Lambda consumer subscribed to the SQS queue
- DynamoDB table created
- You will receive the message: All resources initialized! 🚀

To run tests once you have the services started, you can execute the following command

  ```sh
  docker-compose exec -e DJANGO_CONFIGURATION=Testing django pipenv run pytest
  ```

# 🥷🏽 Usage Development environment

Once you have the services up and running, the use of the proxy is as follows:


Proxy URL : http://localhost:8123/
Path category: categories/MLA5726 


  ```sh
❯ curl http://localhost:8123/categories/MLA5726
 ```
<img src="images/proxy_test1.png" alt="proxy_test1" width="500" height="300">

If you request this URL again, it will be responded through the Redis cache.

To visualize metadata statistics of requests (application level).

  ```sh
❯ curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
-H "Content-Type: application/json" \
-d '{"resource": "/stats", "path": "/stats", "httpMethod": "GET", "requestContext": {}, "multiValueQueryStringParameters": null}'
 ```

To visualize asynchronous tasks. http://localhost:5555/tasks

<img src="images/flower.png" alt="flower" width="900" height="300">


To visualize metadata dynamodb http://localhost:8001

<img src="images/admindb.png" alt="db" width="900" height="500">

# 💣 Load Testing

For load testing, we will use Locust, which will allow us to simulate requests 
and a number of concurrent users in our application. To do this, we must go to...

http://localhost:8089


https://github.com/osstorres/meli/assets/36452775/cc47b317-204b-472f-b22e-ecc2caf1f3c9


---
# 📖 Motivation to create

#### * Decision making: https://aws.amazon.com/es/architecture/well-architected/

Why did I choose this architecture?

We can summarize some important requirements to start designing the architecture:

- Generate an "API proxy" (proxy.com/categories/ ---> mercadolibre.com/categories/)
- Blocking IPs and paths to the proxy
- Visualize proxy usage statistics, if possible, expose a REST API
- Run on Linux
- Support scalability of 50k requests per second 

First, we must consider that we will have a large number of requests to our proxy that we must support at the server level. It is not mentioned if there will be times of the day with more traffic, so we can start thinking about vertical and horizontal auto-scaling of our services. Additionally, an important requirement is to be able to block IPs and paths to our services. Based on this, we can take one of two paths: consider blocking at the application (code) level, which would create a significant bottleneck, or do it properly with a WAF. Additionally, we can consider geographical blocking (CloudFront) or latency, proximity, countries, etc.

With these ideas in mind, the "simple" path with a basic architecture could be an EC2 instance with an auto-scaling group that increases instances as traffic increases. Initially, this may yield results, but we may fall short when scaling more services or considering decoupling components for further data processing. Due to this, I chose Kubernetes to self-manage some containers needed in the proxy. With Kubernetes, we can cover auto-scaling, redundancy, and operational excellence.

We need to consume an external API (mercadolibre.com), it's important to handle exceptions that are beyond our control and return appropriate status codes. It's crucial to note that considering our example request (https://api.mercadolibre.com/categories/MLA97994), we can identify that we will likely have repeated requests over time from different users. In this use case, we can implement a cache to avoid re-requesting information from Mercado Libre. This way, we can provide much faster responses to our users, reduce third-party API failures, and scale the cache cluster for reading instead of our servers in a Kubernetes cluster, which would be more costly.

At this point, we have covered the following:

- Horizontal and vertical scalability
- Reliability
- Efficiency


For the proxy infrastructure, a crucial aspect highlighted by the Well-Architected Framework is security. Based on this, we will cover the part of blocking IPs and paths to the proxy. AWS WAF helps us have complex denial rules for a group of IPs, with IP sets, path blocking, and a combination of these towards the resources we expose, in this case, our EKS service.

Once our proxy service is ready, we move on to the requirement of usage statistics. For this requirement, I took two approaches: one regarding resource usage metrics (CPU, memory, latency, execution time, cluster health, etc.) and another regarding application metadata. Infrastructure usage metrics can be covered using CloudWatch, which integrates well with our services, and an external tool like New Relic or Prometheus-Grafana for our EKS cluster. For application metadata metrics, I decided to create an event-driven architecture to manage the information to process, as described in the architecture diagram. Basically, our synchronous proxy responds as quickly as possible to the user, and we use Celery to handle asynchronous tasks that process metadata from user requests, such as the IP source and requested path. This metadata is formatted and sent to an SQS queue that keeps the messages available for a subscribed Lambda function to use this information and integrate it into DynamoDB for consumption through a REST API.

Certainly, the question arises as to why we don't directly send the metadata to DynamoDB from Celery. I made this architecture decision for three reasons:

- Reduce resource consumption in the deployment of Celery so that it only sends metadata to a queue and does not process it in DynamoDB.
- Cost reduction when inserting into DynamoDB; instead of inserting item by item, the Lambda function can process batches of messages and send them to DynamoDB with lower latency at a VPC endpoint directly in its own network.
- Having an event-driven architecture based on an SQS queue allows us more possibilities for operations with this information. For example, subscribing another Lambda function to send notifications in case of an unrecognized error state by our knowledge base in the external APIs indicating an uncontrolled failure. Since these are metadata statistics, they don't need to be available at that moment for reading. This processing to DynamoDB can take its time. Important for the production and development environment: Currently, in this solution, messages are read one by one. Ideally, messages should be processed in batches, for example, 10k messages in each reading from the SQS queue in batch.


Once we have the application metadata available in DynamoDB, we will use a serverless architecture to serve a REST API based on FastAPI that exposes our DynamoDB data through an API Gateway. This is a simple but functional architecture for our current use case.

---

# 🧪 First ideas

![arch](images/arch1.png)


# 🧪 Shaping

![arch2](images/arch2.png)

---

# 🏗️ Architecture️  

![arch2](images/arch3.jpeg)



