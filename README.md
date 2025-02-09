# aws-ami-patching-automation
Automated AWS AMI patching using Lambda, SSM, SNS, and EventBridge.

# AWS AMI Patching Automation 🚀  

This project automates **EC2 instance patching, AMI creation, and cleanup** using **AWS Lambda, SSM, SNS, and EventBridge**.

## Features 🌟
✔ Automatically finds and patches latest AMIs  
✔ Runs **SSM commands** to apply updates  
✔ Reboots the instance and ensures readiness  
✔ Creates a **new AMI** after patching  
✔ Deletes **old AMIs & snapshots** older than **120 days**  
✔ Sends **SNS notifications** with logs  

## 📌 Setup Instructions
1️⃣ Deploy the **Lambda function**  
2️⃣ Attach the correct **IAM roles**  
3️⃣ Set up **AWS EventBridge** to run on a schedule

## 🔹 IAM Permissions Required for Lambda
To ensure proper execution, your **Lambda function IAM Role** should have:
- ✅ **EC2 permissions** → Start, stop, create AMIs, and delete old AMIs
- ✅ **SSM permissions** → Execute commands on EC2 instances
- ✅ **SNS permissions** → Send notifications to an SNS topic
- ✅ **IAM PassRole** → Allow EC2 to assume its instance profile

🔗 **See the full IAM policy template in AWS Docs or create your own using the AWS Policy Generator.**


🔗 **Read the full tutorial on Medium** 👉 [My Medium Post](https://medium.com/your-medium-link)  

🚀 **Star & Fork this repo if you found it helpful!** ⭐  
