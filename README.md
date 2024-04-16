# aws-cdk-paramo 

By: Julian Alvarez Villamil.

Version: 0.1.0

AWS-CDK

## Prerequisites

- [AWS Account](https://aws.amazon.com/)
- [Anaconda](https://www.anaconda.com/download/) >=4.x
- Optional [Mamba](https://mamba.readthedocs.io/en/latest/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

## AWS CLI

Please check your AWS CLI version:
    
```bash
aws --version
```
 ## Create AWS IAM user

1. Go to the AWS Management Console and open the IAM console at [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

2. In the navigation pane, choose Users.

3. Choose Add user.

4. For User name, type a name for the user.

5. Choose the type of access this set of users will have. For this example, select Programmatic access.

6. Choose Next: Permissions.

7. Choose Attach existing policies directly.

8. In the search box, type AdministratorAccess.

9. Select the AdministratorAccess policy.

10. Choose Next: Tags.

11. Choose Next: Review.

12. Choose Create user.

13. To view the access key pair, choose Show. You will not have access to the secret access key again after this dialog box closes. Your secrets are stored securely and cannot be retrieved later.

14. Open your terminal and configure the AWS CLI with the access key and secret key.

    ```bash
    aws configure
    ```

15. Enter the access key and secret key, you see something like this:

    ```bash
    AWS Access Key ID [None]: <your_access_key_id>
    AWS Secret Access Key [None]: <your_secret_access_key>
    Default region name [None]: <your_region>
    Default output format [None]: json
    ```
16. Verify the configuration:

     ```bash
    aws configure list
    ```
Nice job! You have created an IAM user and configured the AWS CLI.

## Create environment

remember install [conda](https://www.anaconda.com/download/) or [mamba](https://mamba.readthedocs.io/en/latest/) and create the environment:

```bash
conda env create -f environment.yml
activate aws_cdk_paramo
```

or 

```bash
mamba env create -f environment.yml
activate aws_cdk_paramo
```

## Project organization

    aws_cdk_paramo
        ├── data
        │   ├── processed      <- The final, canonical data sets for modeling.
        │   └── raw            <- The original, immutable data dump.
        │
        ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
        │                         the creator's initials, and a short `-` delimited description, e.g.
        │                         `julian-alvarez-v`.
        │
        ├── .gitignore         <- Files to ignore by `git`.
        │
        ├── environment.yml    <- The requirements file for reproducing the analysis environment.
        │
        └── README.md          <- The top-level README for developers using this project.

---

## User Guide

When your environment is ready, please follow the next steps:

1. Install requirements:

```bash 
pip install -r requirements.txt
```

2. Execute bootstrap command to create the stack: This command will create the stack in the AWS account that you have configured in the AWS CLI, only execute this command once.

```bash
cd aws && cdk bootstrap aws://<account_id>/<region>
```

3. Execute the deploy command to create the stack: This command will create the stack in the AWS account that you have configured in the AWS CLI, please execute this command in the root of the project.

```bash
python3 main.py
```


