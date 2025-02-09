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

## **🔹 IAM Permissions Required**
Your Lambda function and EC2 instance need the following permissions:  

### **1️⃣ Lambda IAM Role (LambdaAMIManagementRole)**
✅ **EC2 permissions** → Manage instances, create AMIs, and delete old AMIs  
✅ **SSM permissions** → Run patching commands on EC2 instances  
✅ **SNS permissions** → Send notifications to an SNS topic  
✅ **IAM PassRole** → Allow EC2 to assume its instance profile  

📌 **Full IAM Policy for Lambda:**  
🔗 [Lambda IAM Role Policy](https://github.com/saratkalisetty/aws-ami-patching-automation/blob/main/iam/lambda_role.json)  

### **2️⃣ EC2 IAM Role (EC2SSMRole)**
✅ **SSM permissions** → Execute patching commands and retrieve system info  
✅ **EC2 Describe permissions** → View instance details  

📌 **Full IAM Policy for EC2:**  
🔗 [EC2 SSM Role Policy](https://github.com/saratkalisetty/aws-ami-patching-automation/blob/main/iam/ec2_ssm_role.json)  

---
🔗 **Read the full tutorial on Medium** 👉 [My Medium Post](https://medium.com/@sarathkalisetty/automating-aws-ami-patching-using-lambda-ssm-and-sns-notifications-e15a21d0ed12)  

🚀 **Star & Fork this repo if you found it helpful!** ⭐  

📩 Contributions are welcome! Feel free to submit a PR with improvements.
