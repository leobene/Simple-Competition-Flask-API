# Simple-Competition-Flask-API
A simple **REST** API to create and record competitions using Flask

## API 

From the API we can:

1. Create a competition
2. Add results to a competition (all fields are mandatory), 
  
  ex: 
  ```json
  {
    "competicao": "100m classificatoria 1", 
    "atleta": "Joao das Neves", 
    "value": "10.234", 
    "unidade": "s"
  }
  ```
  ex: 
  ```json
  {
    "competicao": "Dardo semifinal", 
    "atleta": "Claudio", 
    "value": "70.43", 
    "unidade": "m"
  }
  ```
3. Finish a competition.
4. Return the competition, showing the final position of each athlete.


### **Rules**:
1. The API should not accept results records if the competition is already finished.
2. The API may return the ranking / partial result if the dispute is not yet finished.
3. In the darts throw competition, each athlete will have 3 chances, and the result of
competition shall take into account the furthest throwing of each athlete.


### ToDO:
1 - Tests
2 - API Readme
