Little demo w/ grpc server that generates embeddings using huggingface. Then a rust client does some zero-shot sentiment analysis.
```
docker-compose up
```

### Next steps...
- add qdrant
- add import mechanisms
- add search functionality
- add a front end 
- add better import stuff








Usage: server.py [OPTIONS]

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --port          INTEGER  [default: 50052]                                                                                                              │
│ --device        TEXT     [default: cpu]                                                                                                                │
│ --help                   Show this message and exit.                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
