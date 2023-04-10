# XML Paser Service Lambda Version

Notes: This is not included in the CI/CD pipeline, however it can be incoperated later.

Ensure the following application are installed before deployment;

* [aws cli](https://aws.amazon.com/cli/)
* [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

To deploy you have to modify the following to suit your aws service.

* dev.env
    * PROFILE ==> `dev` is my default. Change it to your profile name.

    * BUCKET ==> `gh-dev-sam-deployment` is my default, change it to your deployment bucket.

## Deploy

To deploy run the following sequence in terminal

* `./script/build_layers.sh`
* `./deploy.sh`
