import boto3
import os
import time
from datetime import datetime, timedelta
import botocore.exceptions

# AWS Clients
ec2 = boto3.client('ec2', region_name='us-east-1')
ssm = boto3.client('ssm', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

# Configuration (Update with your values)
AMI_PREFIX = "My-Custom-AMI"
INSTANCE_TYPE = 't3.medium'
IAM_ROLE = 'my-ec2-role'
VPC_SUBNET_ID = 'subnet-xxxxxx'
SECURITY_GROUP_ID = 'sg-xxxxxx'
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')  # SNS Topic from environment variable

# Cleanup Policy (AMIs older than 120 days)
THRESHOLD_DATE = (datetime.utcnow() - timedelta(days=120)).isoformat()

def get_latest_custom_amis():
    """Fetches all AMIs matching the naming pattern, sorted by creation date."""
    response = ec2.describe_images(
        Filters=[{"Name": "name", "Values": [f"{AMI_PREFIX}-*"]}],
        Owners=['self']
    )
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return [ami['ImageId'] for ami in images] if images else []

def launch_ec2_instance(ami_id):
    """Launch an EC2 instance using the given AMI ID."""
    instance_response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=INSTANCE_TYPE,
        IamInstanceProfile={'Name': IAM_ROLE},
        MinCount=1,
        MaxCount=1,
        SubnetId=VPC_SUBNET_ID,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'AMI-Patching-Instance'}]}]
    )
    return instance_response['Instances'][0]['InstanceId']

def patch_and_reboot(instance_id):
    """Run patching via SSM, reboot, and verify instance is available."""
    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ['sudo dnf upgrade -y', 'sudo reboot']},
        TimeoutSeconds=3600
    )
    time.sleep(300)  # Allow time for reboot

def create_ami(instance_id):
    """Creates a new AMI from the patched instance."""
    ami_name = f"{AMI_PREFIX}-{datetime.now().strftime('%Y-%m-%d')}"
    response = ec2.create_image(InstanceId=instance_id, Name=ami_name, NoReboot=True)
    return response['ImageId']

def cleanup_old_amis():
    """Deletes AMIs older than 120 days along with their snapshots."""
    images = ec2.describe_images(Owners=['self'])['Images']
    for image in images:
        if image['Name'].startswith(AMI_PREFIX) and image['CreationDate'] < THRESHOLD_DATE:
            ami_id = image['ImageId']
            ec2.deregister_image(ImageId=ami_id)
            snapshots = ec2.describe_snapshots(Filters=[{"Name": "description", "Values": [f"*{ami_id}*"]}])['Snapshots']
            for snapshot in snapshots:
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

def send_sns_notification(status, message):
    """Sends an SNS notification with execution results."""
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject=f"Lambda Execution: {status}")

def lambda_handler(event, context):
    """Main Lambda function."""
    log = ["🚀 Lambda function started."]
    try:
        ami_list = get_latest_custom_amis()
        for ami_id in ami_list:
            instance_id = launch_ec2_instance(ami_id)
            log.append(f"✅ Launched instance {instance_id} for AMI {ami_id}.")
            patch_and_reboot(instance_id)
            new_ami = create_ami(instance_id)
            log.append(f"✅ Created new AMI {new_ami} from instance {instance_id}.")
            ec2.terminate_instances(InstanceIds=[instance_id])
            log.append(f"✅ Terminated instance {instance_id} after AMI creation.")
        cleanup_old_amis()
        log.append("✅ Old AMIs and snapshots cleaned up.")
        send_sns_notification("Success", "\n".join(log))
        return {"status": "Success", "amis_patched": ami_list}
    except Exception as e:
        log.append(f"❌ ERROR: {str(e)}")
        send_sns_notification("Failure", "\n".join(log))
        return {"status": "Failure", "error": str(e)}
