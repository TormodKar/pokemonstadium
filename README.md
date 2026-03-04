Install runtime only: \
  ```uv sync``` \
Install runtime + dev: \
  ```uv sync --group test --group --lint```


For production: \
```docker build -f backend/Dockerfile --target prod -t pokemonstadium-api:prod backend```