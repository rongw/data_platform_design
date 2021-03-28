This is a very simple and small framework to ensure quick Lambda deployment/update. 

Pre-Request
Create a AWS cli profile with your own AWS access Key and ID e.g. project-a-aws-profile

Steps
1. Create a new directory e.g. myFunction
2. Create a 'code' folder under myFunction directory
3. Put your source code and dependency libraries under myFuncton/code
4. Create a lambda.config file under myFunction director
5. Filling in the config parameter follow on of the exisitng function

Suggestion
Name your aws profile as other Lambda functions, this is to ensure aws profile name stays the same, however the KeyId and Key belongs to each individual developer