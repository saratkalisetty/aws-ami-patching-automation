# ⏳ Automating AMI Patching with EventBridge (Scheduled Execution)

## 📌 Overview
To ensure **automated execution**, we use **AWS EventBridge** to trigger the Lambda function **monthly on the 1st at 8 AM EST**.

## 🔹 Step-by-Step Guide to Set Up EventBridge Rule

### 1️⃣ Go to AWS EventBridge
- Open **AWS Console** → **EventBridge** → Click **Rules**
- Click **Create rule**

### 2️⃣ Define Rule Details
- **Name:** `Lambda-AMI-Patching-Schedule`
- **Description:** "Triggers AMI patching Lambda monthly"

### 3️⃣ Select Event Source  
- **Event Source Type:** `Schedule`  
- **Expression Type:** `Cron expression`  
- **Enter the cron schedule:**  
  ```plaintext
  cron(0 13 1 * ? *)  # Runs at 8 AM EST (13:00 UTC) on the 1st of every month

### 4️⃣ Choose Target
- Target Type: AWS Lambda function
- Select Your Lambda Function (the one handling AMI patching)

### 5️⃣ Review & Create
- Click Create and verify that the rule is enabled.
- This will trigger the Lambda function automatically every month!
