Run:

poetry run python main.py


Build & Deploy:

docker build -t elsdoerfer/tbtc-torch:latest .
docker push elsdoerfer/tbtc-torch:latest
kubectl delete pod -l app=tbtc-torch