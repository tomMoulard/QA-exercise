# QA reponses

## Exercice 1

L'image Docker (./Dockerfile) est utilisée pour créer le container, il suffit de le construire: 
```bash
docker build -t benchmark .
```

Puis, si on veut démarrer un contrôler:
```bash
docker run -e ARGS="--controller tcp://127.0.0.1:6000" benchmark
```

Et si on veut démarrer un agent:
```bash
docker run -e ARGS="--worker tcp://127.0.0.1:6000" benchmark
```

## Exercice 2



## Exercice 3



## Exercice 4



## Exercice 5

