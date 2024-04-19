To create image:
docker build . -t doorbell-receiver

To run:
docker run -d -p 8080:80 -v /home/pi/vue3-doorbell-receiver/src/assets:/app/assets --name doorbell-receiver doorbell-receiver
docker update --restart unless-stopped doorbell-receiver
