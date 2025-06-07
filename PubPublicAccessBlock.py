import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-southeast-1:209479264082:Project2S3AlarmTopic"  

def lambda_handler(event, context):
    try:
        # 获取第一个 S3 bucket 名称
        bucket_list = event['detail']['resource']['s3BucketDetails']
        bucket_name = bucket_list[0]['name']
        
        # 设置 Block Public Access 回到安全值
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        
        # 生成成功信息
        message = f"[AUTO-RESPONSE] Successfully restored BlockPublicAccess for bucket: {bucket_name}"
        print(message)
        
        # 发 SNS 邮件
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="GuardDuty Alert: S3 Public Access Block Restored",
            Message=message
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    except Exception as e:
        error_message = f"[ERROR] Lambda failed: {str(e)}"
        print(error_message)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="GuardDuty Auto-Response Error",
            Message=error_message
        )
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }
