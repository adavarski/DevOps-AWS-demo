Jenkinsfile-s3-web pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/Jenkinsfile-s3-web

Build with Parameters: CREATE, UPLOAD

Check J.Pipeline Outputs:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/J-console-output/consoleText-S3-static-web-site-CREATE

https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/J-console-output/consoleText-S3-static-web-site-UPLOAD

Check S3 static website:

```
curl https://s3-static-website-demo.s3.us-east-2.amazonaws.com/index.html
 <!doctype html>
    <html>
      <head>
        <title>Static HTML Site</title>
      </head>
      <body>
        <p>This is the first paragraph in a simple Static HTML site we developed. There is no <strong>CSS</strong> or <strong>JavaScript</strong>.</p>

        <h6>Thanks for visiting our static page</h6>
    
      </body>
    </html>
```
