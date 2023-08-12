Little demo w/ grpc server that generates embeddings using huggingface. Then a rust client does some zero-shot sentiment analysis.
```
docker-compose up
```

### Next steps...
- [ ] add qdrant
- [ ] add import mechanisms
- [ ] add search functionality
- [ ] add a front end 
- [ ] currently port num in rust is magic num... yeah I should fix that... not really too excited to do that until rest of cli
- [ ] add better import stuff
- [ ] support images

### Server.py usage

```
Usage: server.py [OPTIONS]

 Options
  --port          INTEGER  [default: 50052]
  --device        TEXT     [default: cpu]
  --help                   Show this message and exit.
```
