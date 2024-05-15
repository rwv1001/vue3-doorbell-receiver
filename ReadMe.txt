To create image:
docker build . -t doorbell-receiver

To run:
docker run -d -p 8080:80 -v /home/pi/vue3-doorbell-receiver/src/assets:/app/assets --name doorbell-receiver doorbell-receiver
docker update --restart unless-stopped doorbell-receiver

To run in debug:
Go to https://portainer.cambdoorbell.duckdns.org/ and make sure doorbell-receiver is not running.
Go to https://proxymanager.cambdoorbell.duckdns.org/ and change the scheme for cambdoorbell.duckdns.org to https.
Run 'npm run servecambdoorbell' 
