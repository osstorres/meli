
<br />
<div align="center">
  <a href="images/mercado-libre-log.jpg">
    <img src="images/mercado-libre-log.jpg" alt="Logo" width="320" height="250">
  </a>

  <h3 align="center">Mercado Libre Challenge - Osiel Torres</h3>

</div>



## About The Project

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


### Built With

<p>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="100" height="100" />&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="100" height="100" />&nbsp;
</p>





<!-- GETTING STARTED -->
## ⚡️ Development environment explain

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



## 🔨 Getting Started

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



# 📖 Motivation to create


WIP


# 🧪 First ideas

![arch](images/arch1.png)


# 🧪 Shaping

![arch2](images/arch2.png)


# 


